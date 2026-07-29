import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# --- SISTEMA PARA MANTER O BOT VIVO NA NUVEM ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Online 24/7!"

def run():
    # O Render fornece a porta automaticamente na variável de ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# COLOQUE O ID DO SEU CANAL DE VOZ AQUI
ID_DO_CANAL_DE_VOZ = 1238513896357232675  

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} está online na nuvem!")
    try:
        channel = await bot.fetch_channel(ID_DO_CANAL_DE_VOZ)
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f"Conectado com sucesso ao canal: {channel.name}")
    except Exception as e:
        print(f"Erro ao conectar: {e}")

# Liga o servidor web e depois o bot
keep_alive()

# Apague a linha que tinha "os.environ.get" e coloque o seu token direto aqui dentro das aspas:
TOKEN = "MTUzMTg3NDA5NzM4NDkxNTAzNQ.G08-LO.UKopmXCQPUPAhqH_vhyrB2zquU7AFZU3WNxhKE"

bot.run(TOKEN)

