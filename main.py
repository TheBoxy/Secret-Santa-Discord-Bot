import discord
from discord.ext import commands
from collections import defaultdict
import GenerateNames
Token = 'ENTER TOKEN HERE'

client = commands.Bot(command_prefix='!')

santa_info = defaultdict(list)

    
@client.command()
async def start(ctx):
    santa_embed = discord.Embed(
        title = 'Secret Santa Bot',
        description = '`This is a bot meant to organize a Secret Santa Event. All you have to do is respond to the message with a "👍" if you want to participate. Then the bot will message you. You should respond with suggestions of gift ideas. Have fun`',
        color = discord.Colour.purple())
        
    santa_embed.set_footer(text='Made by Boxy')
    santa_embed.set_image(url='https://i0.wp.com/www.bestworldevents.com/wp-content/uploads/2017/11/Minions-Christmas-Gif.gif?fit=500%2C250')
    
    if ctx.channel.name != 'main':
        return
    msg = await ctx.send(embed=santa_embed)
    await msg.add_reaction('👍')
        
        
@client.command()
async def stop(ctx):
    if isinstance(ctx.channel.name, discord.channel.DMChannel):
        return
    responce = [len(num) for num in santa_info.values()]
    if 1 in responce:
        await ctx.send('Not everyone has responded')
    else:
        genData = GenerateNames.Generate(santa_info)
        
        for name, matched, url, message in genData:
            file = discord.File(url, filename='%s.gif'%(str(matched).strip('#0123456789')))
            
            user_embed = discord.Embed(
                title = '**You got** ' + str(matched),
                description = '**Their suggestions**:\n `%s`'%(str(message)),
                color= discord.Colour.red()
                )
            user_embed.set_image(url='attachment://%s'%('%s.gif'%(str(matched).strip('#0123456789'))))
            print(name, matched, url, message)
            await name.send(file=file, embed=user_embed)
        await ctx.send('SecretSanta.exe ended')
    
    
@client.command()
async def stats(ctx):
    if isinstance(ctx.channel.name, discord.channel.DMChannel):
        return
    for name, contents in santa_info.items():
        if len(contents) == 1:
            await ctx.send(name.mention + ' has not responded yet')
    responce = [len(num) for num in santa_info.values()]
    if 1 not in responce:
        await ctx.send('Everyone has responded')
    
@client.listen('on_message')
async def readmessage(message):
    if message.author == client.user or message.content[0] == '!' or not isinstance(message.channel, discord.channel.DMChannel):
        return 
    if len(santa_info[message.author]) == 1:
        santa_info[message.author].append(message.content)
        print(santa_info)
        await message.channel.send('Received your message 👍')

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user or reaction.emoji != '👍' or reaction.message.channel.name != 'main':
        return 
    if user not in santa_info:
        santa_info[user].append(await user.avatar_url_as(size=32).read())
        await user.send('Reply back with gift suggestions that will be sent to your Secret Santa (Must be written in one message)')
        

client.run(Token)
