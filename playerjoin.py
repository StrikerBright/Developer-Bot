import discord

CHANNEL_ID = 1374965276457570344
DEFAULT_INVITE = "https://discord.gg/2py3Tm5ySs"

invite_cache = {}

async def cache_invites(guild):
    invites = await guild.invites()
    invite_cache[guild.id] = {invite.code: invite.uses for invite in invites}

async def handle_member_join(client, member):
    # Get invites before join from cache
    before_invites = invite_cache.get(member.guild.id, {})
    # Get invites after join
    invites = await member.guild.invites()
    used_invite = None

    for invite in invites:
        before_uses = before_invites.get(invite.code, 0)
        if invite.uses > before_uses:
            used_invite = invite
            break

    # Update the cache for next join
    await cache_invites(member.guild)

    channel = member.guild.get_channel(CHANNEL_ID)
    if not channel:
        return

    if used_invite and used_invite.url == DEFAULT_INVITE:
        msg = f'Civilian {member.name} joined the DCNG server using the default URL'
    elif used_invite:
        # Format the invite as `discord.gg/code`
        invite_code = used_invite.url.replace("https://", "")
        msg = (f'Civilian {member.name} joined the DCNG server by {used_invite.inviter.name} '
               f'using `{invite_code}`')
    else:
        msg = f'Civilian {member.name} joined the DCNG server'

    await channel.send(msg)