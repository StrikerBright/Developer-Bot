import discord
from discord.ext import commands
from playerjoin import handle_member_join, cache_invites
from ticketsystem import send_ticket_embed

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.invites = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with Python"))
    print(f'Logged in as {bot.user}!')
    for guild in bot.guilds:
        await cache_invites(guild)
    # Send the ticket embed (only once, or add logic to avoid duplicates)
    channel = bot.get_channel(1374871127796486226)
    if channel:
        await send_ticket_embed(bot)

@bot.event
async def on_member_join(member):
    await handle_member_join(bot, member)

bot.run('MTM3NDkyODEyODIyODcyMDY5MQ.Gjnp1i.e0HQFRgnRgBvDqAYNPv-Dv_9Dd6_ApdMoX7by4')
