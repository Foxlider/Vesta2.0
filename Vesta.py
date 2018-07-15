import discord
import random
import os
import sys
from discord import opus
from discord.ext import commands
from json import load as jload

description = '''I am Vesta. Not 2.0 yet but Worry not, I am updating.'''

name='vesta'

__program__ = "Vesta"
__version__ = "0.1a"


prefix = '!'


### ______________
### Main Functions

def read_key():
    """
    Read a bot's key JSON to get it's token
    Keys must be stored in the key folder and have a basic 'key':'<keytext>' object
    """
    with open('keys/vesta.key', 'r') as f:
        datum = jload(f)
        key = datum.get("key", "")
        if not key:
            raise IOError("Key not found in JSON keyfile")
        return key
    return None

### ____________
### Data Classes

### _________
### Bot class

class Vesta:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}
    
    ##CMD version
    @commands.command(pass_context=True)
    async def version(self, ctx):
        """Displays the version of the bot"""
        print("Command 'version' called")
        print(f"I am *{__program__} v{__version__}*.\nNice to meet you {ctx.message.author.name}.")
        await ctx.message.delete()
        await ctx.send(f"I am *{__program__} v{__version__}*.\nNice to meet you {ctx.message.author.mention}.")


class Utilities:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    ##CMD roll
    @commands.command(pass_context=True)
    async def roll(self, ctx, dice=""):
        """Rolls a dice in NdN format."""
        print("Command 'roll' called")
        await ctx.message.delete()
        if dice == None or dice =="":
            try : 
                raise ValueError('Format has to be in NdN!')
            except ValueError:
                await ctx.send('Format has to be in NdN!')
                return
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        msg = f'{ctx.message.author.mention} rolled {rolls}d{limit}'
        for r in range(rolls) :
            msg += f"\n Dice {r} is a {random.randint(1, limit)} !"
        
        print(msg)
        await ctx.send(msg)

class WAcommands:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    @commands.command(pass_context=True)
    async def bored(self, ctx):
        """Gives a user an idea to avoid boredom"""
        print("Command 'bored' called")
        with open('data/bored/ideas.json', 'r') as f:
            data = jload(f) 
            line = random.randint(1,len(data))
            print(f"Line {line} : {data[str(line)]}")
            await ctx.send(data[str(line)])
        return None

    @commands.command(pass_context=True)
    async def coriolis(self, ctx, *, ship="", build="", name=""):
        """Prints out our coriolis builds\n (Search will be implemented soon.)"""
        print("Command 'coriolis' called")
        with open('data/coriolis/ships.json', 'r') as f:
            data = jload(f) 
            msg = "Our coriolis builds : \n\n"
            for sClass in data:
                #print(sClass)
                msg += f"[{sClass}]"
                for sName in data[sClass]:
                    #print(f" - {sName}")
                    msg += f"\n  <{sName}>\n"
                    for field in data[sClass][sName]:
                        value = data[sClass][sName][field]
                        #print(f"   - {field} : {value} ")
                        msg += f"     - {field} : {value} \n"
            
            print(msg)
            await ctx.send(msg)
        return None

    
### ________________
### Startup commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), description=description)
bot.add_cog(Vesta(bot))
bot.add_cog(Utilities(bot))
bot.add_cog(WAcommands(bot))

@bot.event
async def on_ready():
    print('------\nStarted {0} v{1}\n------\nLogged in as:\n{2} \n(ID: {2.id})\n------'.format(__program__, __version__, bot.user))
    game=discord.Game(name='Vesta Online')
    await bot.change_presence(status=discord.Status.online, activity=game)
bot.run(read_key(), bot=True, reconnect=True)
