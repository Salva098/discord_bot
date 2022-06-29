import discord
from discord.ext import commands,tasks
from discord.embeds import Embed
from discord_together import DiscordTogether
from levelsql import Level
from free_games import free_gamess
from discord_components import *
import requests
import json
import os
from discord_ui import UI


import radio
import grupal
import music
import experience
import free_games
import allkeyshop

cogs=[music,experience,free_games,grupal,allkeyshop,heardle,radio]
bot=commands.Bot(command_prefix='-')

for i in range(len(cogs)):
  cogs[i].setup(bot)

@tasks.loop(hours=336)
async def update_list_games():
    games = requests.get('https://www.allkeyshop.com/api/v2/vaks.php?action=gameNames&locale=es_ES&currency=eur')
    games = json.loads(games.text)
    games=games["games"]
    a =json.dumps(games)
    with open('games.json', 'w') as outfile:
        json.dump(games, outfile)
    print("hecho")


@tasks.loop(seconds=60.0)
async def Juegos_gratis():
    print("vuelta")
    canales=Level()
    canal=[]
    for y in canales.check_freegame():
        if bot.get_channel(y):
            canal.append(bot.get_channel(y))
    juegos = free_gamess()
    for x in juegos:
        mensajejuego=Embed(title=x.title,description=x.description.strip()[:2045])
        mensajejuego.set_image(url=x.image)
        mensajejuego.add_field(name="Precio antes",value=x.worth)
        mensajejuego.add_field(name="Plataforma",value=x.plataforms)
        mensajejuego.add_field(name="Tipo",value=x.type)
        mensajejuego.add_field(name="Dia Publicado",value=x.published_date)
        mensajejuego.add_field(name="Ultimo dia",value=x.end_date)
        mensajejuego.add_field(name="Instrucciones",value=x.instructions,inline=False)
        
        for z in canal:
            try:
                await z.send(embed=mensajejuego,components=[
                    Button(label="Pillar el Juego",url=x.open_giveaway_url,style=ButtonStyle.URL)
                ])
            except:
                print("no hay permisos")
    canales.disconect()

@bot.event
async def on_message(message):
    if message.author.dm_channel==None:
        message
        if not str(message.channel).startswith("Direct Message with") and not message.author.bot:
            level=Level()
            autor=message.author.id
            server=message.guild.id
            name=message.guild.name
            level.new_user(autor,server,name)
            next_level,nivel=level.increase_exp(autor,server)
            if next_level:
                await message.channel.send(message.author.mention+" Enorabuena has subido al nivel "+ str(nivel))
            level.disconect()
    await bot.process_commands(message)


@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Porno solo"))
    print('My Ready is Body')
    Juegos_gratis.start()
    update_list_games.start()


bot.run(os.environ.get("bot_token"))
