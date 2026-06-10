import discord
import os
import httpx

from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup

class LeagueOfLegendsView(discord.ui.View):
    def __init__(self, nome_campeao):
        super().__init__()

        opgg_url = f"https://op.gg/lol/champions/{nome_campeao.title()}/build"

        self.add_item(
            discord.ui.Button(
                label="📘 Ver no OP.GG",
                url=opgg_url
            )
        )

class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(name="lolbuild", description="Verificar a runa e build de um campeão.")
    async def BuildLol(self, interaction:discord.Interaction, champion:str):

        await interaction.response.defer()


        url = f"https://op.gg/lol/champions/{champion.lower()}/build"
        urlIcon = f"https://ddragon.leagueoflegends.com/cdn/15.12.1/img/champion/{champion.title()}.png"
        urlImagem = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion.title()}_0.jpg"

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
                    "Nome inválido. Tente novamente."
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



        core_build = []
        melhor_winrate = 0
        melhor_pickrate = "?"


        for tabela in tabelas:

            caption = tabela.find("caption")

            if caption and caption.text.strip() == "Builds Table":

                titulo = tabela.find("thead").find("th").text.strip()

                if titulo == "Core builds":

                    linhas = tabela.find("tbody").find_all("tr")

                for linha in linhas:

                    itens = linha.find_all("img")

                    nomes_itens = [
                        item["alt"]
                        for item in itens
                    ]

                    stats = linha.find_all("strong")

                    pick_rate = stats[0].text
                    win_rate = stats[1].text

                    win_rate_num = float(
                        win_rate.replace("%", "")
                    )

                    if win_rate_num > melhor_winrate:

                        melhor_winrate = win_rate_num
                        melhor_pickrate = pick_rate
                        core_build = nomes_itens

                break


        

        
        
        embed = discord.Embed(
            title=f"Build {champion.title()}",
            description="Verificar itens da build:",
            color=discord.Color.red()
        )

        embed.set_image(
            url=urlImagem
        )

        embed.set_thumbnail(
            url=urlIcon
        )

        embed.add_field(
            name="👢 Bota mais utilizada: \n",
            value=(
                f"{bota}"
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

        embed.add_field(
            name="⚔️ Core Build (Maior Win Rate)",
            value=(
                " ➜ ".join(core_build) 
            ),
            inline=False
        )

        view = LeagueOfLegendsView(champion)

        await interaction.followup.send(
            embed=embed,
            view=view
        )
        

async def setup(bot):
    await bot.add_cog(LeagueOfLegends(bot))