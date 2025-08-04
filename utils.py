def is_dm(channel):
    return getattr(channel, "type", None) == discord.ChannelType.private
