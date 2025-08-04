import discord
from config import TICKET_CHANNEL_ID
from database import create_ticket, close_ticket

async def open_ticket_dm(ctx):
    guild = discord.utils.get(ctx.bot.guilds)
    channel = guild.get_channel(TICKET_CHANNEL_ID)
    thread = await channel.create_thread(name=f"ticket-{ctx.author.name}", type=discord.ChannelType.private_thread)
    create_ticket(ctx.author.id, thread.id)
    await thread.send(f"Nouveau ticket de {ctx.author.mention}")
    await ctx.respond("Ticket ouvert !")

async def close_ticket_dm(ctx):
    # Récupérer thread depuis DB
    # Envoyer logs, fermer thread, etc.
    await ctx.respond("Ticket fermé.")
