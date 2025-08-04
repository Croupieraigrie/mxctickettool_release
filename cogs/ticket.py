import discord
from discord.ext import commands
from bot.database import db
from bot.config import Config
import os

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_ticket_for_user(self, user: discord.User):
        guild = self.bot.get_guild(Config.GUILD_ID)
        category = discord.utils.get(guild.categories, id=Config.STAFF_CATEGORY_ID)

        # Création entrée DB
        insert_query = "INSERT INTO tickets (user_id, status) VALUES (%s, 'open')"
        ticket_id = await db.execute(insert_query, (user.id,))

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            # Ajouter ici les rôles staff qui doivent voir les tickets
        }

        channel = await guild.create_text_channel(f"ticket-{ticket_id}", category=category, overwrites=overwrites)

        update_query = "UPDATE tickets SET channel_id = %s WHERE id = %s"
        await db.execute(update_query, (channel.id, ticket_id))

        log_channel = guild.get_channel(Config.LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="Nouveau ticket créé",
                description=f"Ticket #{ticket_id} créé par {user} ({user.id})",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            await log_channel.send(embed=embed)

        return ticket_id, channel

    async def generate_transcript(self, channel: discord.TextChannel):
        messages = []
        async for msg in channel.history(limit=None, oldest_first=True):
            messages.append({
                "author": str(msg.author),
                "timestamp": msg.created_at.isoformat(),
                "content": msg.content
            })

        os.makedirs("transcripts", exist_ok=True)
        html = f"<html><body><h2>Transcript du ticket {channel.name}</h2><hr>"
        for m in messages:
            html += f"<p><b>{m['author']}</b> [{m['timestamp']}]: {m['content']}</p>"
        html += "</body></html>"

        filepath = f"transcripts/{channel.name}.html"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return filepath

    async def close_ticket_for_user(self, ticket_id: int):
        update_query = "UPDATE tickets SET status = 'closed' WHERE id = %s"
        await db.execute(update_query, (ticket_id,))

    @commands.slash_command(name="ticket", description="Ouvrir un ticket via DM")
    async def ticket(self, ctx: discord.ApplicationContext):
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.respond("Commande à utiliser en message privé uniquement.", ephemeral=True)
            return

        user = ctx.author
        existing = await db.query("SELECT id FROM tickets WHERE user_id = %s AND status = 'open'", (user.id,))
        if existing:
            await ctx.respond("Vous avez déjà un ticket ouvert.", ephemeral=True)
            return

        ticket_id, channel = await self.create_ticket_for_user(user)
        await ctx.respond(f"Ticket #{ticket_id} créé, le staff vous répondra bientôt.", ephemeral=True)

        embed = discord.Embed(title=f"Nouveau ticket #{ticket_id}", description=f"Ouvert par {user}", color=discord.Color.green())
        embed.set_thumbnail(url=user.display_avatar.url)
        await channel.send(embed=embed)

    @commands.slash_command(name="close", description="Fermer votre ticket via DM")
    async def close(self, ctx: discord.ApplicationContext):
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.respond("Commande à utiliser en message privé uniquement.", ephemeral=True)
            return

        user = ctx.author
        existing = await db.query("SELECT id, channel_id FROM tickets WHERE user_id = %s AND status = 'open'", (user.id,))
        if not existing:
            await ctx.respond("Vous n'avez aucun ticket ouvert.", ephemeral=True)
            return

        ticket_id, channel_id = existing[0]
        await self.close_ticket_for_user(ticket_id)

        channel = self.bot.get_channel(channel_id)
        if channel:
            transcript_path = await self.generate_transcript(channel)
            await channel.send(file=discord.File(transcript_path, filename=f"transcript_{ticket_id}.html"))
            try:
                await channel.delete(reason=f"Ticket fermé par {user}")
            except Exception as e:
                print(f"Erreur suppression channel: {e}")

        await ctx.respond("Ticket fermé, merci de votre patience.", ephemeral=True)

def setup(bot):
    bot.add_cog(Ticket(bot))
