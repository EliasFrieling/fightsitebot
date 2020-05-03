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

@bot.command()
async def recent(ctx):
    """ Pulls up the most recent article on thefight-site.com"""
    page = urlopen('https://www.thefight-site.com')
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a'):
            if str(link.get('href')).startswith('/home/'):
                await ctx.channel.send('https://www.thefight-site.com' + str(link.get('href')))
                break
#on !roast command
@bot.command()
async def roast(ctx):
    roasts = [
    'Ed\'s favorite fighter is Jon Jones',
    'Ryan thinks Tony beats Khabib',
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
    embed.add_field(name='!recent', value='Returns the most recent article written', inline=False)
    embed.add_field(name='!currenttime', value='States time around the world', inline=False)
    embed.add_field(name='!roast', value='Says some dumb stuff', inline=False)
    await ctx.channel.send(embed=embed)
#on !currenttime command
@bot.command()
async def currenttime(ctx):

    tz_NY = pytz.timezone('America/New_York')
    datetime_NY = datetime.now(tz_NY)
    await ctx.channel.send("New York time: " + datetime_NY.strftime("%H:%M"))

    tz_London = pytz.timezone('Europe/London')
    datetime_London = datetime.now(tz_London)
    await ctx.channel.send("London time: " + datetime_London.strftime("%H:%M"))

    tz_Oslo = pytz.timezone('Europe/Oslo')
    datetime_Oslo = datetime.now(tz_Oslo)
    await ctx.channel.send("Kristiansund time: " + datetime_Oslo.strftime("%H:%M"))

bot.run(TOKEN)
