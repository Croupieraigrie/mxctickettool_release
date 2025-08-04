import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_IDS = [int(guild_id) for guild_id in os.getenv("GUILD_ID", "").split(",") if guild_id]
TICKET_CHANNEL_ID = [1401946039283482634]


def require_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise EnvironmentError(f"La variable d'environnement '{name}' est manquante dans le fichier .env.")
    return value

class Config:
    DISCORD_TOKEN: str = require_env_var("DISCORD_TOKEN")
    GUILD_ID: int = int(require_env_var("GUILD_ID"))
    APPLICATION_ID: int = int(require_env_var("APPLICATION_ID"))
    STAFF_ROLE_ID: int = int(require_env_var("STAFF_ROLE_ID"))
    LOG_CHANNEL_ID: int = int(require_env_var("LOG_CHANNEL_ID"))
    TICKET_CHANNEL_ID: int = int(require_env_var("TICKET_CHANNEL_ID"))

    # Optionnel : type de base de données (sqlite ou mysql)
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")  # valeur par défaut : sqlite

    # Ajoute ici d'autres options si besoin, comme une URL MySQL :
    # MYSQL_URL: str = os.getenv("MYSQL_URL")
