# bot.py
import os
import random
import discord
import discord_func
import api_func as api
from discord.ext import commands
from dotenv import load_dotenv

PREFIX = "!"

#user_ids = []
greetings = ['hello','hi','sup','howdy']
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

talking_ids = []

def user_exists(ID) :
    #check for user.id in usertable
    print('checking id:')
    print(ID)
    user_ids = discord_func.get_all_users()
    return ID in user_ids 

def is_user():
    async def predicate(ctx):
        return user_exists(ctx.author.id)
    return commands.check(predicate)

#return the message before this command
async def get_last_message(channel):
    messages = await channel.history(limit=2).flatten()
    return messages[1]

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guilds:\n'
            f'{guild.name}(id: {guild.id})'
        )

@bot.event
async def on_message(message):
    #TODO also add each word to database as they are said
    #TODO table Messages:  user, message, length, date/time, channel_name, server_id
    if message.author == bot.user:
        return
    
    last_message = await get_last_message(message.channel)
    print('Messaged received')
    print('Last message was: {msg}'.format(msg=last_message.content))
    discord_func.add_on_message(message.id, message.author.id, message.content, len(message.content), message.channel, message.created_at)
    
    if message.content[:len(PREFIX)] != PREFIX and user_exists(message.author.id):
        if message.content in greetings :
            # get default greeting
            x = discord_func.get_greeting(message.author.id)
            print(x)
            (m, e) = x
            if e == 1:
                await message.channel.send(m)
                return
            
            greeting = m
            if (greeting == ''):
                greeting = 'hello'
            await message.channel.send(greeting)
        elif len(message.content.split()) >= 2 and message.author.id in talking_ids:
            (garbage, category, sentiment, entity, entity_sentiment) = api.analyze(message.content)
            args = [message.author.id,category, sentiment, entity, entity_sentiment]
            print(args)
            response, e = discord_func.getResponse(args)
            await message.channel.send(response)
            
    
    await bot.process_commands(message)

@bot.command()
async def create_user(ctx):
    #call sql function

    m, e = discord_func.create_new_user(ctx.author.id, ctx.author.name, ctx.author.name,"hello")
    if (e == 1) :
        await ctx.send(m)
        return

    await ctx.send("created user for: " + ctx.message.author.name)
       # user_ids.append(ctx.author.id)

@bot.command()
#@is_user()
async def clear_user(ctx):
    
    m, e = discord_func.delete_user(ctx.author.id)
    if (e == 1) :
        await ctx.send(m)
        return
    
    await ctx.send("cleared user :" + ctx.message.author.name)
   

@bot.command()
async def set_greeting(ctx, *, arg):
    # call sql function
    e = discord_func.set_greeting(arg, ctx.author.id)
    if e[1] == 0 :
        await ctx.send("set default greeting to: " + arg)
    else:
        await ctx.send(e[1])

@bot.command()
async def set_prefered_name(ctx, *, arg):
    # call sql function
    e = discord_func.set_preferred_name(arg,ctx.author.id)
    if e[1] == 0 :
        await ctx.send("set default name to: " + arg)
    else :
        await ctx.send(e[0])

@bot.command()
async def meany(ctx):
    ##TODO pass correct line above
    #a call of "!meany" will cause this to take the line above and process it.
    print('entering command meany')
    last_message = await get_last_message(ctx.channel)
    print(last_message.content)
    print('got last message')
    discord_func.meany(last_message)

@bot.command()
async def mad(ctx):
    ## TODO pass correct swill here
    mesg = discord_func.mad()
    await ctx.send(mesg)

@bot.command()
async def wordsearch(ctx, *, arg):
    search = arg[2]
    messages, retval = discord_func.wordsearch(arg, ctx.author.id)
    
    if retval == 0 :
        await ctx.send("Users saying the word {word}: \n{list}".format(word=search, list=messages))
    else :
        await ctx.send(messages)

@bot.command()
async def longmessage(ctx, *, arg):
    tup, status = discord_func.longmessage(arg, ctx.author.id)
    users = tup[0]
    messages = tup[1]
    if status == 0 :
        await ctx.send("These are all of {user}'s messages with length longer than {len}: ".format(user=ctx.author.name, len=arg[2]))
        s = ""
        for i in range(len(messages)):
            s = s + (str)(users[i]) + ": " + (str)(messages[i]) + "\n"
        await ctx.send(s)  
    else :
        await ctx.send(status)


@bot.command()
async def talk(ctx):
    if ctx.author.id not in talking_ids :
        talking_ids.append(ctx.author.id)
        await ctx.send("IMU is now talking to "+ ctx.author.name + "!")
    else:
        await ctx.send("IMU is already talking!")
@bot.command()
async def shut_up(ctx):
    if ctx.author.id in talking_ids :
        talking_ids.pop(talking_ids.index(ctx.author.id))
        await ctx.send("IMU will shut up for "+ ctx.author.name + ":(")
    else :
        await ctx.send("IMU is already shut up :(")

@bot.command()
async def scrap(ctx):
    prev_mes_text = ""
    cur_mes = None
    cur_mes_text = ""
    aid = ctx.author.id
    async for message in ctx.channel.history(limit = None, oldest_first = False):
        m = message.content
        if (len(m) > 0 and m[0:1] == "!") or len(m) <= 1:
            continue
        if cur_mes == None: 
            cur_mes = message
        if message.author.id == cur_mes.author.id:
            cur_mes_text += ". " + message.content 
        else:
            if cur_mes.author.id == aid and len(prev_mes_text.split()) >= 2:
                #print("analyze: " + prev_mes_text)
                (x, category, sentiment, entity, entity_sentiment) = api.analyze(prev_mes_text)
                #insert into table
                #id*, response, category, sentiment, entity, entity sentiment, channel_name
                
                args = [aid,cur_mes_text, category, sentiment, entity, entity_sentiment, message.channel.name]
                discord_func.updateResponse(args)
                print(args)

            prev_mes = cur_mes
            prev_mes_text = cur_mes_text
            cur_mes = message
            cur_mes_text = message.content
            
        
                

bot.run(TOKEN)