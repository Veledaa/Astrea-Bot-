import discord
import os
import httpx

from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup



class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(name="lolbuild", description="Verificar a runa e build de um campeão.")
    async def BuildLol(self, interaction:discord.Interaction, champion:str):

        await interaction.response.defer()


        url = f"https://op.gg/lol/champions/{champion.lower()}/build"

        headers = {
            "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/137.0.0.0 Safari/537.36"
                    )
        }


        async with httpx.AsyncClient() as client:

            resposta = await client.get(url, headers=headers)

            if resposta.status_code != 200:
                await interaction.followup.send(
                    "Não foi possivél obter os itens."
                )

                return

            html = resposta.text

            

        soup = BeautifulSoup(html, "html.parser")
            
        tabelas = soup.find_all("table")

        bota = "Não encontrada"
        pick_rate = "?"
        win_rate = "?"

        for tabela in tabelas:

            caption = tabela.find("caption")

            if caption and caption.text.strip() == "Boots Table":

                primeira_linha = tabela.find("tbody").find("tr")

                bota = primeira_linha.find("img")["alt"]

                stats = primeira_linha.find_all("strong")

                pick_rate = stats[0].text
                win_rate = stats[1].text

                break

        
        starter_itens = []
        starter_pick = "?"
        starter_win = "?"

        for tabela in tabelas:

            caption = tabela.find("caption")

            if caption and caption.text.strip() == "Items Table":

                titulo = tabela.find("thead").find("th")

                if titulo and titulo.text.strip() == "Starter items":

                    primeira_linha = tabela.find("tbody").find("tr")

                    imagens = primeira_linha.find_all("img")

                    starter_itens = [
                        imagem["alt"]
                        for imagem in imagens
                    ]

                    stats = primeira_linha.find_all("strong")

                    starter_pick = stats[0].text
                    starter_win = stats[1].text

                    break

        
        
        embed = discord.Embed(
            title=f"Build {champion.title()}",
            description="Verificar itens da build:",
        )

        embed.add_field(
            name="👢 Bota mais utilizada: \n",
            value=(
                f"**{bota}**"
            ),
            inline=False
        )

        embed.add_field(
            name="🧪 Starter Items",
            value=(
                f"{' + '.join(starter_itens)}\n"
            ),
            inline=False
)

        await interaction.followup.send(
            embed=embed
        )
        

async def setup(bot):
    await bot.add_cog(LeagueOfLegends(bot))