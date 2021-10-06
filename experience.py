
import discord
from discord.ext import commands,tasks
from levelsql import Level
from discord.embeds import Embed


class experience(commands.Cog):
    def __init__(self,client):
        self.client=client



    @commands.command()
    async def rank(self,ctx):
        level=Level()
        autor=ctx.author.id
        server=ctx.guild.id
        nivel=level.check_user(autor,server)

        embed=discord.Embed(title="Rango", description="Rango de "+ctx.author.mention)
        embed.set_thumbnail(url=str(ctx.author.avatar_url))
        embed.add_field(name="Nivel", value=nivel.level, inline=False)
        embed.add_field(name="experiencia", value=nivel.exp, inline=False)
        embed.add_field(name="Siguiente nivel", value=nivel.exp_max, inline=False)
        level.disconect()
        await ctx.reply(embed=embed)
    



def setup(client):
  client.add_cog(experience(client))

