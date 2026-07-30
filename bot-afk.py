import asyncio
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
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=">//<!", intents=intents)

# COLOQUE O ID DO SEU CANAL DE VOZ AQUI ou deixe None para usar o comando !join
DEFAULT_VOICE_CHANNEL_ID = None
voice_channel_id = DEFAULT_VOICE_CHANNEL_ID
voice_check_task = None

async def connect_to_voice(channel_id: int):
    try:
        channel = await bot.fetch_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            return False

        if bot.voice_clients:
            voice_client = bot.voice_clients[0]
            if voice_client.channel.id == channel.id and voice_client.is_connected():
                return True
            if voice_client.is_connected():
                await voice_client.disconnect()

        await channel.connect()
        print(f"Conectado com sucesso ao canal: {channel.name}")
        return True
    except Exception as e:
        print(f"Erro ao conectar ao canal de voz: {e}")
        return False

async def disconnect_voice():
    if bot.voice_clients:
        voice_client = bot.voice_clients[0]
        if voice_client.is_connected():
            await voice_client.disconnect()
            return True
    return False

async def voice_watchdog():
    await bot.wait_until_ready()
    while not bot.is_closed():
        if voice_channel_id:
            try:
                connected = bot.voice_clients and bot.voice_clients[0].is_connected()
                print(f"[watchdog] voice_channel_id={voice_channel_id}, connected={connected}")
                if not connected:
                    print("[watchdog] tentando reconectar à call...")
                    await connect_to_voice(voice_channel_id)
            except Exception as e:
                print(f"Watchdog erro: {e}")
        await asyncio.sleep(15)

@bot.event
async def on_ready():
    global voice_check_task
    print(f"Bot {bot.user.name} está online na nuvem!")
    if voice_check_task is None:
        voice_check_task = bot.loop.create_task(voice_watchdog())
    if voice_channel_id:
        await connect_to_voice(voice_channel_id)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != bot.user.id:
        return
    if before.channel is not None and after.channel is None and voice_channel_id:
        await asyncio.sleep(5)
        await connect_to_voice(voice_channel_id)

@bot.event
async def on_guild_available(guild):
    if voice_channel_id:
        await connect_to_voice(voice_channel_id)

@bot.command(name="join")
async def join(ctx):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
        return
    channel = ctx.author.voice.channel
    success = await connect_to_voice(channel.id)
    if success:
        global voice_channel_id
        voice_channel_id = channel.id
        await ctx.send(f"Entrei no canal de voz: {channel.name}")
    else:
        await ctx.send("Não consegui entrar no canal de voz.")

@bot.command(name="leave")
async def leave(ctx):
    if await disconnect_voice():
        global voice_channel_id
        voice_channel_id = None
        await ctx.send("Saí do canal de voz.")
    else:
        await ctx.send("Não estou em nenhum canal de voz agora.")

keep_alive()

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("A variável de ambiente DISCORD_TOKEN não está definida.")

bot.run(TOKEN)





