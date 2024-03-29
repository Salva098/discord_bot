from objects import Game
import time
import requests
import json
import datetime
from levelsql import Level
from discord.ext import commands

class freegames(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def setfree(self,ctx,ch):
        chas=int(ch[2:-1])
        if self.client.get_channel(chas):
            sql=Level()
            server_id=ctx.guild.id
            sql.free_games(server_id,chas)
            await ctx.reply("se ha añadido el "+ch+"canal para que envie juegos gratis")
            sql.disconect()
        else:
            ctx.reply("el canal no existe o no lo has escrito bien")
            
def setup(client):
  client.add_cog(freegames(client))


def free_gamess():
    lista=requests.get("https://www.gamerpower.com/api/giveaways")
    lista_game=[]
    sql =Level()
    hola=json.loads(lista.text)
    lista_id_games=sql.check_id_game()
    for x in reversed(json.loads(lista.text)):
        if not x["id"] in lista_id_games:
            lista_game.append(Game(
                x["title"],
                x["worth"],
                x["image"],
                x["description"],
                x["instructions"],
                x["open_giveaway_url"],
                x["type"],
                x["platforms"],
                x["published_date"],
                x["end_date"]
            ))
            sql.insert_id_game(x["id"])
            
    return lista_game

