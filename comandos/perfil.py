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
            title=f"Perfil de {usuario.name}",
            color= usuario.color
        )


        embed.set_thumbnail(
            url = usuario.display_avatar.url
        )        


        embed.add_field(
            name= "Nome",
            value= usuario.name,
            inline= False
        )


        embed.add_field(
            name= "Nick",
            value= usuario.display_name,
            inline= False
        )


        embed.add_field(
            name= "ID",
            value= usuario.id,
            inline= False
        )


        embed.add_field(
            name= "Criação da Conta",
            value= usuario.created_at.strftime("%d/%m/%Y"),
            inline= True
        )



        embed.add_field(
            name= "Data Entrada Servidor",
            value= usuario.joined_at.strftime("%d/%m/%Y"),
            inline= True
        )


        embed.add_field(
            name= "Atividade",
            value= usuario.activity,
            inline= False
        )

        

        await interaction.response.send_message(
            embed=embed,
        )



    @app_commands.command(name="avatar", description="Verificar o Avatar (foto) do usuário.")
    async def avatar(self, interaction:discord.Interaction, usuario:discord.Member = None):

        if usuario is None:
            usuario = interaction.user


        embed = discord.Embed(
            title= f"Avatar de {usuario.name}",
            color= usuario.color
        )


        embed.set_image(
            url= usuario.display_avatar.url
        )


        await interaction.response.send_message(
            embed=embed
        )



async def setup(bot):
    await bot.add_cog(Perfil(bot))