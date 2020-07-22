import os
import random as r
import sqlite3
import discord
import giphy_client
from discord.ext import commands
from dotenv import load_dotenv
from giphy_client.rest import ApiException

load_dotenv()
D_TOKEN = os.getenv('discord_token')
G_TOKEN = os.getenv('giphy_token')

prefix = "?"
bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
api_instance = giphy_client.DefaultApi()

trigger_words = ['pander']

@bot.event
async def on_ready():
    print('--------')

    initial_extenstions = ['cogs.leveling',
                           'cogs.tvquotes',
                           'cogs.profile']

    if __name__ == '__main__':
        for extension in initial_extenstions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}', file=sys.stderr)
                traceback.print_exc()

    print(f'{bot.user.name} has connected to Discord!')
    print(f'userid: {bot.user.id}')
    print('--------')


async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(G_TOKEN, query, limit=10, rating='g')
        lst = list(response.data)
        gif = r.choices(lst)

        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

#@bot.event
#async def on_member_join(member):
#    embed = discord.Embed(colour=0xb0ec94, url="https://discordapp.com", description=f"Welcome to {member.guild}")
#    embed.set_thumbnail(url=f"{member.avatar.url}")
#    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar.url}")
#    embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

#    channel = await bot.get_channel(id=)

#    await bot.say(content="", embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    gif = await search_gifs('panda')

    if any(word.lower() in message.content.lower() for word in trigger_words):
        await message.channel.send(gif)


    if message.content == '99!':
        await message.channel.send('NINE-NINE!')

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong')

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)

bot.run(D_TOKEN)
