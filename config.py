import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CLIENT_ID = int(os.getenv("DISCORD_CLIENT_ID"))
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
TICKET_CHANNEL_ID = int(os.getenv("TICKET_CHANNEL_ID"))

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

STAFF_ROLE_IDS = [
    1371158093030887444  # Exemple d'ID rôle staff
]
