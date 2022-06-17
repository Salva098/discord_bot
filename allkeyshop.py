
import discord
from discord.ext import commands,tasks
from discord.embeds import Embed
import json
from discord_components import *
from pagination import Pagination



class Allkeyshop(commands.Cog):
    def __init__(self,client):
        self.client=client


    @commands.command()
    async def search(self,ctx,name):
        self.indx=0
        game=[]



        listgames=[]

        f=open("games.json","r")
        file=f.read()
        f.close()
        json_data=json.loads(file)
        for x in json_data:
            if name.lower() in x["name"].lower() :
                listgames.append(x)
        # mostrar listgames en un embed de discord
        if len(listgames)==0:
            await ctx.send("No se encontraron resultados")
        else:
            game = [listgames[i:i + 10] for i in range(0, len(listgames), 10)]
            a =Pagination(self.client,game,ctx.channel)
            await a.start(ctx)

    


def setup(client):
  client.add_cog(Allkeyshop(client))

