import discord
from discord import app_commands
from discord.ext import commands



class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(name="perfil", description="Verificar o perfil de um usuário.")
    async def perfil(self, interaction:discord.Interaction, usuario:discord.Member = None):

        if usuario is None:
            usuario = interaction.user

        
        embed = discord.Embed(
            title=f"Perfil de {usuario.name}"
        )


        embed.set_image(
            url = usuario.display_avatar.url
        )        


        await interaction.response.send_message(
            embed=embed
        )



async def setup(bot):
    await bot.add_cog(Perfil(bot))