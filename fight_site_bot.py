#A bot created to text members of the server to get on discord
#Created by Elias Frieling

import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from html.parser import HTMLParser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import datetime
from pytz import timezone
import pytz


load_dotenv()
#discord bot token
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

#on start message
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    #elias_timeout = False

#on !fighter message
@bot.command()
async def fighter(ctx, *, search_term):
    search = search_term.replace(' ', '+')
    url = 'https://www.thefight-site.com/search?q=' + search
    try:
        page = urlopen(url)
    except:
        await ctx.channel.send("Error opening the URL")
    soup = BeautifulSoup(page, 'html.parser')
    try:
        new_url = soup.find('div', {"class": "search-result"}).attrs['data-url']
    except Exception as e:
        with open('err.log', 'w') as file:
            file.write(str(e))
        file.close()
        await ctx.channel.send('Sorry something went wrong, try checking your spelling')
    await ctx.channel.send('https://www.thefight-site.com' + new_url)
#on !roast command
@bot.command()
async def roast(ctx):
    roasts = [
    'Ed\'s favorite fighter is Jon Jones',
    'Ryan thinks Tony beats Khabib',
    'ACA is worse than Bellator',
    'Boxing sucks',
    'Wonderboy is the best kickboxer in MMA'
    ]
    await ctx.channel.send(random.choice(roasts))

#on !help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        color = discord.Colour.orange()
    )
    embed.set_author(name='List of commands')
    embed.add_field(name='!fighter *enter name*', value='Returns the top fight site article for that fighter', inline=False)
    await ctx.channel.send(embed=embed)
#on !currenttime command
@bot.command()
async def currenttime(ctx):

    tz_NY = pytz.timezone('America/New_York')
    datetime_NY = datetime.now(tz_NY)
    await ctx.channel.send("NY time:" + datetime_NY.strftime("%H:%M:%S"))

    tz_London = pytz.timezone('Europe/London')
    datetime_London = datetime.now(tz_London)
    await ctx.channel.send("London time:" + datetime_London.strftime("%H:%M:%S"))

bot.run(TOKEN)
