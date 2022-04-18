import discord
import time

bot = discord.Client()

file = open("shortcuts.txt","r")

colours = []
instances = []
standard_life=10000;

for i in file:
    X = []
    if i[-1]=="\n":
        i = i[:-1]
    X = i.split(";")
    if(X[0][:2]=="0x"):
        colours.append(X)

def islink(str):
    if(str.startswith("https://") or str.startswith("http://")):
        return True
    if(str.endswith(".png") or str.endswith(".gif")  or str.endswith(".jpg")  or str.endswith(".jpeg")):
        return True
    return False

def spliter(str):
    if "```" in str:
        outside = True
        T = []
        x = ""
        index = 0
        while index < len(str):
            if str[index]==";" and outside:
                T.append(x)
                x = ""
            elif str[index:][:3]=="```":
                if outside:
                    outside = False
                else:
                    outside = True
                x+=str[index]
            else:
                x+=str[index]
            index+=1
        T.append(x)
        return T
                    
    else:
        return str.split(";")

def fixlink(str):
    if(str.startswith("https://") or str.startswith("http://")):
        return str
    else:
        return "http://"+str
    
def iscolour(str):
    if (str.startswith("0x") and len(str)==8):
        return True
    return False

def sorter(T):
    if(len(T)>1 and (islink(T[0]) or iscolour(T[0]))):
       x = T[1]
       T[1] = T[0]
       T[0] = x
    return T

def valid_colour(x):
    if not len(x)==8:
        return False
    try:
        z = int(x,16)
        if 0<z<16777215:
            return True
        else:
            return False
    except:
        return False

def filter(T,message):
    for i in range(len(T)):
        while len(T[i])>0 and T[i][0]==" ":
            T[i] = T[i][1:]
        if T[i]=="/me":
            T[i]=str(message.author.avatar_url)
        elif T[i]=="/bot":
            T[i]=str(bot.user.avatar_url)
        elif T[i]=="/rickroll":
            T[i]="https://i.pinimg.com/originals/75/98/d1/7598d103a735d5568964e4967e42823d.gif"
        if T[i][:2]=="0x" and not valid_colour(T[i]):
            if T[i].lower() == "0xffffff":
                T[i] = "0xFFFFFE"
            for j in colours:
                if T[i]==j[0]:
                    T[i]=j[1]
            if not valid_colour(T[i]):
                T = [["If you tried to do 0xName_Colour \n(like 0xGray)","Your Name_Colour have not been found please check channel #colours on ***The Embeders*** server"],["If you tried to do 0xHex_Code \n(like 0xFF0000)\n ","Make sure that your code is in the correct format (6 digit hexadecimal starting from 0x) or use the predefined colours."]]
                raise ArgumentException("Colour not found",T)
    T = sorter(T)
    return T

def find(author,skip=0):
    global instances
    for instance in instances:
        if instance.master == author and skip==0:
            return [instance]
        elif instance.master == author:
            skip-=1
    return []

def recycle():
    global instances
    if len(instances)<20:
        return;
    
    i=0
    count = 0
    while i<len(instances):
        if instances[i].to_recycle():
            instances.pop(i)
            count+=1
        else:
            i+=1

    print("Currently running: ",len(instances)," (-"+str(count)+")")

async def getMessage(channel,mess_id):
    async for message in channel.history():
        if (message.id == mess_id):
            return message
    return None
    
class ArgumentException(Exception):
    def __init__(self,message,correct=[]):
        self.message = message
        self.correct = correct

    def table(self):
        return self.correct

    def message(self):
        return self.message

