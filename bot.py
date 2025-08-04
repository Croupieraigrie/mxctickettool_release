import discord
from discord.ext import commands
import asyncio
from bot.database import db
from bot.config import Config

intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire les messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} (ID : {bot.user.id})")
    # Initialisation pool DB
    await db.init_pool()
    # Chargement des cogs
    await bot.load_extension("cogs.ticket")
    print("Cogs chargés avec succès.")

async def main():
    async with bot:
        await bot.start(Config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
