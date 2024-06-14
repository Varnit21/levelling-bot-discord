import discord
from discord.ext import commands
import aiosqlite
import time

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

LEVEL_ROLES = {
    5: 'ROLE_ID_1',
    10: 'ROLE_ID_2',
    20: 'ROLE_ID_3'
}

LEVEL_UP_CHANNEL_ID = 'YOUR_CHANNEL_ID'

user_last_message = {}
user_daily_claim = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await create_db()

async def create_db():
    async with aiosqlite.connect('leveling.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            xp INTEGER NOT NULL,
            level INTEGER NOT NULL
        )''')
        await db.commit()

async def get_user_data(user_id):
    async with aiosqlite.connect('leveling.db') as db:
        async with db.execute('SELECT xp, level FROM users WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0], row[1]
            else:
                await db.execute('INSERT INTO users (user_id, xp, level) VALUES (?, ?, ?)', (user_id, 0, 1))
                await db.commit()
                return 0, 1

async def update_user_xp(user_id, xp):
    async with aiosqlite.connect('leveling.db') as db:
        await db.execute('UPDATE users SET xp = xp + ? WHERE user_id = ?', (xp, user_id))
        await db.commit()

async def update_user_level(user_id, level):
    async with aiosqlite.connect('leveling.db') as db:
        await db.execute('UPDATE users SET level = ? WHERE user_id = ?', (level, user_id))
        await db.commit()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    current_time = time.time()
    last_message_time = user_last_message.get(user_id, 0)

    if current_time - last_message_time >= 60:
        user_last_message[user_id] = current_time
        xp, level = await get_user_data(user_id)
        xp += 10

        next_level_xp = level * 100
        if xp >= next_level_xp:
            level += 1
            await update_user_level(user_id, level)
            await send_level_up_message(message.author, level)

        await update_user_xp(user_id, 10)

    await bot.process_commands(message)

async def send_level_up_message(member, level):
    channel = bot.get_channel(int(LEVEL_UP_CHANNEL_ID))
    if channel:
        await channel.send(f'Congratulations {member.mention}, you have reached level {level}!')
    await assign_role(member, level)

async def assign_role(member, level):
    role_id = LEVEL_ROLES.get(level)
    if role_id:
        role = member.guild.get_role(int(role_id))
        if role:
            await member.add_roles(role)
            await member.send(f'You have been given the role: {role.name} for reaching level {level}!')

@bot.command()
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    xp, level = await get_user_data(member.id)
    await ctx.send(f'{member.display_name} is at level {level} with {xp} XP.')

@bot.command()
async def leaderboard(ctx):
    async with aiosqlite.connect('leveling.db') as db:
        async with db.execute('SELECT user_id, xp, level FROM users ORDER BY xp DESC LIMIT 10') as cursor:
            rows = await cursor.fetchall()
            leaderboard = '\n'.join([f'<@{row[0]}>: Level {row[2]}, {row[1]} XP' for row in rows])
            await ctx.send(f'**Leaderboard:**\n{leaderboard}')

@bot.command()
async def daily(ctx):
    user_id = ctx.author.id
    current_time = time.time()
    last_claim_time = user_daily_claim.get(user_id, 0)

    if current_time - last_claim_time >= 86400:
        user_daily_claim[user_id] = current_time
        xp, level = await get_user_data(user_id)
        daily_xp = 50
        xp += daily_xp
        await update_user_xp(user_id, daily_xp)
        await ctx.send(f'{ctx.author.mention}, you have claimed your daily reward of {daily_xp} XP!')

        next_level_xp = level * 100
        if xp >= next_level_xp:
            level += 1
            await update_user_level(user_id, level)
            await ctx.send(f'Congratulations {ctx.author.mention}, you have reached level {level}!')
            await send_level_up_message(ctx.author, level)
    else:
        remaining_time = 86400 - (current_time - last_claim_time)
        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f'{ctx.author.mention}, you can claim your next daily reward in {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.')

bot.run('YOUR_BOT_TOKEN')
