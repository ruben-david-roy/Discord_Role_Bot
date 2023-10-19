import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
import json
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

# load config data from config.json
with open("config.json", "r") as file:
    config = json.load(file)

# retrieve constants from the configuration
ROLE_ID = config["ROLE_ID"]
CHANNEL_ID = config["CHANNEL_ID"]
PREFIX = config["PREFIX"]

# configure bot permissions
intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True
intents.members = True

# initialize bot with a command prefix and set intents
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# set up a Flask application
app = Flask(__name__)

# flask route for checking bot status
@app.route('/')
def index():
    return "Bot Online! ✅"

# event to print bot details and set its status when it's ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    activity = discord.Activity(type=discord.ActivityType.watching, name="after the server")
    await bot.change_presence(activity=activity)

# check if the message is sent by a specific author in a specific channel
def check_user_dm(m, dm_channel, author):
    return m.channel == dm_channel and m.author == author

# utility function to get user and role details via DM
async def get_user_and_role(ctx, prompt):
    dm_channel = await ctx.author.create_dm()
    await dm_channel.send("Please provide the following information:")

    await dm_channel.send(f"{prompt} Username:")
    username_msg = await bot.wait_for(
        'message',
        check=lambda m: check_user_dm(m, dm_channel, ctx.author),
        timeout=60)
    user = discord.utils.find(
        lambda m: m.name == username_msg.content or m.display_name ==
        username_msg.content, ctx.guild.members)

    if not user:
        await dm_channel.send("User not found! Please provide a username and not a nickname. Note that this system is case-sensitive.")
        return None, None

    await dm_channel.send(f"{prompt} Role:")
    role_msg = await bot.wait_for(
        'message',
        check=lambda m: check_user_dm(m, dm_channel, ctx.author),
        timeout=60)
    role = discord.utils.get(ctx.guild.roles, name=role_msg.content)

    return user, role

# bot command to promote a user to a specific role
@bot.command()
async def promote(ctx):
    required_role = ctx.guild.get_role(ROLE_ID)

    if required_role in ctx.author.roles:
        user, promotion_role = await get_user_and_role(ctx, "Promoted")
        if user and promotion_role:
            await user.add_roles(promotion_role)
            print(f"{user.name} has just been promoted to {promotion_role.name}.")
            embed = discord.Embed(
                title=f"{user.name} has just been promoted to {promotion_role.name}.",
                color=discord.Color.blue())
            embed.set_footer(text="Authorised by the Administrators")
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)
        elif not promotion_role:
            await ctx.author.send("Role not found! Note that this system is case-sensitive.")
    else:
        await ctx.send("You do not have the required role to use this command.")

# bot command to demote a user from a specific role
@bot.command()
async def demote(ctx):
    required_role = ctx.guild.get_role(ROLE_ID)

    if required_role in ctx.author.roles:
        user, demotion_role = await get_user_and_role(ctx, "Demoted")
        if user and demotion_role:
            await user.remove_roles(demotion_role)
            print(f"{user.name} has just been demoted from {demotion_role.name}.")
            embed = discord.Embed(
                title=
                f"{user.name} has just been demoted from {demotion_role.name}.",
                color=discord.Color.blue())
            embed.set_footer(text="Authorised by the Administrators")
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)
        elif not demotion_role:
            await ctx.author.send("Role not found!")
    else:
        await ctx.send("You do not have the required role to use this command.")

# main execution: run bot and flask server concurrently
if __name__ == '__main__':
    from threading import Thread

    bot_token = os.getenv("BOT_TOKEN")

    t = Thread(target=bot.run, args=(bot_token, ))
    t.start()

    app.run(host='0.0.0.0', port=5000)
