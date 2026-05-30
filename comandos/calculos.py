import discord
from discord import app_commands
from discord.ext import commands



class Calculos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.command(name="somar", description="Soma 2 números")
    async def somar(self, interaction:discord.Interaction, num1:float, num2:float):

        resultado = num1 + num2

        await interaction.response.send_message(f"A soma entre {num1} e {num2} é: {resultado}")



    @app_commands.command(name="subtrair", description="Subtrai 2 números")
    async def subtrair(self, interaction:discord.Interaction, num1:float, num2:float):
        
        resultado = num1 - num2

        await interaction.response.send_message(f"A subtração entre {num1} e {num2} é: {resultado}")

    
    @app_commands.command(name="multiplicar", description="Multiplica 2 números")
    async def multiplicar(self, interaction:discord.Interaction, num1:float, num2:float):
        
        resultado = num1 * num2

        await interaction.response.send_message(f"A multiplicação entre {num1} e {num2} é: {resultado}")

    
    @app_commands.command(name="dividir", description="Divide 2 números")
    async def dividir(self, interaction:discord.Interaction, num1:float, num2:float):
        
        resultado = num1 / num2

        await interaction.response.send_message(f"A divisão entre {num1} e {num2} é: {resultado}")
     

async def setup(bot):
    await bot.add_cog(Calculos(bot))