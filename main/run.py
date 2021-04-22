import discord
import os

import shutil

from discord.ext import commands
import music
import tts
import imagemod

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = 'def dog:'

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='~',intents=intents)



"""
TODO Reimplement:
Webserver

Commands:
    Say
    Summon (@everyone)
    Chaos (Move people around a lot)
    Shutdown (Play windows xp shutdown and then DC)
    Vinny (Posts a random vinny video)
    CBT
    Cum

Music Functionality

TTS Functionality

TODO New Features:
markov chain thing
see if a posted picture is of a cat
Commands:
    Check if minecraft server is up and running
"""

# Generic Commands
@bot.command(name='image')
async def imageCommand(ctx, arg):
    filename = await imagemod.addCenteredTextToImage(arg)
    await ctx.send(file=discord.File(r'img/result.jpg'))
    await imagemod.deleteResult()


# TTS

@bot.command(name='tts')
async def testCommand(ctx):
    filename = tts.synthesize_text("test")
    await music.play_file(ctx, filename, bot)

# Music Commands

@bot.command(name='test')
async def testCommand(ctx):
    await ctx.send('eat shit and die.')

@bot.command(name='join',help='Joins the bot into the channel')
async def join(ctx):
    await music.join(ctx)

@bot.command(name='leave', help='Kicks the bot from the channel')
async def leave(ctx):
    await music.leave(ctx)

@bot.command(name='play', help='To play song')
async def play(ctx, url):
    await music.play(ctx, url, bot)

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    await music.pause(ctx)

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    await music.resume(ctx)

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    await music.stop(ctx)

# Passive events (startup/etc.)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    

bot.run(TOKEN)