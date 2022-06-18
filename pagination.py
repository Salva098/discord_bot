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
        self.indxoffers=0

        self.options=[]

    
    async def back(self,interaction):
        self.indx= self.indx -1 
        if self.indx >=0:

            await self.embed(self.game,self.indx,interaction)
            await interaction.send(content="pagina anterior")
        else:
            self.indx=self.indx+1
            await interaction.send(content="No hay pagina anterior")

    async def backoffers(self,interaction):
        self.indxoffers= self.indxoffers -1 
        if self.indxoffers >=0:

            await self.embedoffers(self.offers,self.indxoffers,interaction)
            await interaction.send(content="pagina anterior")
        else:
            self.indxoffers=self.indxoffers+1
            await interaction.send(content="No hay pagina anterior")

    async def nextoffers(self,interaction):
        self.indxoffers= self.indxoffers +1 
        if not self.indxoffers  == len(self.game)-1:

            await self.embedoffers(self.offers,self.indxoffers,interaction)
            await interaction.send(content="pagina siguiente")
        else:
            self.indxoffers=self.indxoffers-1
            await interaction.send(content="No hay pagina siguiente")




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
        for x in regionlist:    
            pricelist=[]
            timelist=[]
            for y in history:
                if str(x["id"]) == str(y["regionId"]):
                    pricelist.append(y["price"])
                    timelist.append( datetime.utcfromtimestamp(int( y['timestamp'])).strftime('%d-%m-%Y')  )
            indextime={}
            for xT in timelist:
                time=[]
                for indx, y in enumerate(timelist):
                    if xT == y:
                        time.append(indx)

                indextime[str(xT)]=time

            for k,xV in indextime.items():
                price = 0
                for y in xV:
                    price = price + pricelist[y]
                media = price/len(xV)
                indextime[k]=media
            maphistory[x['name']]=indextime
        for x in regionlist:
            ax.plot(maphistory[x['name']].keys(),maphistory[x['name']].values(),label=x['name'])
   
        fig.set_figwidth(20)
        fig.set_figheight(8)
        # fig.legend(prop={'size': 6})
        plt.xticks(rotation=90, fontweight='light',  fontsize='x-small',)

      
        ax.legend(loc = 'upper right')
        plt.savefig('diagrama-dispersion.png')
        await interaction.channel.send(file=discord.File('diagrama-dispersion.png'))
        os.remove('diagrama-dispersion.png')




    async def Ofertas(self,interaction):
        self.indxoffers=0
        await self.startoffer(interaction.channel)
    



    async def selectgame(self,interaction):
        json = requests.get("https://www.allkeyshop.com/api/v2/vaks.php?action=products&locale=es_ES&currency=eur&ids={}&showOffers=1&showVouchers=1".format(interaction.values[0])).json()
        product = json['products'][0]
        embedgame = Embed(title=product['name'],description="Este juego tiene "+str(product["offerAggregate"]["offerCount"])+" ofertas, con el precio mas bajo "+str(product["offerAggregate"]["lowestPrice"])+ " y el precio mas alto "+str(product["offerAggregate"]["highestPrice"]),color=0x00ff00)
        if product['coverImageUrl'] != None:
            embedgame.set_image(url=product['coverImageUrl'])
        if product['thumbnailUrl'] != None:    
            embedgame.set_thumbnail(url=product['thumbnailUrl'])
        self.gameid=product['id']
        self.offers=[product["offers"][i:i + 10] for i in range(0, len(product["offers"]), 10)]
        await interaction.channel.send(embed=embedgame,
        components=[
                        [  
                        self.client.components_manager.add_callback(
                            Button(label="Ofertas",style=ButtonStyle.blue),self.Ofertas),
                        self.client.components_manager.add_callback(
                            Button(label="Historico",style=ButtonStyle.red),self.Historico)
                        ]
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

    async def embedoffers(self, offers,index, interaction):
        embed=Embed(title="Resultados de la busqueda",description="Busqueda hecha por "+interaction.message.author.mention,color=0x00ff00)
        for x in offers[index]:
            code="No Code"
            frase ="En "+x["store"]["name"]+" el precio esta a "+ str(x["price"])+"€"
            if x["bestVoucher"]:
                    frase = frase + " y puede bajar a  "+str(x["bestVoucher"]["priceWithVoucher"])+" € con un descuento de "+str(x["bestVoucher"]["discount"]["value"])+"%"
                    code ="Code:"+x["bestVoucher"]["code"]
            embed.add_field(name=frase,value=code,inline=False)
        previusstyle = False
        if not index>=0:
            previusstyle = True
        nextstyle = False
        if index==len(self.offers):
            nextstyle = True

        await interaction.message.edit(embed=embed,components=[
 
                [
        self.client.components_manager.add_callback(
            Button(label="<",style=ButtonStyle.blue,disabled= previusstyle),self.backoffers),
        self.client.components_manager.add_callback(
            Button(label=">",style=ButtonStyle.blue,disabled=nextstyle),self.nextoffers)
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


    async def startoffer(self,ctx):
        embed=Embed(title="Ofertas",color=0x00ff00)

        for x in self.offers[self.indx]:
            code="No Code"
            frase ="En "+x["store"]["name"]+" el precio esta a "+ str(x["price"])+"€"
            if x["bestVoucher"]:
                frase = frase + " y puede bajar a  "+str(x["bestVoucher"]["priceWithVoucher"])+" € con un descuento de "+str(x["bestVoucher"]["discount"]["value"])+"%"
                code ="Code:"+x["bestVoucher"]["code"]
            embed.add_field(name=frase,value=code,inline=False)
        previusstyle = False
        if self.indxoffers==0:
            previusstyle = True
        nextstyle = False
        if self.indxoffers==len(self.offers)-1:
            nextstyle = True


        await ctx.send(embed=embed,components=[

                    [
            self.client.components_manager.add_callback(
                Button(label="<",style=ButtonStyle.blue,disabled= previusstyle),self.backoffers),
            self.client.components_manager.add_callback(
                Button(label=">",style=ButtonStyle.blue,disabled=nextstyle),self.nextoffers)
                    ]
                ])