class Embed():
    def __init__(self,T,message,life=None):
        self.master = message.author.id
        if life==None:
            self.lifetime = standard_life
        else:
            self.lifetime = life
        self.life = int(time.time())+self.lifetime
        self.ch = message.channel
        if(len(T)==0) or (len(T)==1 and T[0]==""):
            self.e = discord.Embed(title='⠀')
        elif(len(T)==1):
            if valid_colour(T[0]):
                self.e = discord.Embed(title='⠀',colour=int(T[0],16))
            else:
                self.e = discord.Embed(title=T[0])
        elif(len(T)==2):
            if valid_colour(T[1]):
                self.e = discord.Embed(title=T[0],colour=int(T[1],16))
            else:
                T = [['Title','*not required*'],['Colour','*not required*\nMUST start with 0x and be a valid six digit hex code or a predified colour (check #shortcuts on ***The Embeders*** server)']]
                raise ArgumentException('Out of two arguments, none of them are valid colours.',T)
        else:
            T = [['Title','*not required*'],['Colour','*not required*\nMUST start with 0x and be a valid six digit hex code or a predified colour (check #shortcuts on ***The Embeders*** server)']]
            raise ArgumentException('Invalid amount of arguments (must be 0, 1 or 2)',T)
        if not(message.author.id == 362947029800058881):
            (self.e).set_footer(text="© Patryk Kuchta 2021\nRegister today to get rid or modify the footer!");
        
    def author(self,T):
        if(len(T)==0) or (len(T)==1 and T[0]==""):
            (self.e).set_author(name="")
        elif len(T)==1 and not T[0]=="":
            (self.e).set_author(name=T[0])
        elif(len(T)==2):
            if(islink(T[1])):
                T[1]=fixlink(T[1])
                (self.e).set_author(name=T[0],icon_url=T[1])
            else:
                T = [['Name','*required*'],['Image','*not required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
                raise ArgumentException('Out of two arguments, none of them are vaild image URLs',T)
        else:
            T = [['Name','*required*'],['Image','*not required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
            raise ArgumentException('Invalid amount of arguments (must be 1 or 2, or 0 if you want to clear it)',T)

    def footer(self,T):
        if(len(T)==0) or (len(T)==1 and T[0]==""):
            (self.e).set_footer(text="")
        elif len(T)==1 and not T[0]=="":
            (self.e).set_footer(text=T[0])
        elif(len(T)==2):
            if(islink(T[1])):
                T[1]=fixlink(T[1])
                (self.e).set_footer(text=T[0],icon_url=T[1])
            else:
                T = [['Text','*required*'],['Image','*not required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
                raise ArgumentException('Out of two arguments, none of them are vaild image URLs',T)
        else:
            T = [['Text','*required*'],['Image','*not required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
            raise ArgumentException('Invalid amount of arguments (must be 1 or 2, or 0 if you want to clear it)',T)

    def image(self,T):
        if(len(T)==0) or (len(T)==1 and T[0]==""):
            (self.e).set_image(url="")
        elif len(T)==1 and not T[0]=="":
            if(islink(T[0])):
                T[0]=fixlink(T[0])
                (self.e).set_image(url=T[0])
            else:
                T = [['Image','*required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
                raise ArgumentException('The argument is not a vaild image URLs',T)
                
        else:
            T = [['Image','*required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
            raise ArgumentException('Invalid amount of arguments (must be 1, or 0 if you want to clear it)',T)

    def thumbnail(self,T):
        if(len(T)==0) or (len(T)==1 and T[0]==""):
            (self.e).set_image(url="")
        elif len(T)==1 and not T[0]=="":
            if(islink(T[0])):
                T[0]=fixlink(T[0])
                (self.e).set_thumbnail(url=T[0])
            else:
                T = [['Image','*required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
                raise ArgumentException('The argument is not a vaild image URLs',T)
        else:
            T = [['Image','*required*\nMUST be working URLs with of an image (check if the url ends with gif, png or jpg) or a predefined refence to link (check #shortcuts on ***The Embeders*** server)']]
            raise ArgumentException('Invalid amount of arguments (must be 1, or 0 if you want to clear it)',T)

    def addf(self,T):
        if(len(T)==2):
            (self.e).add_field(name=T[0], value=T[1])
        elif(len(T)==3):
            (self.e).add_field(name=T[0], value=T[1],inline=False)
        else:
            T = [['Header','*required*'],['Body','*required*'],['Inline','*not required*\nIf you want to display this field in line add any argument (example (...);1)']]
            raise ArgumentException('Invalid amount of arguments (must be 2 or 3)',T)
        
    def setf(self,T):
        if(len(T)==3):
            try:
                (self.e).set_field_at(index=int(T[0])-1,name=T[1],value=T[2])
            except Exception as error:
                T = [['Index','*required*\nMUST be a number and must be an index within the current list (counting from 1)'],['Header','*required*'],['Body','*required*'],['Inline','*not required*\nIf you want to display this field in line add any argument (example (...);1)']]
                raise ArgumentException('Provided index is invalid',T)
        elif(len(T)==4):
            try:
                (self.e).set_field_at(index=int(T[0])-1,name=T[1],value=T[2],inline=False)
            except:
                T = [['Index','*required*\nMUST be a number and must be an index within the current list (counting from 1)'],['Header','*required*'],['Body','*required*'],['Inline','*not required*\nIf you want to display this field in line add any argument (example (...);1)']]
                raise ArgumentException('Provided index is invalid',T)
        else:
            T = [['Index','*required*\nMUST be a number and must be an index within the current list (counting from 1)'],['Header','*required*'],['Body','*required*'],['Inline','*not required*\nIf you want to display this field in line add any argument (example (...);1)']]
            raise ArgumentException('Invalid amount of arguments (must be 3 or 4)',T)

    def insf(self,T):
        if(len(T)==3):
            try:
                (self.e).insert_field_at(index=int(T[0])-1,name=T[1],value=T[2])
            except:
                T = [['Index','*required*\nMUST be a number and must be an index within the current list (counting from 1)'],['Header','*required*'],['Body','*required*'],['Inline','*not required*\nIf you want to display this field in line add any argument (example (...);1)']]
                raise ArgumentException('Provided index is invalid',T)
        elif(len(T)==4):
            try:
                (self.e).insert_field_at(index=int(T[0])-1,name=T[1],value=T[2])
            except:
                T = [['Index','*required*\nMUST be a number and must be an index within the current list (counting from 1)'],['Header','*required*'],['Body','*required*'],['Inline','*not required*\nIf you want to display this field in line add any argument (example (...);1)']]
                raise ArgumentException('Provided index is invalid',T)
        else:
            T = [['Index','*required*\nMUST be a number and must be an index within the current list (counting from 1)'],['Header','*required*'],['Body','*required*'],['Inline','*not required*\nIf you want to display this field in line add any argument (example (...);1)']]
            raise ArgumentException('Invalid amount of arguments (must be 3 or 4)',T)


    def delf(self,T):
        if len(T)==1 and not T[0]=="":
            try:
                (self.e).insert_field_at(index=int(T[0])-1,name=T[1],value=T[2])
            except:
                T = [['Index',"*not required*\nMUST be a number and must be an index within the current list (counting from 1)\n***If you don't provide the index it will delete all the fields***"]]
                raise ArgumentException('Provided index is invalid',T)
        elif (len(T)==0) or (len(T)==1 and T[0]==""):
            (self.e).clear_fields()
        else:
            T = [['Index',"*not required*\nMUST be a number and must be an index within the current list (counting from 1)\n***If you don't provide the index it will delete all the fields***"]]
            raise ArgumentException('Invalid amount of arguments (must be 0 or 1)',T)
        
    async def send(self,channel=None):
        if channel==None:
            await (self.ch).send(embed=self.e)
        else:
            await channel.send(embed=self.e)

    async def edit(self,message):
        await message.edit(embed=self.e)

    async def start(self):
        pass

    async def check(self):
        pass

    async def send_int(self,channelid,guildid):
        for guild in bot.guilds:
            if guild.id == guildid:
                for channel in guild.channels:
                    if channel.id == channelid:
                        await self.send(channel)

    def extend(self):
        self.life = int(time.time())+self.lifetime

    def master(self):
        return self.master

    def to_recycle(self):
        if int(time.time())>self.life:
            return True
        return False

    def length(self):
        return len((self.e).fields)

    async def id(self):
        pass

class Poll(Embed):
    def __init__(self,T,message):
        Embed.__init__(self,T,message,604800)
        self.place = 0
        self.mess = 0
        self._stats = None
        self.started = False
        
    async def start(self,channel):
        if(not self.started):
            self.started = True
            self.ch = channel
            await Embed.send(self,channel)
            async for msg in self.ch.history(limit=1):
                self.mess = msg
            self._stats = None
        else:
            raise ArgumentException('Your Poll is already started',[['But you can create a new one','just use >create_poll']])

    async def check(self,message):
        msg = await getMessage(self.ch,self.mess.id);
        B = msg.reactions
        x = Embed(["Current result:","0x999999"],self.mess)
        x.author([(msg.embeds)[0].title])
        x.footer([])
        for i in B:
            T = [i.count,i.emoji]
            x.addf(T)
        
        if self._stats == None:
            await x.send(message.channel)
            async for msg in message.channel.history(limit=1):
                self._stats = msg.id
        else:
            statistic = await getMessage(message.channel,self._stats);
            await x.edit(statistic)

    async def send(self,channel=None):
        if(not self.started):
            if channel==None:
                await (self.ch).send(embed=self.e)
            else:
                await channel.send(embed=self.e)
        else:
            raise ArgumentException('Your Poll is already started',[['But you can create a new one','just use >create_poll']])

    def id(self):
        return self.mess.id;
    
async def errorMessage(message,title,Table):
    T = [title, "0xFFA500"]
    err = Embed(T,message)
    T = ["Your command has caused an Error..."]
    err.author(T)
    T = ["https://toppng.com/uploads/preview/emoji-glitch-popart-kpop-text-textbox-error-face-11563322597vypecnobqs.png"]
    err.thumbnail(T)
    T = ["Because of the error, your embed was not modified."]
    err.footer(T)
    for arg in Table:
        err.addf(arg)
    await err.send()

async def notfound(message):
    T = ["Embed Not Found", "0xACE1AF"]
    err = Embed(T,message)
    T = ["Your command has caused a minor Error..."]
    err.author(T)
    T = ["https://static.thenounproject.com/png/1400397-200.png"]
    err.thumbnail(T)
    T = ["Use >create to create your embed"]
    err.footer(T)
    T = [["You haven't created an embed",' ⠀'],['All your embeds disappered',' ⠀'],['Embeds are automaticly deleted after 10 minutes without any action on them',' ⠀',' ⠀']]
    for arg in T:
        err.addf(arg)
    await err.send()

async def help(message):
    T = ["Available Commands:", "0xFFD700"]
    err = Embed(T,message)
    T = ["This bot was made by © Patryk Kuchta 2021"]
    err.author(T)
    T = ["https://www.epfl.ch/research/domains/cnp/wp-content/uploads/2020/03/i-need-help-1024x683.jpg"]
    err.thumbnail(T)
    T = ["Fields with * are requiered if at least one argument is provided"]
    err.footer(T)
    T = [[">create",'Text;0xColour\nInitialise your embed.'],['>previous','\nIf the previous embed is still alive, it will restore it'],
         ['>footer','Text;url\nModify or reset your footer'],['>author','Text*;url\nModify or reset your author part'],['>thumbnail','url\nModify or reset your small picture on the top']
         ,['>image','url\nModify or reset your big picture in the middle'],['>field add','Text\*;Value\*;Inline\nAdd a field to your table'],['>field set','Index\*;Text\*;Value\*;Inline\nModify a field in your table']
         ,['>field insert','Index\*;Text\*;Value\*;Inline\nInsert a field to your table'],['>field delete','Index*\nDelete a field from your table'],['>here','\nDiplay your embed on this channel']]
    for arg in T:
        err.addf(arg)
    await err.send()
    T = ["Types:", "0xFFD700"]
    err = Embed(T,message)
    T = ["This bot was made by © Patryk Kuchta 2021"]
    err.author(T)
    T = ["Visit this server for more info: https://discord.gg/xCm36tmkcu"]
    err.footer(T)
    T = [['Text','Any text but it must not contain ;'],['0xColour','Colour in hexadecimal form or one of the predefined colours (check The Embeders server)']
         ,['url','Any link that leads DIRECTLY to an image (you can google search and after that ***Open image in a new tab*** and copy the link) or one of the predefined url (check The Embeders server)']
         ,['Value',"The same as text but it's displayed diffrently"],['Inline','If you want diplay mode inline for a particular field type anything as the last argument']
         ,['Index',"An integer that's within the tables boundaries. (Counting from 1)"]]
    for arg in T:
        err.addf(arg)
    await err.send()

async def send_to(channel,text):
    msg = text.format()
    await channel.send(msg)

async def done(message):
    emoji = bot.get_emoji(820685277391093810)
    await message.add_reaction(emoji)

@bot.event
async def on_ready():
    print('------------------')
    print('Logged in as ' + bot.user.name)
    print('------------------')
    await bot.change_presence(activity=discord.Game(name="with Embeds. BETA"))

@bot.event
async def on_message(message):
    global instances
    if message.author == bot.user:
        return

    sim = Embed([],message)
    if message.content.startswith(">create"):
        try:
            if message.content.startswith(">create_poll"):
                arg = message.content[13:]
                T = spliter(arg)
                T = filter(T,message)
                x = Poll(T,message)
            else:
                arg = message.content[8:]
                T = spliter(arg)
                T = filter(T,message)
                x = Embed(T,message)
            instances.insert(0,x)
            await x.send()
            emoji = bot.get_emoji(820685277391093810)
            await message.add_reaction(emoji)
            print("Currently running: ",len(instances)," (+1)")
            
        except Exception as error:
            emoji = bot.get_emoji(820687219491995668)
            await message.add_reaction(emoji)
            try:
                await errorMessage(message,error.message,error.correct)
            except:
                print(error)
                await errorMessage(message,"Unexpected Error",[])
                await send_to(message.channel,"```"+str(error)+"```")
                
    elif message.content.startswith(">help"):
        await help(message)
                
            
    elif message.content.startswith(">") and not message.content.startswith("> "):
        L = find(message.author.id)
        if(len(L)>0):
            x = L[0]
            x.extend()
            try:
                if message.content.startswith(">previous"):
                    arg = message.content[10:]
                    T = spliter(arg)
                    T = filter(T,message)
                    print("Currently running: ",len(instances)," (+1)")
                    if not T[0]=="":
                        L = find(message.author.id,int(arg))
                    else:
                        L = find(message.author.id,1)
                    if(len(L)>0):
                        x = L[0]
                        x.extend()
                        instances.insert(0,x)
                        await x.send()
                        await done(message)
                    else:
                        await notfound(message)
                    
                elif message.content.startswith(">footer"):
                    arg = message.content[8:]
                    T = spliter(arg)
                    T = filter(T,message)
                    #sim
                    sim.footer(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.footer(T)
                    await x.send()
                    await done(message)

                elif message.content.startswith(">author"):
                    arg = message.content[8:]
                    T = arg.split(";")
                    T = filter(T,message)
                    #sim
                    sim.author(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.author(T)
                    await x.send()
                    await done(message)

                elif message.content.startswith(">thumbnail"):
                    arg = message.content[11:]
                    T = spliter(arg)
                    T = filter(T,message)
                    #sim
                    sim.thumbnail(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.thumbnail(T)
                    await x.send()
                    await done(message)

                elif message.content.startswith(">image"):
                    arg = message.content[7:]
                    T = spliter(arg)
                    T = filter(T,message)
                    #sim
                    sim.image(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.image(T)
                    await x.send()
                    await done(message)
    
                elif message.content.startswith(">field add"):
                    arg = message.content[11:]
                    T = spliter(arg)
                    T = filter(T,message)
                    #sim
                    sim.addf(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.addf(T)
                    await x.send()
                    await done(message)

                elif message.content.startswith(">field set"):
                    arg = message.content[11:]
                    T = spliter(arg)
                    T = filter(T,message)
                    #sim
                    for i in range(x.length()):
                        sim.addf([" "," "])
                    print(T)
                    sim.setf(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.setf(T)
                    await x.send()
                    await done(message)

                elif message.content.startswith(">field insert"):
                    arg = message.content[14:]
                    T = spliter(arg)
                    T = filter(T,message)
                    #sim
                    for i in range(x.length()):
                        sim.addf([" "," "])
                    sim.insf(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.insf(T)
                    await x.send()
                    await done(message)

                elif message.content.startswith(">field delete"):
                    arg = message.content[14:]
                    T = spliter(arg)
                    T = filter(T,message)
                    #sim
                    for i in range(x.length()):
                        sim.addf([" "," "])
                    sim.delf(T)
                    await sim.send_int(820698418757369917,819882393913524275)
                    #sim
                    x.delf(T)
                    await x.send()
                    await done(message)

                elif message.content.startswith(">list_colours") and message.author.id == 362947029800058881:
                    for colour in colours:
                        b = Embed(colour,message)
                        await b.send()

                elif message.content.startswith(">here"):
                    await x.send(message.channel)
                    await done(message)

                elif message.content.startswith(">start"):
                    if isinstance(x, Poll):
                        await x.start(message.channel)
                        await done(message)
                    else:
                        raise ArgumentException('Only a poll can be started',[['To create a poll use:','>create_poll']])

                elif message.content.startswith(">check"):
                    if isinstance(x, Poll):
                        await x.check(message)
                    else:
                        raise ArgumentException('Only a poll can be checked',[['To create a poll use:','>create_poll']])
                    
                    
            except Exception as error:
                emoji = bot.get_emoji(820687219491995668)
                await message.add_reaction(emoji)
                try:
                    await errorMessage(message,error.message,error.correct)
                except:
                    print(error)
                    await errorMessage(message,"Unexpected Error",[])
                    await send_to(message.channel,"```"+str(error)+"```")
                
        else:
            await notfound(message)

    recycle()

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    x = None
    for i in instances:
        if isinstance(i, Poll):
            try:
                if reaction.message.id == i.id():
                    x = i
                    break
            except:
                pass
    if x == None:
        return;
    else:
        await i.check(reaction.message);

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user:
        return
    x = None
    for i in instances:
        if isinstance(i, Poll):
            try:
                if payload.message_id == i.id():
                    x = i
                    break
            except:
                pass
    if x == None:
        return;
    else:
        ch = await bot.fetch_channel(payload.channel_id)
        msg = await getMessage(ch,payload.message_id);
        await i.check(msg);
                
bot.run('ODE5MjA4ODkyODM0NjQ0MDA4.YEjRvA.T1wZ_XCC3RcU3v9OxEh2woUggaU')
    
