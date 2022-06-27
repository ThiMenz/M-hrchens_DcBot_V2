# ----------------------------------------------------
# 			Created by Möhrchen [Thilo]  
#           ©2022 - All Rights Reserved
# ----------------------------------------------------

import srcomapi, srcomapi.datatypes as dt
import discord
from discord.ext import tasks, commands
from discord.utils import get
from webserver import keep_alive
import os
import random
from datetime import datetime
import calendar
import time



def TestForAdvancedCommand(messagePar, checkPar):
    if checkPar.lower() in messagePar.lower(): return True
    
    return False
    


#=========Important Variables=========

viableCommandChannels = ['bot-commands']

prefix = "m!"
intents = discord.Intents.all()
discord.member = True
client = commands.Bot(command_prefix="m!",intents = intents)
                            
activeGuildId = 988336667146481725 
categoryOfVoiceChannelsID = 989190438898532422
createVoiceChannelVCID = 988336667591073843
memberRoleID = 988497403571228724
welcomeChannelID = 988690177071390761
welcomeChannel = None

theGuild = None
categoryOfVoiceChannels = None
memberRole = None

nicePeopleArray = ["Meister Möhre#1623"]
godDamnNicePeopleArray = ["Meister Möhre#1623"]

listOfBotStatus = ['m!help']
activeBotStatus = 0

