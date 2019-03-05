#!/usr/bin/python3

# # # # # # # # # # # # # # # # # # #
#                                   #
#       bot boi v0.3 by Koby W      #
#                                   #
# # # # # # # # # # # # # # # # # # #

import os
import sys

clear = lambda: os.system('clear')
clear()

print("\n")
print("*--------------------------------------*")
print(sys.version)
print("Booting bot")
#print(sys.path)

import discord
from discord.ext import commands
from discord import Game
import asyncio
import time
import requests

prefix = "."
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    '''Outputs to console when connection is established'''
    print("\n")
    print("Bot ready!")
    print("Using discord.py version: " + discord.__version__)
    print("*---------------------------------------*")
    print("\n")
    await bot.change_presence(game=discord.Game(name="use .help"))

@bot.event
async def on_message_delete(message):
    ''' Called once a message is deleted '''
    author = message.author
    content = message.content
    channel = message.channel
    modlog = bot.get_channel("546771825347002376")
    #modlog = bot.get_channel("mod-log")
    await bot.send_message(modlog, " \"{}\" - deleted in {}, from {} .".format(content, channel, author))
    print("(Message delete) Channel sending report to: {}, from {}: {} ".format(modlog, author, content))

####                    ####
#                          #
# Requests Project Start:  #
#                          #
###                      ###

req = requests.get("https://api.fortnitetracker.com/v1") 

@bot.command(pass_context = True)
async def fnstats(message,ctx, user):
    ''' Lets you check a players fortnite stats - Currently only PC '''
    channel = message.channel
    fUserID = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/users/id?username="+user)
    UserIDD = fUserID.json()
    UUID = UserIDD['uid']
    print("User ID: " + UUID)

    fStats = requests.get("https://fortnite-public-api.theapinetwork.com/prod09/users/public/br_stats_v2?user_id="+UUID+"&platform=pc")
    print(fStats)
    fStatsD = fStats.json()

    kills= fStatsD['overallData']['defaultModes']['kills']
    wins = fStatsD['overallData']['defaultModes']['placetop1']
    gamesPlayed = fStatsD['overallData']['defaultModes']['matchesplayed']
    KD = kills / (gamesPlayed - wins)
    winRatio = wins / gamesPlayed

    embed = discord.Embed(title = user, description="User Stats", color=0x00ff00)
    embed.add_field(name="Wins", value=str(wins), inline = False)
    embed.add_field(name="Kills", value=str(kills), inline = False)
    embed.add_field(name="Games Played", value=str(gamesPlayed), inline = False)
    embed.add_field(name="K/D", value=str(KD), inline = False)
    embed.add_field(name="Win Percentage", value=str(winRatio), inline = False)

    await bot.send_message(channel, embed=embed)

@bot.command(pass_context = True)
async def weather(ctx, city):
    ''' Check the weather of your city '''
    channel = bot.get_channel('544887992892784695')
    #channel = message.channel
    key = "4639d5dd44237face893de6775526417"
    w = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+key)
    #print(w.url)
    wD = w.json()
    tempK = wD['main']['temp']
    tempC = round(tempK - 273)
    tempF = round(tempC + 32, 1)
    main = wD['weather'][0]['main']
    desc = wD['weather'][0]['description']
    humid = wD['main']['humidity']

    embed = discord.Embed(title = "Weather", description=city, color=0x00ff00)
    embed.add_field(name = main, value=desc, inline = False)
    embed.add_field(name = "Temperature", value=str(tempC)+"C°"+"\n"+str(tempF)+"F°", inline = False)
    embed.add_field(name = "Humidity", value=str(humid), inline = False)

    await bot.send_message(channel, embed=embed)

## Requests Project end ##

@bot.command(pass_context = True)
async def say(message, ctx, *args):
    '''User's input gets deleted, then the bot outputs it.'''
    channel = message.channel
    msg = ' '.join(args)
    #print(dir(ctx))
    await bot.delete_message(ctx.message) 
    return await bot.say(msg)

@bot.command(pass_context = True)
async def changeprefix(ctx, newPrefix):
    '''Currently under-development - used to change bot prefix '''
    prefix=newPrefix
    await bot.say("prefix changed to " + args)

@bot.command()
async def beep():
    ''' Checks if the bot is responsive '''
    await bot.say("boop!")

bot.run("NTQ0ODkwNzU4MTIyMTc2NTEy.D1GlSg.PLTBhJwqn_pFIpgVD2G3gBgHWpo")
