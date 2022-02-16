import discord
import os

import shutil
import random
import json
import asyncio

from discord.ext import commands
import music
#import tts
import imagemod
# import calendarapi

import datetime
import websockets

from mcstatus import MinecraftServer

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = 'def dog:'

command_prefix = '~'
commands = []

intents = discord.Intents().all()
activity = discord.Game(name="Fuckers put me on AWS")

client = discord.Client(intents=intents, activity=activity)
generic_error = "Something broke, msg Potato (See console)."
version = "0.5.0"

CONFIG_PATH = "config.json"
CONFIG = None

WEBSOCKET_SERVER = None

LEFT_ARROW = '\U00002B05'
RIGHT_ARROW = '\U000027A1'
RED_X = '\U0000274C'

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

class Config():
    def __init__(self, path):
        self.path = path
        self.readFromFile(path)

    def readFromFile(self, path):
        f = open(path)
        data = json.load(f)
        self.data = data
        if self.data['debug']:
            print('Debug enabled')
    
    def getContentDict(self):
        return self.data['contentDict']
"""

TODO:
Auto-populate missing config file

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

# Fun commands

@CommandHandler(name='RTC', desc='This will make the problem worse, not fix it.')
async def rtcCommand(message, args):
    count = len(message.mentions)
    if count == 0:
        user = message.author
    elif count == 1:
        user = message.mentions[0]
    else:
        await message.channel.send('Too many mentions, usage: `~rtc <user>`')
        return

    if user.voice == None or user.voice.channel == None:
        await message.channel.send('User not in voice channel.')
        return

    async def move_user(idx, channnels, user):
        if idx == 0:
            return
        await user.move_to(channels[random.randint(0, len(channels)-1)])
        await asyncio.sleep(0.35)
        await move_user(idx-1, channels, user)

    channels = message.guild.voice_channels

    home = message.author.voice.channel
    await move_user(5, channels, user)
    await message.author.move_to(home)

@CommandHandler(name='Mcstatus', desc='Checks the status of the public Potato MC server.')
async def mcstatusCommand(message, args):
    server = MinecraftServer(CONFIG.data["mc_ip"], CONFIG.data["mc_port"])
    try:
        status = server.status()
        await message.channel.send("{0} players online (Version {1}), and replied in {2} ms".format(status.players.online, status.version.name, status.latency))
    except:
        await message.channel.send('Server is down.')

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

@CommandHandler(name='Beep')
async def helpCommand(message, args):
    m = await message.channel.send('do not react')
    await m.add_reaction(RED_X)

# TTS

@CommandHandler(name='TTS', desc='Reads a user supplied message (Disabled).')
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
    pass
    


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    # Add the websocket server to the list of coroutines
    asyncio.ensure_future(WEBSOCKET_SERVER.coroutine())

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

    if(reaction.emoji == RED_X):
        print('working')
        dmchannel = await user.create_dm()
        await dmchannel.send('https://cdn.discordapp.com/attachments/680290124797706260/680290416847093814/IMG_1176.JPG')
        await dmchannel.send('mmm tasty snnack yumm y ..')

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
                await message.reply(random.choice(CONFIG.getContentDict()['horse']))

    
class WebsocketServer:
    def __init__(self):
        pass

    def coroutine(self):
        async def handler(websocket, path):
            while True:
                message = await websocket.recv()
                # Respond to message accordingly
                query = json.loads(message)
                print(query)
                if query['TYPE'] == 'GETGUILDS':
                    guilds = []
                    async for guild in client.fetch_guilds(limit=150):
                        g = {
                            "id": guild.id,
                            "displayName" : guild.name,
                            'iconURL': str(guild.icon_url)
                        }
                        guilds.append(g)
                    response = {
                        "guilds": guilds
                    }
                    await websocket.send(json.dumps(response))

                if query['TYPE'] == 'GETTEXT':
                    tcs = []
                    g = client.get_guild(query['GUILD'])
                    for channel in g.text_channels:
                        tcs.append({
                            "id": str(channel.id),
                            "displayName" : channel.name
                        })
                    response = {
                        "textChannels": tcs
                    }
                    await websocket.send(json.dumps(response))
                
                if query['TYPE'] == 'SENDTEXT':
                    # Cast the channel id back to int, get the channel by its id, send the message
                    await client.get_channel(int(query['CHANNEL'])).send(query['MESSAGE'])
                

        return websockets.serve(handler, '127.0.0.1', 5678)



CONFIG = Config(CONFIG_PATH)
WEBSOCKET_SERVER = WebsocketServer()
client.run(TOKEN)