import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    # IDs Discord
    GUILD_ID = int(os.getenv("GUILD_ID", 0))
    STAFF_CATEGORY_ID = int(os.getenv("STAFF_CATEGORY_ID", 0))
    LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", 0))
