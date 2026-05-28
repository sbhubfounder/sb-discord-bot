import discord
from discord.ext import commands
import os
import datetime
from flask import Flask
from threading import Thread

# 1. Keep-Alive Web Server (For 24/7 Free Hosting)
app = Flask('')
@app.route('/')
def home():
    return "Bot is active, welcoming, and moderating!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Configure Intents (Required to see joins and read commands)
intents = discord.Intents.default()
intents.members = True          # Required to see when users join
intents.message_content = True  # Required to read !kick, !ban, !mute commands

bot = commands.Bot(command_prefix="!", intents=intents)

# 3. Event: Bot is Ready & Set Status
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Welcoming users!"))
    print("Status set to 'Welcoming users!'")

# 4. Event: Welcome User
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if not channel:
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
    
    if channel:
        embed = discord.Embed(
            title="Welcome to the server!",
            description=f"Welcome {member.mention}! We are glad to have you here.",
            color=discord.Color.blue()
        )
        embed.set_image(url=member.display_avatar.url)
        
        await channel.send(content=member.mention, embed=embed)

# ----------------------------------------------------
# 5. MODERATION COMMANDS
# ----------------------------------------------------

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    """Kicks a user and DMs them the reason."""
    # Try to DM the user first before kicking them
    try:
        await member.send(f"You have been kicked from **{ctx.guild.name}**. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send(f"*(Note: Could not DM {member.mention} because their DMs are closed.)*")
    
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} has been kicked. Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    """Bans a user and DMs them the reason."""
    # Try to DM the user first before banning them
    try:
        await member.send(f"You have been banned from **{ctx.guild.name}**. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send(f"*(Note: Could not DM {member.mention} because their DMs are closed.)*")
    
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} has been banned. Reason: {reason}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
    """Mutes (Times out) a user for a specific amount of minutes and DMs them."""
    duration = datetime.timedelta(minutes=minutes)
    
    # Try to DM the user first
    try:
        await member.send(f"You have been muted in **{ctx.guild.name}** for {minutes} minutes. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send(f"*(Note: Could not DM {member.mention} because their DMs are closed.)*")
        
    await member.timeout(duration, reason=reason)
    await ctx.send(f"🔇 {member.mention} has been muted for {minutes} minutes. Reason: {reason}")


# ----------------------------------------------------
# 6. Start the Bot
# ----------------------------------------------------
keep_alive()

TOKEN = os.environ.get('MTUwOTY2NzA0NTY3MzkzMDgwMg.GK-60z.6eAM-3Seu6sSKrc6boT5XWp8f280sMS6mV2U38')
if TOKEN:
    bot.run(MTUwOTY2NzA0NTY3MzkzMDgwMg.GK-60z.6eAM-3Seu6sSKrc6boT5XWp8f280sMS6mV2U38)
else:
    print("Error: DISCORD_TOKEN environment variable not found.")