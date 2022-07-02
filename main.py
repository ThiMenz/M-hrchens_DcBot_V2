# ----------------------------------------------------
# 			Created by Möhrchen [Thilo]  
#           ©2022 - All Rights Reserved
# ----------------------------------------------------

import srcomapi, srcomapi.datatypes as dt
import discord
import embeds
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

def ConvertStringToTime(strPar):
    parFloat = float(strPar)
    rest = round(parFloat % 60, 2)
    minutes = int(round((parFloat - rest) / 60, 0))
    hours = 0
    returnString0 = ""
    returnString1 = ""
    returnString2 = ""
    if minutes > 59:
        while minutes > 59:
            minutes -= 60
            hours += 1
        returnString0 = str(hours) + ":"

    if minutes < 10: returnString1 = "0" + str(minutes)
    else: returnString1 = "" + str(minutes)
    
    if rest < 10: returnString2 = ":0" + str(rest)
    else: returnString2 = ":" + str(rest)
        
    if rest * 100 % 10 == 0: return (returnString0 + returnString1 + returnString2 + "00")
    else: return (returnString0 + returnString1 + returnString2 + "0")
    


#=========Important Variables=========

api = srcomapi.SpeedrunCom(); api.debug = 1

listLimit = 30
categoryChoices = ["Any% NMG", "Any%", "Alt Ending", "All Collectibles", "No Shortcuts"]
bossChoices = ["Splitty", "Mr D.A.N.C.E", "Mama Squid", "Helpy", "Bartender", "Squid 1", "Squid 2"]
difficultyChoices = ["IE", "EE", "VE", "Easy"]
typingCategoryChoices = ["Any%NMG", "Any%", "AltEnding", "AllCollectibles", "NoShortcuts"]
typingBossChoices = ["Splitty", "MrDance", "MamaSquid", "Helpy", "Bartender", "Squid1", "Squid2"]
typingChapterChoices = ["ChapterA", "ChapterB", "ChapterC", "ChapterD", "ChapterE"]
typingOtherExtChoices = ["ChapterRelay", "Iaf", "DoubleTime", "Death%", "BlockMassacre", "MinimumKills"]


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
        
    @tasks.loop(seconds=60.0)
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
            await message.channel.send(embed=embeds.help_embed_1)
            await message.channel.send(embed=embeds.help_embed_2)
        
        if TestForAdvancedCommand(messageStr, prefix + 'wys') or TestForAdvancedCommand(messageStr, prefix + 'willyousnail'):

            #Try to get the Category and the Difficulty -->

            tempCategory = None #Is a string
        
            for cateCommand in typingCategoryChoices:
                if TestForAdvancedCommand(messageStr, cateCommand) and tempCategory == None:
                    tempCategory = categoryChoices[typingCategoryChoices.index(cateCommand)]
        
            typeOfCategory = 'Category' #Default Value = Category
            minusCommandSplitter = 0


            if tempCategory == None: #Test for ILs (Chapters)
                for chapterCommand in typingChapterChoices:
                    if TestForAdvancedCommand(messageStr, chapterCommand) and tempCategory == None:
                        tempCategory = chapterCommand
                        typeOfCategory = 'Chapter'

            if tempCategory == None: #Test for Other Extensions
                for otherExtCommand in typingOtherExtChoices:
                    if TestForAdvancedCommand(messageStr, otherExtCommand) and tempCategory == None:
                        tempCategory = otherExtCommand
                        typeOfCategory = 'OtherExtension'
                     
            if tempCategory == None: #It should be a Boss, 100% or a typo
                if '100%' in messageStr:  #It's 100%
                    tempCategory = '100%'
                    typeOfCategory = '100%'
                    minusCommandSplitter = 1
                else:
                    for bossCommand in typingBossChoices:
                        if TestForAdvancedCommand(messageStr, bossCommand) and tempCategory == None:
                            tempCategory = bossChoices[typingBossChoices.index(bossCommand)]
                            typeOfCategory = 'Boss'
                
                
            tempDifficulty = None #Is an integer
        
            if typeOfCategory != '100%':
                for diffCommand in difficultyChoices:
                    if TestForAdvancedCommand(messageStr, diffCommand) and tempDifficulty == None:
                        tempDifficulty = difficultyChoices.index(diffCommand)
          
            if tempCategory == None: 
                await message.channel.send("Please specify the catagory!")
                return

            await message.channel.send("Loading...")
            theLeaderboard = None
            cateString = ""
            searchApi = api.search(srcomapi.datatypes.Game, {"name": "Will You Snail?"})
            game = searchApi[0]
            cates = game.categories  
            levels = game.levels
            try:                                                    #Now try to get the Leaderboard from the right category -->
                if typeOfCategory == 'Category':
                    categoryInt = categoryChoices.index(tempCategory)
                    if categoryInt == 4: categoryInt = 10
                    cate = cates[categoryInt]
                    difficultyVar = cate.variables[0] 
                    cateString = "leaderboards/{}/category/{}?var-{}={}".format(game.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[tempDifficulty])
                elif typeOfCategory == 'Boss':
                    cate = cates[9]
                    bossVar = cate.variables[1]
                    difficultyVar = cate.variables[0]
                    cateString = "leaderboards/{}/category/{}?var-{}={}&var-{}={}".format(game.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[tempDifficulty], bossVar.id, list(bossVar.data["values"]["choices"].keys())[bossChoices.index(tempCategory)])
                elif typeOfCategory == '100%':
                    cate = cates[8]
                    cateString = "leaderboards/{}/category/{}".format(game.id, cate.id)
                elif typeOfCategory == 'Chapter':
                    difficultyVar = cates[tempDifficulty+4]
                    level = levels[typingChapterChoices.index(tempCategory)]  
                    cateVar = difficultyVar.variables[0]
                    cateString = "leaderboards/{}/level/{}/{}?var-{}={}".format(game.id, level.id, difficultyVar.id, cateVar.id, list(cateVar.data["values"]["choices"].keys())[0]) #This number at the end controls Any% or AllPuzzles
                elif typeOfCategory == 'OtherExtension':
                    game3 = searchApi[3]
                    cates3 = game3.categories
                    if typingOtherExtChoices.index(tempCategory) == 1:
                        iafArray = ["2", "25", "50", "75", "100", "1000"]
                        iafIndex = ""
                        for iafValue in iafArray:
                            if typingOtherExtChoices[1].lower() + iafValue in messageStr.lower():
                                iafIndex = iafValue
                        cate = cates3[1]
                        levelVar = cate.variables[0]
                        cateString = "leaderboards/{}/category/{}?var-{}={}".format(game3.id, cate.id, levelVar.id, list(levelVar.data["values"]["choices"].keys())[iafArray.index(iafIndex)])
                        minusCommandSplitter = 1
                    elif typingOtherExtChoices.index(tempCategory) == 3:
                        cate = cates3[3]
                        cateString = "leaderboards/{}/category/{}".format(game3.id, cate.id)
                        minusCommandSplitter = 1
                    else: 
                        cate = cates3[typingOtherExtChoices.index(tempCategory)]
                        difficultyVar = cate.variables[0]
                        cateString = "leaderboards/{}/category/{}?var-{}={}".format(game3.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[tempDifficulty])

                theLeaderboard = dt.Leaderboard(api, data=api.get(cateString))

                                                                    #Try to display the Leaderboard --> 

                if minusCommandSplitter == 1 and tempDifficulty != None:
                    await message.channel.send("This category hasn't a difficulty!")
                    return

                try:
                    tempNumbers = messageStr.replace(prefix, '').split(' ')[3 - minusCommandSplitter] 
                    if '-' in messageStr: #Command option 1: X-Y
                        try:
                            tempNumber1 = int(tempNumbers.split('-')[0])
                            tempNumber2 = int(tempNumbers.split('-')[1])
                        except Exception as e:
                            await message.channel.send("Please enter a valid number!")
                            return

                        if tempNumber2 > len(theLeaderboard.runs):
                            if len(theLeaderboard.runs) == 1:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entry!")
                            else:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entries!")
                            return
                    
                        if tempNumber2 - tempNumber1 >= 30:
                            await message.channel.send("Leaderboard index should be 30 or lower!")
                            return
                        elif tempNumber2 - tempNumber1 < 0:
                            await message.channel.send("Leaderboard index should be 1 or higher!")
                            return
                    
                        _complString = "The " + str(tempCategory) + " Leaderboard: \n"
                        for i in range(tempNumber1, tempNumber2 + 1):
                            _names = theLeaderboard.runs[i - 1]['run'].players
                            _time = ConvertStringToTime(float(theLeaderboard.runs[i - 1]['run'].times["primary_t"]))
                            _complString = _complString + str(i) + ". **" + str(_time) + "** by **" + str(_names[0].name) + "**"
                            arrayCount = 0
                            if len(_names) > 1:
                                for pla in _names:
                                    if arrayCount > 0:
                                        _complString = _complString + " and **" + pla.name + "**"
                                    arrayCount += 1

                            _complString = _complString + "\n"

                        
                        await message.channel.send(_complString)   
                        
                    else:               #Command option 2: X
                        try:
                            tempNumber1 = int(tempNumbers)
                        except Exception as e:
                            await message.channel.send("Please enter a valid number!")
                            return

                        if tempNumber1 > len(theLeaderboard.runs):
                            if len(theLeaderboard.runs) == 1:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entry!")
                            else:
                                await message.channel.send("This Leaderboard has only " + str(len(theLeaderboard.runs)) +  " entries!")
                            return
                
                        if tempNumber1 > 30:
                            await message.channel.send("Leaderboard index should be 30 or lower!")
                            return
                        elif tempNumber1 == 0:
                            await message.channel.send("The Leaderboard doesn't exist anymore! :(") #FlippyDolphin's Easter Egg
                            return 
                    
                        _complString = "The " + str(tempCategory) + " Leaderboard: \n"
                        for i in range(1, tempNumber1 + 1):
                            _names = theLeaderboard.runs[i - 1]['run'].players
                            _time = ConvertStringToTime(float(theLeaderboard.runs[i - 1]['run'].times["primary_t"]))
                            _complString = _complString + str(i) + ". **" + str(_time) + "** by **" + str(_names[0].name) + "**"
                            arrayCount = 0
                            if len(_names) > 1:
                                for pla in _names:
                                    if arrayCount > 0:
                                        _complString = _complString + " and **" + pla.name + "**"
                                    arrayCount += 1

                            _complString = _complString + "\n"
                    
                        await message.channel.send(_complString)   
                except Exception as e:
                    await message.channel.send("Please enter the number of runs you'd like display!")
            except Exception as e:
                await message.channel.send("Please specify the difficulty!")
            a = 0
            async for data in message.channel.history(limit=2):
                if a == 1:
                    await data.delete()
                a += 1

    
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
