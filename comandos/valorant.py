import discord
import httpx
import os

from discord import app_commands
from discord.ext import commands
from urllib.parse import quote


class ValorantView(discord.ui.View):
    def __init__(self, nick, tag):
        super().__init__()

        riot_id = quote(f"{nick}#{tag}")

        tracker_url = f"https://tracker.gg/valorant/profile/riot/{riot_id}/overview"

        self.add_item(
            discord.ui.Button(
                label="📊 Ver no Tracker",
                url=tracker_url
            )
        )
        print("self criada")
        print(tracker_url)


class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(name="valorant", description="Ver informações de sua conta Valorant")
    async def infoValorant(self, interaction:discord.Interaction, nick:str, tag:str):

        await interaction.response.defer()

        API_KEY = os.getenv("VALORANT_API_KEY")


        
        urlPerfil = f"https://api.henrikdev.xyz/valorant/v2/account/{nick}/{tag}"
        urlCards = f"https://api.henrikdev.xyz/valorant/v1/account/{nick}/{tag}"
        

        headers = {
            "Authorization": API_KEY
        }

    

        async with httpx.AsyncClient() as client:

            resposta = await client.get(urlPerfil, headers=headers)
            respostaCard = await client.get(urlCards, headers=headers)

            

            if resposta.status_code != 200:

                await interaction.followup.send(
                    "Nick ou Tag inválidos"
                )

                return


            dados = resposta.json()
            dadosCard = respostaCard.json()

            regiao = dados["data"]["region"]
            
          

            urlMmr = f"https://api.henrikdev.xyz/valorant/v3/mmr/{regiao}/pc/{nick}/{tag}"
            respostaMMR = await client.get(urlMmr, headers=headers)

            
            
            dadosMMR = respostaMMR.json()
            

       
        rank = dadosMMR["data"]["current"]["tier"]["name"]
        
        
        pontuacao = dadosMMR["data"]["current"]["rr"]
        

        nickName = dados["data"]["name"]
        tagName = dados["data"]["tag"]
        nivel = dados["data"]["account_level"]

        plataformas = ", ".join(dados["data"]["platforms"])
        ultimaAtualizacao = dados["data"]["updated_at"] #retorna a data da ultima mudança nos dados da conta

        cardPequeno = dadosCard["data"]["card"]["small"]
        cardGrande = dadosCard["data"]["card"]["wide"]
        
        wins = dadosMMR["data"]["seasonal"][0]["wins"]
        
        games = dadosMMR["data"]["seasonal"][0]["games"]
        
        winRate = (wins / games) * 100 
        
        
        embed = discord.Embed(
            title=f"{nick} #{tagName}",
            description="Informações da Conta:",
            color= discord.Color.red()
        )

        
        embed.add_field(
            name="🌎 Região",
            value=regiao.upper(),
            inline=True
        )

        embed.add_field(
            name="⭐ Nível",
            value=nivel,
            inline=True
        )

        embed.add_field(
            name="🖥️ Plataformas",
            value=plataformas,
            inline=True
        )

        embed.add_field(
            name="🏆 Rank",
            value=rank,
            inline=True
        )

        embed.add_field(
            name="💎 Pontuação",
            value=pontuacao,
            inline=True
        )

        embed.add_field(
            name="📈 Win Rate",
            value=f"{winRate:.1f}%",
            inline=True
        )

        embed.add_field(
            name="👤 Riot ID",
            value=f"{nickName} #{tagName}",
            inline=False
        )


        embed.set_thumbnail(
            url=cardPequeno
        )

        embed.set_image(
            url=cardGrande
        )

        embed.set_footer(
            text=f"Ultima atualização: {ultimaAtualizacao}"
        )
        
        view = ValorantView(nickName, tagName)

        
        await interaction.followup.send(
            embed=embed,
            view=view
        )
       
async def setup(bot):
        await bot.add_cog(Valorant(bot))