import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()

Token = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)


@bot.event
async def on_ready():
    sincs = await bot.tree.sync()
    print(f"{len(sincs)} Comandos sincronizados!")
    print("BOT ONLINE - Olá, Mundo!")
    print(bot.user.name)
    print(bot.user.id)



async def carregarCogs():
    for arquivo in os.listdir("comandos"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")



async def main():
    
    async with bot:


        await carregarCogs()


        await bot.start(Token)


asyncio.run(main())