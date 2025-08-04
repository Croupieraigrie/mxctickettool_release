import discord
from discord.ext import commands
from discord import app_commands
import logging
import os

from mxctickettool.config import DISCORD_TOKEN, GUILD_IDS

# 🔧 Setup du logging
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

# 📁 Création du dossier logs si nécessaire
os.makedirs("logs", exist_ok=True)

handler = logging.FileHandler(filename="logs/bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# 🤖 Déclaration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="ping", description="Test de ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong !")



# 📦 Chargement dynamique des cogs + sync des commandes
@bot.event
async def on_ready():
    logger.info(f"Connecté en tant que {bot.user} (ID: {bot.user.id})")
    print(f"✅ {bot.user} est en ligne et prêt")

    # 🔄 Synchronisation des commandes globales
    try:
        synced = await bot.tree.sync()
        logger.info(f"{len(synced)} commandes globales synchronisées")
    except Exception as e:
        logger.error("Erreur lors de la synchronisation globale :", exc_info=e)

    # 🌍 Synchronisation des commandes spécifiques à chaque serveur
    for guild_id in GUILD_IDS:
        try:
            guild = discord.Object(id=guild_id)
            synced_guild = await bot.tree.sync(guild=guild)
            logger.info(f"{len(synced_guild)} commandes synchronisées pour le serveur {guild_id}")
        except Exception as e:
            logger.error(f"Échec de la sync pour le serveur {guild_id} :", exc_info=e)

    # 📦 Chargement des cogs si le dossier existe
    if os.path.exists("./cogs"):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"✅ Cog '{filename}' chargé")
                except Exception as e:
                    logger.error(f"❌ Échec du chargement du cog '{filename}' :", exc_info=e)
    else:
        logger.warning("📁 Le dossier './cogs' n'existe pas — aucun cog chargé.")


        

# 🚀 Démarrage du bot
bot.run(DISCORD_TOKEN)
