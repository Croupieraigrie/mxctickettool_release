import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger("bot")

class TicketCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Ouvre un ticket en DM")
    async def ticket(self, interaction: discord.Interaction):
        if not isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Cette commande doit être utilisée en message privé (DM) avec le bot.", ephemeral=True
            )
            return

        await interaction.response.send_message("✅ Ton ticket a été ouvert avec succès.", ephemeral=True)

    @app_commands.command(name="close", description="Ferme ton ticket en DM")
    async def close(self, interaction: discord.Interaction):
        if not isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Cette commande doit être utilisée en DM.", ephemeral=True
            )
            return

        await interaction.response.send_message("🚪 Ticket fermé. Merci pour ta demande.", ephemeral=True)

async def setup(bot: commands.Bot):
    logger.info("📦 Cog Ticket chargé")
    await bot.add_cog(TicketCog(bot))
