#A bot created to text members of the server to get on discord
#Created by Elias Frieling

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from html.parser import HTMLParser
from urllib.request import urlopen
from bs4 import BeautifulSoup

client = discord.Client()
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

@bot.command()
async def fighter(ctx, *, search_term):
    search = ''
    for i in search_term:
        if i == ' ':
            search += '+'
        else:
            search += i
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


@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        color = discord.Colour.orange()
    )
    embed.set_author(name='List of commands')
    embed.add_field(name='!fighter', value='Returns the top fight site article for that fighter', inline=False)
    await ctx.channel.send(embed=embed)
bot.run(TOKEN)
