import discord
from discord import app_commands
from discord.ext import commands
import httpx


class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="pokemon", description="Mostra informações de Pokemons")
    async def pokemon(self, interaction:discord.Interaction, nome:str):

        url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"


        async with httpx.AsyncClient() as client:

            resposta = await client.get(url)

        if resposta.status_code != 200:
            await interaction.response.send_message("Pokemon não encontrado. Verifique se escreveu corretamente.")
        
            return

        dados = resposta.json()


        nomePokemon = dados["name"].title()
        idPokemon = dados["id"]
        alturaPokemon = dados["height"]
        pesoPokemon = dados["weight"]

        tipos = [
            tipo["type"]["name"].title()
            for tipo in dados["types"]
        ]

        tipos = ", ".join(tipos)

        imagem = dados["sprites"]["front_default"]

        embed = discord.Embed(
            title=nomePokemon,
            color=discord.Color.yellow()
        )

        embed.add_field(
            name="ID",
            value=idPokemon
        )

        embed.add_field(
            name="Altura",
            value=alturaPokemon
        )

        embed.add_field(
            name="Peso",
            value=pesoPokemon
        )

        embed.add_field(
            name="Tipos",
            value=tipos,
            inline=False
        )

        embed.set_thumbnail(
            url=imagem
        )

        await interaction.response.send_message(
            embed=embed
        )

        await interaction.response.send_message(f"O nome do pokemon é: {nomePokemon}")


async def setup(bot):
    await bot.add_cog(Pokemon(bot))