import discord
from discord.ext import commands,tasks
from discord.embeds import Embed
from discordTogether import DiscordTogether
from levelsql import Level
from free_games import free_gamess
from discord_components import *
import os

import music
import experience
import free_games
cogs=[music, experience,free_games]
bot=commands.Bot(command_prefix='-')
togetherControl = DiscordTogether(bot)
# bot=commands.Bot(command_prefix='-')

for i in range(len(cogs)):
  cogs[i].setup(bot)


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
        # mensajejuego.set_thumbnail(url=x.image)
        mensajejuego.add_field(name="Precio antes",value=x.worth)
        mensajejuego.add_field(name="Plataforma",value=x.plataforms)
        mensajejuego.add_field(name="Tipo",value=x.type)
        mensajejuego.add_field(name="Dia Publicado",value=x.published_date)
        mensajejuego.add_field(name="Ultimo dia",value=x.end_date)
        mensajejuego.add_field(name="Instrucciones",value=x.instructions,inline=False)
        
        for z in canal:
            await z.send(embed=mensajejuego,components=[
                Button(label="Pillar el Juego",url=x.open_giveaway_url,style=ButtonStyle.URL)
            ])
    canales.disconect()

@bot.event
async def on_message(message):
    if not message.channel.guild.id == 890181927766745088:
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





# bot gobierno de españa
# bot.run()


# ahiidisegratis

bot.run(os.environ.get("DSC_bot"))
