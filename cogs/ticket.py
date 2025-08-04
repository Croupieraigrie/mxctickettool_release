import discord
from discord.ext import commands
from database import db
from datetime import datetime
from utils import is_dm

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ticket", description="Ouvrir un ticket d'assistance via DM")
    async def ticket(self, ctx: discord.ApplicationContext):
        if not is_dm(ctx.channel):
            await ctx.respond("Cette commande doit être utilisée en message privé (DM).", ephemeral=True)
            return

        user = ctx.author

        existing = await db.query("SELECT id FROM tickets WHERE user_id = %s AND status = 'open'", (user.id,))
        if existing:
            await ctx.respond("Vous avez déjà un ticket ouvert.", ephemeral=True)
            return

        from ticket_manager import create_ticket_for_user
        ticket_id, channel = await create_ticket_for_user(self.bot, user)

        await ctx.respond("Votre ticket a été créé, un membre du staff vous répondra bientôt.", ephemeral=True)

        embed = discord.Embed(title=f"Nouveau ticket #{ticket_id}",
                              description=f"Ticket ouvert par {user} (ID: {user.id})",
                              color=discord.Color.green())
        embed.set_thumbnail(url=user.display_avatar.url)
        await channel.send(embed=embed)

    @commands.slash_command(name="close", description="Fermer votre ticket via DM")
    async def close(self, ctx: discord.ApplicationContext):
        if not is_dm(ctx.channel):
            await ctx.respond("Cette commande doit être utilisée en message privé (DM).", ephemeral=True)
            return

        user = ctx.author
        existing = await db.query("SELECT id, channel_id FROM tickets WHERE user_id = %s AND status = 'open'", (user.id,))
        if not existing:
            await ctx.respond("Vous n'avez aucun ticket ouvert.", ephemeral=True)
            return

        from ticket_manager import close_ticket_for_user
        ticket_id, channel_id = existing[0]
        await close_ticket_for_user(self.bot, ticket_id, user_initiated=True)

        channel = self.bot.get_channel(int(channel_id))
        if channel:
            from html_generator import generate_transcript
            transcript_path = await generate_transcript(channel)
            await channel.send(file=discord.File(transcript_path, filename=f"transcript_ticket_{ticket_id}.html"))

            try:
                await channel.delete(reason=f"Ticket #{ticket_id} fermé par l'utilisateur {user}.")
            except Exception as e:
                print(f"Erreur suppression channel : {e}")

        await ctx.respond("Votre ticket a été fermé. Merci d'avoir contacté le support.", ephemeral=True)

def setup(bot):
    bot.add_cog(Ticket(bot))
