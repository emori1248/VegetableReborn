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

command_prefix = '~'
commands = []

intents = discord.Intents().all()
activity = discord.Game(name="Fuckers put me on AWS")

client = discord.Client(intents=intents, activity=activity)
generic_error = "Something broke, msg Potato (See console)."
version = "0.2.0"

# def add_command(func):
#     commands.append(SimpleCommand(name='test', executor=func))

class CommandHandler(object):
    def __init__(self, name, desc='default description.'):
        self.name = name
        self.description = desc

    def __call__(self, f):
        commands.append(SimpleCommand(name=self.name, description=self.description, executor=f))



class SimpleCommand:
    def __init__(self, name, executor, description):
        self.name = name
        self.description = description
        self.executor = executor


"""

TODO Reimplement:
Refactor out of Bot system to Client

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

@CommandHandler(name='image')
async def imageCommand(ctx, arg):
    if (await imagemod.addCenteredTextToImage(arg)):
        await ctx.send(file=discord.File(r'tmp/output.jpg'))
    else:
        await ctx.send(generic_error)
        print("ERROR: img dir empty for image command")

# TODO make better
@CommandHandler(name='help')
async def helpCommand(message, args):
    print("test")
    str = ""
    for command in commands:
        str += f'{command.name}: \'{command.description}\'\n'
    await message.channel.send(str)

# TTS

@CommandHandler(name='tts', desc='Reads a user supplied message')
async def ttsCommand(message, args):
    await message.channel.send("TTS is currently disabled due to reaching Google's TTS quota.")
    # filename = tts.synthesize_text(arg)
    # await music.play_file(ctx, filename, bot)

# Admin Commands

@CommandHandler(name='version', desc='Shows the currently runnning version of the bot.')
async def versionCommand(message, args):
    await message.channel.send(f'Bot is running version {version}.')

# Passive events (startup/etc.)

@CommandHandler(name='test')
async def testCommand(message, args):
    print(commands[0].name + commands[0].desc)

# commands.append(SimpleCommand(name='test', executor=testCommand))


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):

    # If message is from a bot, ignore
    if message.author.bot:
        return

    # If message begins with command prefix, process like a command
    if message.content[0] == command_prefix:

        args = (message.content[1:]).split()

        # Run any matching command executors to the arg0
        for c in commands:
            if c.name.lower() == args[0].lower():
                await c.executor(message, args)


    # Check for any other message related events

    for role in message.author.roles:
        if role.name.lower() == "horse": # User has role
            if random.randint(0, 20) == 0:
                await message.reply(random.choice(["ok gabe", "heard", "over", "good comms", "ratio + homeless", "who asked tho"]))

    

client.run(TOKEN)