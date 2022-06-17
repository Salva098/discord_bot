from discord.embeds import Embed
import requests
import discord
from discord_components import *
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import figure
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import os






class Pagination():
    def __init__(self,client,game,channel):
        self,
        self.client=client
        self.game=game
        self.channel=channel
        self.indx=0
        self.options=[]

    
    async def back(self,interaction):
        self.indx= self.indx -1 
        if self.indx >=0:

            await self.embed(self.game,self.indx,interaction)
            await interaction.send(content="pagina anterior")
        else:
            self.indx=self.indx+1
            await interaction.send(content="No hay pagina anterior")






    async def next(self,interaction):
        self.indx= self.indx +1 
        if not self.indx  == len(self.game)-1:

            await self.embed(self.game,self.indx,interaction)
            await interaction.send(content="pagina siguiente")
        else:
            self.indx=self.indx-1
            await interaction.send(content="No hay pagina siguiente")

    async def Historico(self,interaction):
        timelist = []
        pricelist = []
        regionlist = []
        json= requests.get("https://www.allkeyshop.com/api/v2/vaks.php?action=history&locale=es_ES&currency=eur&id={}".format(str(self.gameid))).json()
        history=json["response"]['history']
        regions=json["response"]['regions']
        for x,y in regions.items():
            regionlist.append(y)
        fig, ax = plt.subplots()
        maphistory={}
        history= sorted(history,key=lambda x : x['timestamp'])
        for x in regionlist:    
            pricelist=[]
            timelist=[]
            for y in history:
                if str(x["id"]) == str(y["regionId"]):
                    pricelist.append(y["price"])
                    timelist.append( datetime.utcfromtimestamp(int( y['timestamp'])).strftime('%d-%m-%Y %H:%M:%S'))
            maphistory[x['name']]=[pricelist,timelist]
        # plt.figure(figsize=(20,8))
        fig.set_figwidth(20)
        fig.set_figheight(8)
        fig.legend(prop={'size': 6})
        for x in regionlist:
            ax.scatter(maphistory[x['name']][1],maphistory[x['name']][0],label=x['name'])
        dtFmt = mdates.DateFormatter('%d-%m') # define the formatting
        plt.gca().xaxis.set_major_formatter(dtFmt) 
        # show every 12th tick on x axes
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=90, fontweight='light',  fontsize='x-small',)

      
        ax.legend(loc = 'upper right')
        plt.savefig('diagrama-dispersion.png')
        await interaction.channel.send(file=discord.File('diagrama-dispersion.png'))
        os.remove('diagrama-dispersion.png')




    async def Ofertas(self,interaction):
        pass

    async def selectgame(self,interaction):
        json = requests.get("https://www.allkeyshop.com/api/v2/vaks.php?action=products&locale=es_ES&currency=eur&ids={}&showOffers=1&showVouchers=1".format(interaction.values[0])).json()
        product = json['products'][0]
        embedgame = Embed(title=product['name'],description="Este juego tiene "+str(product["offerAggregate"]["offerCount"])+" ofertas, con el precio mas bajo "+str(product["offerAggregate"]["lowestPrice"])+ " y el precio mas alto "+str(product["offerAggregate"]["highestPrice"]),color=0x00ff00)
        embedgame.set_image(url=product['coverImageUrl'])
        embedgame.set_thumbnail(url=product['thumbnailUrl'])
        self.gameid=product['id']

        await interaction.channel.send(embed=embedgame,
        components=[    
            self.client.components_manager.add_callback(
                Button(label="Historico",style=ButtonStyle.red),self.Historico),
            self.client.components_manager.add_callback(
                Button(label="Ofertas",style=ButtonStyle.blue),self.Ofertas)
        ]
        )




    async def embed(self, game,index, interaction):
        self.options=[]
        embed=Embed(title="Resultados de la busqueda",description="Busqueda hecha por "+interaction.message.author.mention,color=0x00ff00)
        for x in game[index]:
            embed.add_field(name=" - "+x["name"],value="----------------------",inline=False)
            self.options.append(SelectOption(label=x['name'],value=x['id']))
        previusstyle = False
        if not index>=0:
            previusstyle = True
        nextstyle = False
        if index==len(self.game):
            nextstyle = True

        await interaction.message.edit(embed=embed,components=[
        self.client.components_manager.add_callback(
                Select( options=self.options),self.selectgame),
                [
        self.client.components_manager.add_callback(
            Button(label="<",style=ButtonStyle.blue,disabled= previusstyle),self.back),
        self.client.components_manager.add_callback(
            Button(label=">",style=ButtonStyle.blue,disabled=nextstyle),self.next)
                ]
            ])

    async def start(self,ctx):
        embed=Embed(title="Resultados de la busqueda",description="Busqueda hecha por "+ctx.author.mention,color=0x00ff00)
        self.options=[]

        for x in self.game[self.indx]:
            embed.add_field(name=" - "+x["name"],value="----------------------",inline=False)
            self.options.append(SelectOption(label=x['name'],value=x['id']))
        previusstyle = False
        if self.indx==0:
            previusstyle = True
        nextstyle = False
        if self.indx==len(self.game)-1:
            nextstyle = True


        await ctx.send(embed=embed,components=[
            self.client.components_manager.add_callback(
                    Select( options=self.options),self.selectgame),
                    [
            self.client.components_manager.add_callback(
                Button(label="<",style=ButtonStyle.blue,disabled= previusstyle),self.back),
            self.client.components_manager.add_callback(
                Button(label=">",style=ButtonStyle.blue,disabled=nextstyle),self.next)
                    ]
                ])