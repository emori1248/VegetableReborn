import discord
import os

import shutil
import random

from discord.ext import commands
import music
#import tts
import imagemod
# import calendarapi

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = 'def dog:'

intents = discord.Intents().all()
client = discord.Client(intents=intents)
activity = discord.Game(name="Fuckers put me on AWS")
bot = commands.Bot(command_prefix='~', intents=intents, activity=activity)

generic_error = "Something broke, msg Potato (See console)."
version = "0.1.3"



"""

TODO Reimplement:
Webserver
Nice looking help command

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

TODO calendar design
type ~register in a dm channel to register for notifs
on startup add all registered users to a notif list
get the next event from goog calendar and set a timer to post that to all registered user dms when it fires
on event fire set timer for next event
"""

# Generic Commands
@bot.command(name='image')
async def imageCommand(ctx, arg):
    if (await imagemod.addCenteredTextToImage(arg)):
        await ctx.send(file=discord.File(r'tmp/output.jpg'))
    else:
        await ctx.send(generic_error)
        print("ERROR: img dir empty for image command")


# TTS

@bot.command(name='tts')
async def testCommand(ctx, arg):
    # filename = tts.synthesize_text(arg)
    # await music.play_file(ctx, filename, bot)
    await ctx.send("TTS is currently disabled due to reaching Google's TTS quota.")
    # Ran out of google TTS api quota lmao might switch

# Admin Commands

@bot.command(name='version')
async def versionCommand(ctx):
    await ctx.send(f'Bot is running version {version}.')

# @bot.command(name='timeout')
# async def timeoutCommand(ctx):
#     member = ctx.message.author
#     role = discord.utils.get(ctx.message.guild.roles, name="Timeout")
#     await member.add_roles(role)

# Music Commands

# @bot.command(name='test')
# async def testCommand(ctx):
#     content = calendarapi.main()
    
#     await ctx.send(content)

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

@bot.event
async def on_message(message):
    # print("test")
    # print(message.author.roles)

    for role in message.author.roles:
        if role.name.lower() == "horse": # User has role
            if random.randint(0, 20) == 0:
                await message.reply(random.choice(["ok gabe", "heard", "over", "good comms", "ratio + homeless", "who asked tho"]))

    

bot.run(TOKEN)