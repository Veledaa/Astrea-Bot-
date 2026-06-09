import discord
from discord import app_commands
from discord.ext import commands
import httpx


class PokemonView(discord.ui.View):
    def __init__(self, nomePokemonView):
        super().__init__()

        urlPokedex = f"https://pokemondb.net/pokedex/{nomePokemonView.lower()}"

        self.add_item(
            discord.ui.Button(
                label="🔴 Veja na Pokedex",
                url=urlPokedex
            )
        )

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

            

            speciesUrl = dados["species"]["url"]
            respostaSpecies = await client.get(speciesUrl)

            dadosSpecies = respostaSpecies.json()

            


        nomePokemon = dados["name"].title()
        idPokemon = dados["id"]
        alturaPokemon = dados["height"] / 10 #metros
        pesoPokemon = dados["weight"] / 10 #kg

        tipos = [
            tipo["type"]["name"].title()
            for tipo in dados["types"]
        ]

        tipos = ", ".join(tipos)

        imagem = dados["sprites"]["front_default"]


        geracoes = {
            "generation-i": "1ª Geração (Kanto)",
            "generation-ii": "2ª Geração (Johto)",
            "generation-iii": "3ª Geração (Hoenn)",
            "generation-iv": "4ª Geração (Sinnoh)",
            "generation-v": "5ª Geração (Unova)",
            "generation-vi": "6ª Geração (Kalos)",
            "generation-vii": "7ª Geração (Alola)",
            "generation-viii": "8ª Geração (Galar)",
            "generation-ix": "9ª Geração (Paldea)"
        }


        geracaoApi = dadosSpecies["generation"]["name"]


        geracao = geracoes.get(geracaoApi, "Desconhecida")


        cores = {
            "yellow": 0xFFFF00,
            "red": 0xFF0000,
            "blue": 0x0000FF,
            "green": 0x00FF00,
            "black": 0x000000,
            "brown": 0x8B4513,
            "purple": 0x800080,
            "pink": 0xFFC0CB,
            "white": 0xFFFFFF,
            "gray": 0x808080
        }


        corPokemon = cores.get(
            dadosSpecies["color"]["name"],
            0x2F3136
        )

        
        embed = discord.Embed(
            title=nomePokemon,
            description=f"Informações sobre {nomePokemon}: ",
            color=corPokemon
        )
        
        embed.add_field(
            name="ID",
            value=idPokemon
        )

        embed.add_field(
            name="Altura",
            value=f"{alturaPokemon} m"
        )

        embed.add_field(
            name="Peso",
            value=f"{pesoPokemon} Kg"
        )

        embed.add_field(
            name="Tipos",
            value=tipos,
            inline=False
        )

        embed.add_field(
            name="Geração",
            value=geracao,
        )

        embed.set_thumbnail(
            url=imagem
        )

        view = PokemonView(nomePokemon)
        
        await interaction.response.send_message(
            embed=embed,
            view=view
        )
        

async def setup(bot):
    await bot.add_cog(Pokemon(bot))