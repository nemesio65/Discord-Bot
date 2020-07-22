import random as r
import sqlite3
import discord
from discord.ext import commands
import asyncio
import datetime
import math

class LvlCog(commands.Cog, name='Leveling'):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_message(self, message):
            db = sqlite3.connect('bot.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
                val = (message.author.guild.id, message.author.id, 2, 0)
                cursor.execute(sql, val)
                db.commit()
            else:
                cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
                result1 = cursor.fetchone()
                exp = int(result1[1])
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (exp + 2, str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()

                cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
                result2 = cursor.fetchone()

                xp_start = int(result2[1])
                lvl_start = int(result2[2])
                xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
                if xp_end < xp_start:
                    await message.channel.send(f"{message.author.mention} has leveled up to level {lvl_start + 1}.")
                    sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
                    val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                    val = (0, str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

        @commands.command()
        async def rank(self, ctx, user:discord.User=None):
            if user is not None:
                db = sqlite3.connect('bot.db')
                cursor = db.cursor()
                cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{user.id}'")
                result = cursor.fetchone()
                if result is None:
                    await ctx.send('That user is not yet ranked.')
                else:
                    await ctx.send(f"{user.name} is currently levels '{str(result[2])}' and has '{str(result[1])}' XP.")
                cursor.close()
                db.close()
            elif user is None:
                    db = sqlite3.connect('bot.db')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
                    result = cursor.fetchone()
                    if result is None:
                        await ctx.send('That user is not yet ranked.')
                    else:
                        await ctx.send(f"{ctx.message.author.name} is currently level '{str(result[2])}' and has '{str(result[1])}' XP.")
                    cursor.close()
                    db.close()

def setup(bot):
    bot.add_cog(LvlCog(bot))
    db = sqlite3.connect('bot.db')
    cursor = db.cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS levels (
        guild_id TEXT,
        user_id TEXT,
        exp TEXT,
        lvl TEXT 
    )
    ''')
    print('Leveling is loaded')
