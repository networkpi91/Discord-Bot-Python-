#start of script
from dotenv import load_dotenv
import discord
from discord.ext import commands 
from discord.ext.commands import bot
from discord.utils import get
from datetime import datetime
from discord import FFmpegPCMAudio
from discord.ext.commands import has_permissions, MissingPermissions
import json
import time 
import os 
import sys
import subprocess
load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True 
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = '!',intents=intents)


####Prints in Console
class MyClient(discord.Client):
    async def setup_hook():
        print("The Bot is now ready to use!")
        
## END

###Notfiy Me the Bot is Online
@client.event 
async def on_ready(): 
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="NAME"))  
    z = client.get_channel(Channel Here)
    user_id = "53USER ID HERE"
    embed = discord.Embed(title= f"The  bot is online", timestamp = datetime.now(), color = discord.Color.green())
    await z.send(embed = embed)
    await z.send(f"<@{user_id}>")
    







##Fun Text Commands
@client.command()
async def hello(ctx):
    message = await ctx.message.delete() 
    await ctx.send("Hello! ")
    
    
@client.command()
async def goodbye(ctx):
    message = await ctx.message.delete()
    await ctx.send("Goodbye, I hope you have a good Day!")
    

### END


@client.command()
async def nade(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('AUDIO FILE NAME')
        player = voice.play(source)
        message = await ctx.message.delete()
        if (ctx.voice_client):
            time.sleep(4)
            await ctx.guild.voice_client.disconnect()
            
### End ####






### Staff Commands
###### DM USING THE BOT####
@client.command()
async def mess(ctx, user:discord.Member, *, message=None):
    embed = discord.Embed(title="You have recieved a Messege from Staff",timestamp = datetime.now(), color = discord.Color.blue())
    embed = embed.set_thumbnail(url="IMAGE")
    embed = embed.add_field(name="", value=message, inline=False)
    embed = embed.set_footer(text= "| Official System Message | Please do not reply to the bot, this is not monitored .")
    await user.send(embed=embed)
    message = await ctx.message.delete()



### Kick/BAN####
@client.command()

@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason = None):
    z = client.get_channel()
    message = await ctx.message.delete() 
    await member.kick(reason=reason)
    await z.send(f'User {member} has been kicked')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command!")



@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    z = client.get_channel()
    message = await ctx.message.delete() 
    await member.ban(reason=reason)
    await z.send(f'User {member} has been banned')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command!")


    
### End ###






## Developer Commands ##


####Sending Patch Notes
@client.command()
async def patch(ctx, *, message: str):
    
    user = ""
    z = client.get_channel()
    embed = discord.Embed(title= f"Patch Notes", timestamp = datetime.now(), color = discord.Color.blue())
    embed = embed.set_thumbnail(url="")
    embed = embed.add_field(name="Updates", value= message, inline=False)
    embed = embed.set_footer(text= "| Official System Message")
    message = await ctx.message.delete() 
    
    
    await z.send(embed = embed) 
###END###











## ADMIN FUNCTIONS | LOGS ##
#####  Messege LOGS ####


@client.event
async def on_message_delete(message):
    z = client.get_channel()
    embed = discord.Embed(title = f"{message.author}'s Message was Deleted", description = f"Deleted Message: {message.content}\nAuthor: {message.author.mention}\nLocation: {message.channel.mention}", timestamp = datetime.now(), color = discord.Color.red())
    await z.send(embed = embed)

@client.event
async def on_message_edit(before, after):
    z = client.get_channel()
    embed = discord.Embed(title = f"{before.author} Editied Their Messege", description = f"Before Message: {before.content}\nAfter: {after.content}\nAuthor: {before.author.mention}\nLocation: {before.channel.mention}", timestamp = datetime.now(), color = discord.Color.red())
    embed.set_author(name = before.name, icon_url = after.display_avatar)
    await z.send(embed = embed)

####### Roles Changes         
@client.event
async def on_member_update(before, after):
    z = client.get_channel()
    if len(before.roles) > len(after.roles):
        role = next(role for role in before.roles if role not in after.roles)
        embed = discord.Embed(title = f"{before}'s Role has been Removed", description = f"{role.name} was removed from {before.mention}", timestamp = datetime.now(), color = discord.Color.red())
    elif len(after.roles) > len(before.roles):
        role = next(role for role in after.roles if role not in before.roles)
        embed = discord.Embed(title = f"{before}'s Role has been Added", description = f"{role.name} was added from {before.mention}", timestamp = datetime.now(), color = discord.Color.red())
    elif before.nick != after.nick:
        embed = discord.Embed(title = f"{before}'s Nickname Changed", description = f"Before: {before.nick}\nAfter: {after.nick}", timestamp = datetime.now(), color = discord.Color.red())
    else:
        return
    embed.set_author(name = before.name, icon_url = after.display_avatar)
    
    await z.send(embed = embed)
    
        ####### Join/ Leave

@client.event
async def on_member_join(member):
    
    
        user= member.created_at    
        role = member.guild.get_role()
        z = client.get_channel()
        embed = discord.Embed(title= f" Joined ", color = discord.Color.green())
        embed.set_author(name = member, icon_url = member.display_avatar)
        embed = embed.add_field(name="Discord Name", value=member, inline=False)
        embed = embed.add_field(name="Account Age", value=user, inline=False)
        embed = embed.add_field(name="User Joined at:", value=datetime.now(), inline=False)
        
        
        await member.add_roles(role)
        await member.send("")
        await z.send(embed = embed)
        
        
@client.event
async def on_member_remove(member):
            user= member.created_at 
            z = client.get_channel()
            embed = discord.Embed(title= f" Left", timestamp = datetime.now(), color = discord.Color.red())
            embed.set_author(name = member, icon_url = member.display_avatar)
            
            embed.set_author(name = member, icon_url = member.display_avatar)
            embed = embed.add_field(name="Discord Name", value=member, inline=False)
            embed = embed.add_field(name="Account Age", value=user, inline=False)
            embed = embed.add_field(name="User Left at:", value=datetime.now(), inline=False)
            await z.send(embed = embed)  
## END###


## VARIOUS BOT FUNCTIONS
#^^^^AUDIO CLIPS^^^^^#

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I Left the Voice Channel!")
    else:
        await ctx.send("I am not in a voice channel!")#
## END ##




            
    
        


##### BOT TOKEN###################
client.run('TOKEN HERE')