currentTemporaryVoiceChannels = [0]
currentTemporaryVoiceChannelLeader = [0]
lastTemporaryVoiceChannelRenames = [0]
#=========Discord Client=========



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        global theGuild 
        theGuild = await client.fetch_guild(activeGuildId)
        global categoryOfVoiceChannels
        categoryOfVoiceChannels = client.get_channel(categoryOfVoiceChannelsID)
        global memberRole
        memberRole = get(theGuild.roles, id=memberRoleID)
        global welcomeChannel
        welcomeChannel = client.get_channel(welcomeChannelID)
        print(memberRole)
        self.Change_Status.start()
        
    @tasks.loop(seconds=30.0)
    async def Change_Status(self):
        global activeBotStatus
        await self.change_presence(activity=discord.Game(name=listOfBotStatus[activeBotStatus]))
        if activeBotStatus < len(listOfBotStatus) - 1: activeBotStatus += 1
        else: activeBotStatus = 0
        
    async def on_voice_state_update(self, member, before, after):
    
        if after.channel == None and before.channel == None: return
            
        if before.channel != None:
            if before.channel.id in currentTemporaryVoiceChannels:
                if len(before.channel.members) == 0:
                    currentTemporaryVoiceChannelLeaderTempObj = currentTemporaryVoiceChannelLeader[(currentTemporaryVoiceChannels.index(before.channel.id))]
                    lastTemporaryVoiceChannelRenames.remove(lastTemporaryVoiceChannelRenames[(currentTemporaryVoiceChannels.index(before.channel.id))])
                    currentTemporaryVoiceChannelLeader.remove(currentTemporaryVoiceChannelLeaderTempObj)
                    currentTemporaryVoiceChannels.remove(before.channel.id)
                    await before.channel.delete()
                
        if after.channel == None: return
        if after.channel.id != createVoiceChannelVCID: return
        
        roomName = ""
        if member.nick == None:
            roomName = member.name + "'s Raum"
        else:
            roomName = member.nick + "'s Raum"
        
        channel = await theGuild.create_voice_channel(roomName, category=categoryOfVoiceChannels)
        currentTemporaryVoiceChannels.append(channel.id)
        currentTemporaryVoiceChannelLeader.append(member.id)
        lastTemporaryVoiceChannelRenames.append(0)
        await member.move_to(channel)
        
        
    async def on_message(self, message):

        if message.channel.type == discord.ChannelType.private: return
      
        if message.type is discord.MessageType.new_member:
            newMemberID = message.author.mention.replace("<@", "").replace(">", "")
            theMember = await theGuild.fetch_member(newMemberID)
            await theMember.add_roles(memberRole)
            embed = discord.Embed(
            title = 'Herzlich Willkommen auf dem Discord von Möhrchen!',
            description = 'Viel Spaß dir hier, mach bitte aber kein Unsinn :)',
            colour = discord.Colour.blue()
            )
            await welcomeChannel.send("Guten Tag, " + theMember.mention + "!", embed=embed)
            return
        
        prefix = 'm!'
        messageStr = '{0.content}'.format(message)
        
        if message.author.bot: return
        
        if "raumverwaltung" in str(message.channel.name):
            try:
                if str(prefix + 'usercount') in messageStr.lower() or str(prefix + 'uc') in messageStr.lower():
                    if not message.author.voice.channel.id in currentTemporaryVoiceChannels: return
                    try:
                        await message.author.voice.channel.edit(user_limit=int(messageStr.lower().replace(str(prefix + 'usercount '), "").replace(str(prefix + 'uc '), "")))
                    except:
                        print("Roommanagement-Mistake")
                    
                
                if str(prefix + 'name') in messageStr.lower():
                    if not message.author.voice.channel.id in currentTemporaryVoiceChannels: return
                    timeStampFromRoomRename = lastTemporaryVoiceChannelRenames[(currentTemporaryVoiceChannels.index(message.author.voice.channel.id))]
                    if int(time.time()) - timeStampFromRoomRename < 1:
                        tempDmChannel = await message.author.create_dm()
                        await tempDmChannel.send(content="Du kannst diesen Command erst wieder <t:" + str(timeStampFromRoomRename) + ":R> benutzen!")  
                        await message.delete()
                        return
                    try:
                        lastTemporaryVoiceChannelRenames[(currentTemporaryVoiceChannels.index(message.author.voice.channel.id))] = int(time.time() + 301)
                        await message.author.voice.channel.edit(name=messageStr.replace(str(messageStr[0] + messageStr[1] + messageStr[2] + messageStr[3] + messageStr[4] + messageStr[5] + messageStr[6]), ""))
                    except:
                        print("Roommanagement-Mistake")
            except:
                print("Roommanagement-Mistake")
                
            await message.delete()   
            
        if len(messageStr) < 2: return
       




      
        if messageStr[0] != 'm' or messageStr[1] != '!' :
            if messageStr[0] == 'M' and messageStr[1] == '!':
                prefix = 'M!'
            else:
                return #when no prefix in a message is detected nothing should happen
        
                
        
        
        if str(message.author) not in nicePeopleArray and not str(message.channel.name) in viableCommandChannels: return #when the author isn't included in the Array nothing happens


        if str(prefix + 'test') in messageStr.lower():
            theId = int(messageStr.replace(str(prefix + 'test'), ""))
            print(theId)
            theChannel = client.get_channel(theId)
            print(theChannel)
            
            
        if str(prefix + 'reaction') in messageStr.lower():
            if str(message.author) not in godDamnNicePeopleArray: return
            a = 0
            tempData = [''] * 6
            async for data in message.channel.history(limit=6):
                tempData[a] = str(data.content)
                await data.delete()
                a += 1
                
            roleFile = open("Roles.txt", "r")
            
            roleFileRL = roleFile.readlines()
            roleFile.close()


            embed = discord.Embed(
            title = tempData[1],
            description = tempData[0].replace(prefix + 'reaction', ''),
            colour = discord.Colour.blue()
            )
            
            if tempData[3] != "-":
                embed.set_image(url=tempData[3])
            
            theNewMessage = await message.channel.send(tempData[2], embed=embed)

            roleFileW = open("Roles.txt", "w")
            for ln in roleFileRL:
                roleFileW.write(ln)
            roleFileW.write(str(tempData[5]) + "~" + str(theNewMessage.id) + "\n")

            try:
                
                await theNewMessage.add_reaction(str(tempData[4]))
            except:
                print("Entered smth wrong!")
            
            
            
            
        #===Clear Command (m!clear X)===

        if str(prefix + 'clear') in messageStr.lower():
            if str(message.author) not in godDamnNicePeopleArray: return 
            try:
                async for m in message.channel.history(limit=1 + int(messageStr.replace(str(prefix + 'clear '), ''))):
                    await m.delete()
                return
            except:
                print('m!clear Error!')



        #===Embed Command (m!embed)===
        
        if TestForAdvancedCommand(messageStr, str(prefix + 'embed')):                 
            if str(message.author) not in godDamnNicePeopleArray: return
            howMuchFields = int(str(message.channel.last_message.content).replace(str(prefix + 'embed '), ""))
            
            historyCount = 5 + (howMuchFields * 3) + 4
            
            a = 0
            tempData = [''] * historyCount
            async for data in message.channel.history(limit=historyCount):
                tempData[a] = str(data.content)
                await data.delete()
                a += 1
            
            embed = discord.Embed(
            title = tempData[2],
            description = tempData[1],
            colour = discord.Colour.blue(),
            timestamp = datetime.now()
            )
            for i in range(howMuchFields):
                currentInlineBool = False
                if "true" in tempData[historyCount - 9 - (i * 3)]: 
                    currentInlineBool = True
                embed.add_field(name=tempData[historyCount - 7 - (i * 3)], value=tempData[historyCount - 8 - (i * 3)], inline=False)  
                
            if tempData[historyCount - 5] != "-":
                embed.set_author(name=tempData[historyCount - 5], icon_url=tempData[historyCount - 6])
            if tempData[historyCount - 4] != "-":
                embed.set_thumbnail(url=tempData[historyCount - 4])
            if tempData[historyCount - 3] != "-":
                embed.set_image(url=tempData[historyCount - 3])
            
            whichMessage = ''
            if tempData[historyCount - 2] != "-":
                whichMessage = tempData[historyCount - 2]
            
            _theChannelID_ = int(tempData[historyCount - 1])
            channelInWhichTheEmbedWillBePosted = client.get_channel(_theChannelID_)
            print(channelInWhichTheEmbedWillBePosted)
            await channelInWhichTheEmbedWillBePosted.send(whichMessage, embed=embed)
        #===Help Command (m!Help)==

        if TestForAdvancedCommand(messageStr, str(prefix + 'help')): 
            embed = discord.Embed(
            title = 'Help',
            description = 'This is a list of the commands: \n ',
            colour = discord.Colour.blue()
            )
            #embed.add_field(name='m!src X', value='Shows top X runs.', inline=True)
            #embed.set_thumbnail(url='https://www.speedrun.com/themeasset/2woqj208/logo?v=ae9623c')
            await message.channel.send(embed=embed)
        


    
    #===Reaction Add===


          
    async def on_raw_reaction_add(self, payload):
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if not message.author.bot: return 
        user = payload.member
        tempRole = None
        roleTxt = open("Roles.txt", "r")
        roleTxtRl = roleTxt.readlines()
        roleTxt.close()
        for ln in roleTxtRl:
            if "~" in ln:
                if int(ln.split('~')[1]) == int(payload.message_id):  
                    tempRole = discord.utils.get(user.guild.roles, name=str(ln.split('~')[0])) 

        if user.bot: return
        await user.add_roles(tempRole)


      
    #===Reaction Remove===  
      
    async def on_raw_reaction_remove(self, payload): 
        #At the Reaction-Remove-Function he returns "payload.member = None", that's why the program needs to fetch the member
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)  
        if not message.author.bot: return 
        guild = client.get_guild(payload.guild_id)
        user = await(guild.fetch_member(payload.user_id))
        if user.bot: return
        tempRole = None
        roleTxt = open("Roles.txt", "r")
        roleTxtRl = roleTxt.readlines()
        roleTxt.close()
        for ln in roleTxtRl:
            if "~" in ln:
                if int(ln.split('~')[1]) == int(payload.message_id):  
                    tempRole = discord.utils.get(user.guild.roles, name=str(ln.split('~')[0])) 
        if user.bot: return
        await user.remove_roles(tempRole)
        

#Start the Discord Bot -->

client = MyClient()
keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
