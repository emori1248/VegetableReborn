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
version = "0.3.0"

LEFT_ARROW = '\U00002B05'
RIGHT_ARROW = '\U000027A1'

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

# number as page number (index starting at 1)
def getHelpPageEmbed(number):
    items_per_page = 5
    # If page out of bounds
    if number - 1 >= len(commands) / items_per_page or number <= 0:
        # Invalid Help Page
        return None

    emb = discord.Embed(title=f"Help Page {number}")
    for c in commands[(number-1)*items_per_page:(number*items_per_page)]:
        emb.add_field(name=c.name, value=c.description, inline=False)

    return emb
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

@CommandHandler(name='Image')
async def imageCommand(ctx, arg):
    if (await imagemod.addCenteredTextToImage(arg)):
        await ctx.send(file=discord.File(r'tmp/output.jpg'))
    else:
        await ctx.send(generic_error)
        print("ERROR: img dir empty for image command")

@CommandHandler(name='Help')
async def helpCommand(message, args):
    m = await message.channel.send(embed=getHelpPageEmbed(1))
    await m.add_reaction(LEFT_ARROW)
    await m.add_reaction(RIGHT_ARROW)

# TTS

@CommandHandler(name='TTS', desc='Reads a user supplied message')
async def ttsCommand(message, args):
    await message.channel.send("TTS is currently disabled due to reaching Google's TTS quota.")
    # filename = tts.synthesize_text(arg)
    # await music.play_file(ctx, filename, bot)

# Admin Commands

@CommandHandler(name='Version', desc='Shows the currently runnning version of the bot.')
async def versionCommand(message, args):
    await message.channel.send(f'Bot is running version {version}.')

@CommandHandler(name='Example')
async def versionCommand(message, args):
    pass

# Passive events (startup/etc.)

@CommandHandler(name='Test')
async def testCommand(message, args):
    async for member in message.guild.fetch_members(limit=50):
        print("{} {}".format(member.name, member.activity))


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if(reaction.emoji == LEFT_ARROW):
        # if help message
        title = reaction.message.embeds[0].title
        if 'Help' in title:
            # edit to next page
            index = title[len(title)-1]
            emb = getHelpPageEmbed(int(index)-1)
            if emb != None:
                await reaction.message.edit(embed=emb)
       
    if(reaction.emoji == RIGHT_ARROW):
        # if help message
        title = reaction.message.embeds[0].title
        if 'Help' in title:
            # edit to next page
            index = title[len(title)-1]
            emb = getHelpPageEmbed(int(index)+1)
            if emb != None:
                await reaction.message.edit(embed=emb)

@client.event
async def on_message(message):

    # If message is from a bot, ignore
    if message.author.bot:
        return

    # If message begins with command prefix, process like a command
    if message.content[0] == command_prefix:

        args = (message.content[1:]).split()

        # Run the first matching command executor to the arg0 of the command string
        for c in commands:
            if c.name.lower() == args[0].lower():
                await c.executor(message, args)
                return


    # Check for any other message related events

    for role in message.author.roles:
        if role.name.lower() == "horse": # User has role
            if random.randint(0, 20) == 0:
                await message.reply(random.choice(["ok gabe", "heard", "over", "good comms", "ratio + homeless", "who asked tho"]))

    

client.run(TOKEN)