import discord
from database import db
from config import TICKET_CHANNEL_ID, STAFF_ROLE_IDS

async def create_ticket_for_user(bot, user):
    channel = bot.get_channel(TICKET_CHANNEL_ID)
    # Crée un thread dans le channel staff
    thread = await channel.create_thread(name=f"ticket-{user.name}", type=discord.ChannelType.public_thread)

    # Enregistre dans la BDD
    query = "INSERT INTO tickets (user_id, channel_id, status) VALUES (%s, %s, 'open')"
    ticket_id = await db.execute(query, (user.id, thread.id))

    # Mention du staff
    mention_roles = " ".join(f"<@&{role_id}>" for role_id in STAFF_ROLE_IDS)
    await thread.send(f"Nouveau ticket ouvert par {user.mention}\n{mention_roles}")

    return ticket_id, thread

async def close_ticket_for_user(bot, ticket_id, user_initiated=False):
    query = "UPDATE tickets SET status = 'closed' WHERE id = %s"
    await db.execute(query, (ticket_id,))

    # Optionnel: log fermeture ou autres actions
