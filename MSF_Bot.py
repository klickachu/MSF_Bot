import discord
from discord.ext import commands
from discord import Game
from tinydb import TinyDB, Query, where
import asyncio

token='' #Insert server token here
U50_img = "https://i.imgur.com/q7fhFvz.png" #Ultimus lvl 50 raid map
U40_img = "https://i.imgur.com/kkSsMJj.png" #Ultimus lvl 40 raid map
U35_img = "https://i.imgur.com/Rc2CISl.png" #Ultimus lvl 35 raid map
U30_img = "https://i.imgur.com/5JlBEXN.png" #Ultimus lvl 30 raid map
DP60_img = "https://i.imgur.com/EJx3nG6.png" #Deadpool En Fuego raid map
TMZ_img = "" #Roster map with players timezones and typical availability
STR_img = "" #Strike Team Roster

# Setup DB, Default raid schedule is Day 1 03:00 & 23:00; Day 2 19:00; Day 3 15:00; Day 4 11:00; Day 5 07:00 UTC
# Raid rotation: 1 raid every 20h based on raid ticket availability
db = TinyDB('db.json')
db.purge()  #start with empty DB at each startup

#status tracks current raid '1' and next raid '2'
db.insert({'Key': 0, 'Type': 'Ultimus', 'Day': 1, 'Time': '03:00 UTC', 'Status': 1})
db.insert({'Key': 1, 'Type': 'Ultimus', 'Day': 1, 'Time': '23:00 UTC', 'Status': 2})
db.insert({'Key': 2, 'Type': 'Ultimus', 'Day': 2, 'Time': '19:00 UTC', 'Status': 0})
db.insert({'Key': 3, 'Type': 'Ultimus', 'Day': 3, 'Time': '15:00 UTC', 'Status': 0})
db.insert({'Key': 4, 'Type': 'Ultimus', 'Day': 4, 'Time': '11:00 UTC', 'Status': 0})
db.insert({'Key': 5, 'Type': 'Ultimus', 'Day': 5, 'Time': '07:00 UTC', 'Status': 0})

bot = commands.Bot(command_prefix='!')

async def mass_purge(ctx,ImgURL):
# Confirm user has rights and delete all messages in channel and repost image for appropriate raid
# Create Config role with manage messages permission, add your captains to it as well as the Bot
    author = ctx.message.author
    if not author.server_permissions.manage_messages:
	    return await bot.send_message(ctx.message.channel, "You need the **Config** role to use this command!")

    tmp = await bot.send_message(ctx.message.channel, 'Clearing messages...')
    async for msg in bot.logs_from(ctx.message.channel):
        await bot.delete_message(msg)

    await bot.send_message(ctx.message.channel, ImgURL)

 
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	await bot.change_presence(game=Game(name="!help"))

@bot.command(pass_context = True)
async def purge(ctx, number : int):
# Confirm user has rights and delete messages in channel
    author = ctx.message.author
    if not author.server_permissions.manage_messages:
	    return await bot.send_message(ctx.message.channel, "You need the **Config** role to use this command!")

    deleted = await bot.purge_from(ctx.message.channel, limit = number)
    await bot.send_message(ctx.message.channel, 'Deleted {} message(s)'.format(len(deleted)))

@bot.command(pass_context = True)
async def str(ctx):
#Clear channel and post Strike Team Roster
    await mass_purge(ctx, STR_img)
	
@bot.command(pass_context = True)
async def tmz(ctx):
#Clear channel and post Timezone roster 
    await mass_purge(ctx, TMZ_img)	
	
@bot.command(pass_context = True)
async def u30(ctx):
#Clear channel and post Ultimus lvl 30 raid map
    await mass_purge(ctx, U30_img)
    await bot.send_message(ctx.message.channel, STR_img)	

@bot.command(pass_context = True)
async def u35(ctx):
#Clear channel and post Ultimus lvl 35 raid map
    await mass_purge(ctx, U35_img)
    await bot.send_message(ctx.message.channel, STR_img)

