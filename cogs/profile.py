import random as r
import sqlite3
import discord
from discord.ext import commands
import asyncio
import datetime
import math


class ProfileCog(commands.Cog, name='Profile'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def biosetup(self, ctx, *, content:str):
        db = sqlite3.connect('bot.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT profiles.user_id, profiles.guild_id FROM profiles JOIN levels ON profiles.user_id = levels.user_id and profiles.guild_id = levels.guild_id WHERE levels.guild_id = '{ctx.message.author.guild.id}' and levels.user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO profiles(guild_id, user_id, bio, twitch) VALUES(?,?,?,?)")
            val = (ctx.message.author.guild.id, ctx.message.author.id, str(content), None)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send('Your bio has been updated.')
        else:
            cursor.execute(f"SELECT user_id, bio FROM profiles WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            sql = ("UPDATE profiles SET bio = ? WHERE guild_id = ? and user_id = ?")
            val = (str(content), str(ctx.message.guild.id), str(ctx.message.author.id))
            cursor.execute(sql, val)
            db.commit()

            await ctx.send(f"your bio has been updated.")

    @commands.command()
    async def twitchsetup(self, ctx, *, content:str):
        db = sqlite3.connect('bot.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT profiles.user_id, profiles.guild_id FROM profiles JOIN levels ON profiles.user_id = levels.user_id and profiles.guild_id = levels.guild_id WHERE levels.guild_id = '{ctx.message.author.guild.id}' and levels.user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO profiles(guild_id, user_id, bio, twitch) VALUES(?,?,?,?)")
            val = (ctx.message.author.guild.id, ctx.message.author.id, None, str(content))
            cursor.execute(sql, val)
            db.commit()
            await ctx.send('Your twitch has been updated.')
        else:
            cursor.execute(f"SELECT user_id, twitch FROM profiles WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            sql = ("UPDATE profiles SET twitch = ? WHERE guild_id = ? and user_id = ?")
            val = (str(content), str(ctx.message.guild.id), str(ctx.message.author.id))
            cursor.execute(sql, val)
            db.commit()

            await ctx.send(f"your twitch has been updated.")

    @commands.command()
    async def bio(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('bot.db')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user_id, bio, twitch FROM profiles WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('That user has no bio.')
            else:
                await ctx.send(f"{user.name} bio: '{str(result[1])}' twitch: '{str(result[2])}' .")
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('bot.db')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user_id, bio, twitch FROM profiles WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('That user has no bio.')
            else:
                await ctx.send(
                    f"{ctx.message.author.name} bio: '{str(result[1])}' twitch: '{str(result[2])}' .")
            cursor.close()
            db.close()


def setup(bot):
    bot.add_cog(ProfileCog(bot))
    db = sqlite3.connect('bot.db')
    cursor = db.cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS profiles (
        guild_id TEXT,
        user_id TEXT,
        bio TEXT,
        twitch TEXT
    )
    ''')
    print('Profiles is loaded')
