from discord_together import DiscordTogether
from discord.ext.commands import command, Cog
import os
from discord_components import (
    Button,
    ButtonStyle
)
from discord import Embed
import discord

class Grupal(Cog):
    def __init__(self,client):
        self.client=client
    
    
    @Cog.listener()
    async def on_ready(self):
        self.togetherControl = await DiscordTogether(os.environ['DSC_bot']) 
 
    @command(help="creas una sala para ver cosas en una misma sala")
    async def grupal(self, ctx):
        async def callback(interaction):
            link=await self.togetherControl.create_link(ctx.author.voice.channel.id,interaction.custom_id,max_age =43200)
            embed=Embed(title="Sala de "+interaction.author.display_name, description=f"[Link de la sala para jugar a {interaction.custom_id}]({link})")
            await interaction.send(embed=embed)


        embed=Embed(title="Actividades Compartidas",description="Pulsa en los botones para crear una sala y compartir con los de la sala", color=discord.Color.random())


        if ctx.author.voice is None:
             await ctx.send("No estas en ningun canal de voz")
        else:
            await ctx.send(embed=embed,components=[self.client.components_manager.add_callback(Button(style=ButtonStyle.red,label="YouTube",id='youtube'),callback),self.client.components_manager.add_callback(Button(style=ButtonStyle.blue,label="Poker",id="poker"),callback),self.client.components_manager.add_callback(Button(style=ButtonStyle.green,label="Betrayal",id="betrayal"),callback)])

def setup(client):
  client.add_cog(Grupal(client))

