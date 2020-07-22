import random as r
import sqlite3
import discord
from discord.ext import commands
import asyncio
import datetime

class QuoteCog(commands.Cog, name='TVQuotes'):

        def __init__(self, bot):
            self.bot = bot

        @commands.command()
        async def b99(self, ctx):
            db = sqlite3.connect('seriesquotes.db')
            cursor = db.cursor()
            cursor.execute('''
            SELECT Quote.quote, Character.name, Series.name FROM Quote JOIN Character JOIN Series
            ON Quote.character_id = Character.id and Character.series_id = Series.id
            WHERE Character.series_id == 1 ORDER BY random() LIMIT 1
            ''')
            result = cursor.fetchall()
            for row in result:
                quote, character, series = row
                await ctx.send(f"{quote}\n - **{character}**, *{series}*")

        @commands.command()
        async def tv(self, ctx):
            db = sqlite3.connect('seriesquotes.db')
            cursor = db.cursor()
            cursor.execute('''
            SELECT Quote.quote, Character.name, Series.name FROM Quote JOIN Character JOIN Series
            ON Quote.character_id = Character.id and Character.series_id = Series.id
            ORDER BY random() LIMIT 1
            ''')
            result = cursor.fetchall()
            for row in result:
                quote, character, series = row
                await ctx.send(f"{quote}\n - **{character}**, *{series}*")

        @commands.command()
        async def office(self, ctx):
            db = sqlite3.connect('seriesquotes.db')
            cursor = db.cursor()
            cursor.execute('''
            SELECT Quote.quote, Character.name, Series.name FROM Quote JOIN Character JOIN Series
            ON Quote.character_id = Character.id and Character.series_id = Series.id
            WHERE Character.series_id == 2 ORDER BY random() LIMIT 1
            ''')
            result = cursor.fetchall()
            for row in result:
                quote, character, series = row
                await ctx.send(f"{quote}\n - **{character}**, *{series}*")

def setup(bot):
    bot.add_cog(QuoteCog(bot))
    db = sqlite3.connect('seriesquotes.db')
    cursor = db.cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Series (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Character (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        series_id INTEGER,
        name TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Quote (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        series_id INTEGER,
        character_id INTEGER,
        quote TEXT
    )
    ''')
    print('TVQuotes is loaded')
