import discord
from discord.ext import commands,tasks
from discord.embeds import Embed
from discord import FFmpegPCMAudio

class Radio(commands.Cog):
    def __init__(self,client):
        self.client=client

    
    @commands.command()
    async  def radio(self,ctx,url:str ="http://82.223.139.234/omeganull"):
        channel = ctx.message.author.voice.channel
        global player
        try:
            player = await channel.connect()
        except:
            pass
        player.play(FFmpegPCMAudio(url))
    
    @commands.command()
    async def rstop(self,ctx):
        player.stop()

def setup(client):
  client.add_cog(Radio(client))