@bot.command(pass_context = True)
async def u40(ctx):
#Clear channel and post Ultimus lvl 40 raid map
    await mass_purge(ctx, U40_img)
    await bot.send_message(ctx.message.channel, STR_img)

@bot.command(pass_context = True)
async def u50(ctx):
#Clear channel and post Ultimus lvl 50 raid map
    await mass_purge(ctx, U50_img)
    await bot.send_message(ctx.message.channel, STR_img)

@bot.command(pass_context = True)
async def dp60(ctx):
#Clear channel and post Deadpool lvl 60 raid map
    await mass_purge(ctx, DP60_img)
    await bot.send_message(ctx.message.channel, STR_img)

@bot.group(pass_context = True)
async def raid(ctx):
#Print out Raid Schedule
    RaidCurrent = db.get(where("Status") ==1)
    RaidNext = db.get(where("Status") == 2)
    embed = discord.Embed(title="Raid Schedule", description="Day 1 03:00 & 23:00; Day 2 19:00; Day 3 15:00; Day 4 11:00; Day 5 07:00 UTC", color=0xeee657)
    embed.add_field(name="Current Raid", value="{Type} {Time}".format(**RaidCurrent))
    embed.add_field(name="Next Raid", value="{Type} {Time}".format(**RaidNext))

    await bot.send_message(ctx.message.channel, embed=embed)

@raid.command(pass_context = True)
async def inc(ctx):
#Increment Raid Schedule and display updates
    author = ctx.message.author
    if not author.server_permissions.manage_messages:
        return await bot.send_message(ctx.message.channel, "You need the **Config** role to use this command!")

    RaidCurrent = db.get(where("Status") == 2)
    #Clear old raid and set new raid status
    Raid = Query()
    db.update({'Status': 0}, Raid.Status == 1)
    db.update({'Status': 1}, Raid.Status == 2)
    RaidKey = int("{Key}".format(**RaidCurrent))+1
    if RaidKey == 6:
        db.update({'Status': 2}, Raid.Key == 0)
    else:
        db.update({'Status': 2}, Raid.Key == RaidKey)
    RaidNext = db.get(where("Status") == 2)
    embed = discord.Embed(title="Updated Raid Schedule", description="", color=0xeee657)
    embed.add_field(name="Current Raid", value="{Type} {Time}".format(**RaidCurrent))
    embed.add_field(name="Next Raid", value="{Type} {Time}".format(**RaidNext))

    await bot.send_message(ctx.message.channel, embed=embed)
	
@bot.command(pass_context = True)
async def info(ctx):
    embed = discord.Embed(title="MSF Bot", description="Reset MSF Strike Team Channels.", color=0xeee657)
    embed.add_field(name="Author", value="Klickachu")

    await bot.send_message(ctx.message.channel, embed=embed)

bot.remove_command('help')

@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title="MSF Raids", description="Reset MSF Strike Team Channels. List of commands are:", color=0xeee657)

    embed.add_field(name="!purge #", value="Delete # of messages from current channel", inline=False)
    embed.add_field(name="!str", value="Post Strike Team Roster", inline=False)	
    embed.add_field(name="!tmz", value="Clear timezone channel and repost timezone chart", inline=False)
    embed.add_field(name="!raid", value="Print out the Raid Schedule", inline=False)
    embed.add_field(name="!raid inc", value="Increment the Raid Schedule", inline=False)
    embed.add_field(name="!u30", value="Ultimus Level 30", inline=False)	
    embed.add_field(name="!u35", value="Ultimus Level 35", inline=False)	
    embed.add_field(name="!u40", value="Ultimus Level 40", inline=False)	
    embed.add_field(name="!u50", value="Ultimus Level 50", inline=False)
    embed.add_field(name="!dp60", value="Deadpool En Fuego Level 60", inline=False)
    embed.add_field(name="!info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="!help", value="Gives this message", inline=False)

    await bot.send_message(ctx.message.channel, embed=embed)

bot.run(token)
