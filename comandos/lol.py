import discord
import os
import httpx

from discord import app_commands
from discord.ext import commands



class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(name="lolbuild", description="Verificar a runa e build de um campeão.")
    async def BuildLol(self, interaction:discord.Interaction, nomepersonagem:str):

        url = ""

   

async def setup(bot):
    await bot.add_cog(LeagueOfLegends(bot))