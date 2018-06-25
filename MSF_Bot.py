import discord
from discord.ext import commands
from discord import Game
import asyncio

token='' #Insert server token here
U50_img = "https://i.imgur.com/q7fhFvz.png" #Ultimus lvl 50 raid map
U40_img = "https://i.imgur.com/kkSsMJj.png" #Ultimus lvl 40 raid map
U35_img = "https://i.imgur.com/Rc2CISl.png" #Ultimus lvl 35 raid map
U30_img = "https://i.imgur.com/5JlBEXN.png" #Ultimus lvl 30 raid map
DP60_img = "https://i.imgur.com/EJx3nG6.png" #Deadpool En Fuego raid map
TMZ_img = "" #Roster map with players timezones and typical availability
bot = commands.Bot(command_prefix='!')

async def mass_purge(ctx,ImgURL):
# Confirm user has rights and delete all messages in channel and repost image for appropriate raid
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
async def tmz(ctx):
    await mass_purge(ctx, TMZ_img)	
	
@bot.command(pass_context = True)
async def u30(ctx):
    await mass_purge(ctx, U30_img)	

@bot.command(pass_context = True)
async def u35(ctx):
    await mass_purge(ctx, U35_img)
	
@bot.command(pass_context = True)
async def u40(ctx):
    await mass_purge(ctx, U40_img)
	
@bot.command(pass_context = True)
async def u50(ctx):
    await mass_purge(ctx, U50_img)

@bot.command(pass_context = True)
async def dp60(ctx):
    await mass_purge(ctx, DP60_img)
	
@bot.command(pass_context = True)
async def info(ctx):
    embed = discord.Embed(title="MSF Bot", description="Reset MSF Strike Team Channels.", color=0xeee657)
    
    embed.add_field(name="Author", value="Klickachu")

    await bot.send_message(ctx.message.channel, embed=embed)

bot.remove_command('help')

@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title="MSF Raids", description="Reset MSF Strike Team Channels. List of commands are:", color=0xeee657)

    embed.add_field(name="!tmz", value="Clear timezone channel and repost timezone chart", inline=False)	
    embed.add_field(name="!u30", value="Ultimus Level 30", inline=False)	
    embed.add_field(name="!u35", value="Ultimus Level 35", inline=False)	
    embed.add_field(name="!u40", value="Ultimus Level 40", inline=False)	
    embed.add_field(name="!u50", value="Ultimus Level 50", inline=False)
    embed.add_field(name="!dp60", value="Deadpool En Fuego Level 60", inline=False)
    embed.add_field(name="!info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="!help", value="Gives this message", inline=False)

    await bot.send_message(ctx.message.channel, embed=embed)

bot.run(token)