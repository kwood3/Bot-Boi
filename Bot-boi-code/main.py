#!/usr/bin/python3
import sys

print(sys.version)
#print(sys.path)

import discord
from discord.ext import commands
from discord import Game
import asyncio
import time

prefix = "!"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    '''Outputs to console when connection is established'''
    print("")
    print("Bot ready!")
    print("Using discord.py version: " + discord.__version__)
    print("\n")
    await bot.change_presence(game=discord.Game(name="use " + prefix + "help"))

@bot.event
async def on_message_delete(message):
    ''' Called once a message is deleted '''
    author = message.author
    content = message.content
    channel = message.channel
    await bot.send_message(channel, '{}: {}'.format("Message deleted in ", channel, ":", author, content))

@bot.command(pass_context = True)
async def say(ctx, *args):
    '''User's input gets deleted, then the bot outputs it.'''
    msg = ' '.join(args)
    print(dir(ctx))
    await bot.delete_message(ctx.message)
    return await bot.say(msg)

@bot.command()
async def changeprefix(ctx, newPrefix):
    prefix=newPrefix
    await bot.say("prefix changed to " + args)

@bot.command()
async def beep():
    '''Checks if bot is responsive'''
    await bot.say("boop!")

bot.run("TOKEN")
