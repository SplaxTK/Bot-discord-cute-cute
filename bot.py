import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
import random

# Configuração das permissões do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessário para rastrear membros

bot = commands.Bot(command_prefix="!", intents=intents)

# ============================================
# SISTEMA DE MEMÓRIA
# ============================================

class MemorySystem:
    def __init__(self):
        self.data_file = "server_memory.json"
        self.memory = self.load_memory()
        self.last_joke_times = {}
    
    def load_memory(self):
        """Carrega a memória do arquivo JSON"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_memory(self):
        """Salva a memória no arquivo JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def get_user_profile(self, user_id):
        """Obtém ou cria perfil do usuário"""
        user_id_str = str(user_id)
        if user_id_str not in self.memory:
            self.memory[user_id_str] = {
                "nome": "",
                "personalidade": [],
                "entrada": datetime.now().isoformat(),
                "ultima_msg": datetime.now().isoformat(),
                "piadas_contadas": 0,
                "eventos": []
            }
            self.save_memory()
        return self.memory[user_id_str]
    
    def update_personality(self, user_id, trait):
        """Adiciona traço de personalidade ao usuário"""
        profile = self.get_user_profile(user_id)
        if trait not in profile["personalidade"]:
            profile["personalidade"].append(trait)
            if len(profile["personalidade"]) > 10:  # Limita a 10 traços
                profile["personalidade"].pop(0)
            self.save_memory()
    
    def add_event(self, user_id, event):
        """Adiciona um evento importante"""
        profile = self.get_user_profile(user_id)
        profile["eventos"].append({
            "descricao": event,
            "data": datetime.now().isoformat()
        })
        if len(profile["eventos"]) > 20:  # Limita a 20 eventos
            profile["eventos"].pop(0)
        self.save_memory()
    
    def get_time_in_server(self, user_id):
        """Calcula o tempo que o usuário está no servidor"""
        profile = self.get_user_profile(user_id)
        entrada = datetime.fromisoformat(profile["entrada"])
        tempo = datetime.now() - entrada
        return tempo

    def can_send_joke(self, user_id):
        """Impede que o bot envie piadas em excesso para o mesmo usuário."""
        user_id_str = str(user_id)
        now = datetime.now()
        last_time = self.last_joke_times.get(user_id_str)

        if last_time is None:
            self.last_joke_times[user_id_str] = now
            return True

        if now - last_time < timedelta(seconds=20):
            return False

        self.last_joke_times[user_id_str] = now
        return True
    
    def generate_inside_joke(self, user_id):
        """Gera uma piada interna baseada na personalidade do usuário"""
        profile = self.get_user_profile(user_id)
        personality = profile["personalidade"]
        
        if not personality:
            return None
        
        candidates = []
        for trait in personality:
            if trait in PERSONALITY_JOKES:
                candidates.extend(PERSONALITY_JOKES[trait])
        
        if not candidates:
            return f"🤖 O {profile['nome'] or 'usuário'} é tão legal que até os bots querem ser amigos!"
        
        joke_template = random.choice(candidates)
        return joke_template.format(nome=profile["nome"] or "usuário")

# Inicializa o sistema de memória
memory = MemorySystem()

PERSONALITY_JOKES = {
    "gamer": [
        "🎮 O {nome} é tão gamer que tentou dar alt+F4 na vida real!",
        "🎮 O {nome} joga tanto que até o controle pediu férias!",
        "🎮 O {nome} é tão gamer que o sofá virou console de guerra!",
        "🎮 O {nome} fala 'mais uma partida' até no banho!",
        "🎮 O {nome} é tão gamer que as horas passam voando... e o rank também!"
    ],
    "dorminhoco": [
        "😴 O {nome} dorme tanto que até o despertador pede pra dormir mais!",
        "😴 O {nome} é tão dorminhoco que o sono veio antes da mensagem!",
        "😴 O {nome} dorme com tanta vontade que até os sonhos pedem silêncio!",
        "😴 O {nome} é tão sonolento que acordou no meio do 'bom dia'!",
        "😴 O {nome} dorme tanto que o bot até ficou com sono de esperar!"
    ],
    "comilão": [
        "🍕 O {nome} comeu a pizza e o bot ficou com inveja!",
        "🍔 O {nome} é tão comilão que a fome chegou antes do horário!",
        "🥪 O {nome} faz uma refeição e chama de 'lanche rápido'!",
        "🍟 O {nome} come tão bem que até a geladeira faz carinho!",
        "🍰 O {nome} tem o talento de transformar qualquer mesa em buffet!"
    ],
    "trabalhador": [
        "💼 O {nome} trabalha tanto que merece um aumento de carisma!",
        "💼 O {nome} é tão trabalhador que o relógio pede licença!",
        "💼 O {nome} produz tanto que o café fica com inveja!",
        "💼 O {nome} trabalha com tanto foco que até o bot respeita!",
        "💼 O {nome} é tão profissional que até o descanso pediu prazo!"
    ],
    "engraçado": [
        "😂 O {nome} é tão engraçado que deveria pagar imposto de risada!",
        "😂 O {nome} faz piada tão bem que o chat quase quebra o servidor!",
        "😂 O {nome} é tão engraçado que até o silêncio ri!",
        "😂 O {nome} faz comentários que merecem aplauso e emoji de risada!",
        "😂 O {nome} tem humor tão bom que o bot ficou sem palavras!"
    ],
    "nerd": [
        "🤓 O {nome} é tão nerd que decodificou a mensagem secreta do bot!",
        "🤓 O {nome} sabe tanto que até o Google pede dicas!",
        "🤓 O {nome} é tão nerd que até o teclado pede autógrafo!",
        "🤓 O {nome} é tão inteligente que o bot aprende com ele!",
        "🤓 O {nome} é tão nerd que a curiosidade virou superpoder!"
    ],
    "músico": [
        "🎵 O {nome} toca tão bem que até os bots dançam!",
        "🎵 O {nome} tem tanto talento que a música pediu pra entrar na lista!",
        "🎵 O {nome} faz um som tão bom que a sala fica com clima!",
        "🎵 O {nome} canta tão bem que até o silêncio acompanha!",
        "🎵 O {nome} é tão musical que o bot quase pediu um solo!"
    ],
    "escritor": [
        "📝 O {nome} escreve tão bem que o bot virou fã!",
        "📝 O {nome} tem uma escrita tão boa que até os emojis ficam poéticos!",
        "📝 O {nome} escreve como se cada palavra tivesse alma!",
        "📝 O {nome} é tão criativo que a frase virou meme!",
        "📝 O {nome} escreve tão bem que até o bot quer um livro!"
    ],
    "fofo": [
        "💖 O {nome} é tão fofo que até o bot quer te abraçar!",
        "💖 O {nome} tem um jeito tão fofo que o chat derrete!",
        "💖 O {nome} é fofo de um jeito que faz qualquer um sorrir!",
        "💖 O {nome} é tão fofo que até a mensagem ganha carinho!",
        "💖 O {nome} tem energia tão doce que o bot fica comovido!"
    ],
    "curioso": [
        "🔍 O {nome} é tão curioso que até a dúvida pediu explicação!",
        "🔍 O {nome} pergunta tanto que o bot quase faz aula!",
        "🔍 O {nome} tem curiosidade tão grande que o universo fica atento!",
        "🔍 O {nome} é tão curioso que até o silêncio vira pergunta!",
        "🔍 O {nome} faz perguntas que deixam o chat pensando!"
    ],
    "otimista": [
        "🌤️ O {nome} é tão otimista que até o dia ruim ganha brilho!",
        "🌤️ O {nome} vê o lado bom de tudo, inclusive do bot!",
        "🌤️ O {nome} é tão positivo que o bom humor se multiplica!",
        "🌤️ O {nome} espalha esperança tanto que até o chat sorri!",
        "🌤️ O {nome} é tão otimista que até o 'talvez' parece certeza!"
    ],
    "introvertido": [
        "🤫 O {nome} é tão introvertido que até o silêncio tem respeito!",
        "🤫 O {nome} fala pouco, mas quando fala, o chat presta atenção!",
        "🤫 O {nome} é tão reservado que o bot respeita o espaço!",
        "🤫 O {nome} é tão calmo que o silêncio fica elegante!",
        "🤫 O {nome} é introvertido, mas tem uma presença gigante!"
    ],
    "criativo": [
        "🎨 O {nome} é tão criativo que até a ideia mais simples vira obra-prima!",
        "🎨 O {nome} tem tanta criatividade que o bot fica sem filtro!",
        "🎨 O {nome} cria tanto que o chat parece uma galeria!",
        "🎨 O {nome} é tão criativo que até os emojis viram arte!",
        "🎨 O {nome} transforma o comum em algo incrível!"
    ]
}

PERSONALITY_KEYWORDS = {
    "gamer": ["jogo", "jogar", "games", "gamer", "rpg", "fps", "moba", "play", "console", "steam", "rank"],
    "dorminhoco": ["sono", "dormir", "dormindo", "cama", "cansado", "noite", "acordei", "sonolento", "cochilo"],
    "comilão": ["comer", "comi", "fome", "pizza", "hamburguer", "lanche", "bebida", "bebi", "churrasco"],
    "trabalhador": ["trabalho", "trabalhar", "emprego", "estudo", "escritório", "deadline", "tarefa", "projeto"],
    "engraçado": ["risada", "kkk", "haha", "hahaha", "engraçado", "piada", "meme", "humor"],
    "nerd": ["programar", "código", "python", "javascript", "nerd", "tecnologia", "algoritmo", "debug", "terminal"],
    "músico": ["música", "tocar", "cantar", "instrumento", "som", "ritmo", "violão", "guitarra", "piano"],
    "escritor": ["escrever", "história", "livro", "poema", "texto", "roteiro", "redação", "conto"],
    "fofo": ["fofo", "cute", "adorável", "meigo", "lindo", "bonito", "carinho", "amor"],
    "curioso": ["curioso", "por que", "porque", "pergunta", "saber", "explorar", "entender"],
    "otimista": ["otimista", "esperança", "positivo", "melhor", "bom", "amanhã", "confiante"],
    "introvertido": ["quieto", "calmo", "reservado", "silêncio", "sozinho", "isolado", "pouco"],
    "criativo": ["criativo", "ideia", "inventar", "arte", "inspirado", "original", "imaginar"]
}

# ID do canal de voz
ID_DO_CANAL_DE_VOZ = 1238513896357232675

# ============================================
# EVENTOS DO BOT
# ============================================

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} está online!")
    print(f"Memória carregada: {len(memory.memory)} usuários")
    
    try:
        channel = await bot.fetch_channel(ID_DO_CANAL_DE_VOZ)
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f"Conectado com sucesso ao canal: {channel.name}")
        else:
            print("O ID fornecido não pertence a um canal de voz.")
    except Exception as e:
        print(f"Erro ao conectar na call: {e}")

@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    if len(message.content.strip()) < 3:
        return
    
    # Atualiza perfil do usuário
    user_id = message.author.id
    profile = memory.get_user_profile(user_id)
    profile["nome"] = message.author.display_name
    profile["ultima_msg"] = datetime.now().isoformat()
    memory.save_memory()
    
    # Analisa a mensagem para detectar traços de personalidade
    detect_personality(message.content, user_id)
    
    # Verifica eventos importantes
    await check_important_events(message)
    
    # Chance de contar uma piada interna, reduzida e com cooldown por usuário
    profile = memory.get_user_profile(user_id)
    trait_count = len(profile["personalidade"])
    joke_chance = 0.06 + min(0.08, 0.01 * trait_count)

    if random.random() < joke_chance and memory.can_send_joke(user_id):
        joke = memory.generate_inside_joke(user_id)
        if joke:
            await message.channel.send(joke)
            profile = memory.get_user_profile(user_id)
            profile["piadas_contadas"] += 1
            memory.save_memory()
    
    # Processa comandos
    await bot.process_commands(message)

def detect_personality(text, user_id):
    """Detecta traços de personalidade baseado no texto de forma mais inteligente"""
    text_lower = text.lower()
    scores = {}

    for trait, keywords in PERSONALITY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text_lower:
                score += 2 if " " in keyword else 1
        if score > 0:
            scores[trait] = score

    if not scores:
        return

    top_traits = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:3]
    for trait, _ in top_traits:
        memory.update_personality(user_id, trait)

async def check_important_events(message):
    """Verifica eventos importantes (ex: aniversário de entrada)"""
    user_id = message.author.id
    profile = memory.get_user_profile(user_id)
    
    # Verifica se é aniversário de entrada (6 meses)
    tempo = memory.get_time_in_server(user_id)
    if tempo.days > 0 and tempo.days % 180 == 0 and tempo.days < 190:
        anos = tempo.days // 365
        meses = (tempo.days % 365) // 30
        
        if anos > 0:
            msg = f"🎉 {message.author.display_name} está no servidor há {anos} ano(s) e {meses} mês(es)! Parabéns!"
        else:
            msg = f"🎉 {message.author.display_name} está no servidor há {meses} mês(es)! Que legal!"
        
        await message.channel.send(msg)
        memory.add_event(user_id, f"Aniversário de entrada: {tempo.days} dias")

@bot.event
async def on_member_join(member):
    """Quando um novo membro entra no servidor"""
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"👋 Bem-vindo {member.mention}! Eu sou o bot com memória, vou lembrar de você!")
    
    # Cria perfil do novo membro
    profile = memory.get_user_profile(member.id)
    profile["nome"] = member.display_name
    memory.add_event(member.id, "Entrou no servidor")
    memory.save_memory()

# ============================================
# COMANDOS
# ============================================

@bot.command(name="perfil")
async def perfil(ctx, member: discord.Member = None):
    """Mostra o perfil de um usuário"""
    if member is None:
        member = ctx.author
    
    profile = memory.get_user_profile(member.id)
    tempo = memory.get_time_in_server(member.id)
    
    embed = discord.Embed(
        title=f"📊 Perfil de {member.display_name}",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Tempo no servidor",
        value=f"{tempo.days} dias",
        inline=True
    )
    
    embed.add_field(
        name="Personalidade",
        value=", ".join(profile["personalidade"]) or "Ainda descobrindo...",
        inline=True
    )
    
    embed.add_field(
        name="Piadas contadas",
        value=str(profile["piadas_contadas"]),
        inline=True
    )
    
    if profile["eventos"]:
        ultimos_eventos = profile["eventos"][-3:]
        eventos_texto = "\n".join([f"• {e['descricao']}" for e in ultimos_eventos])
        embed.add_field(
            name="Últimos eventos",
            value=eventos_texto,
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name="personalidades")
async def listar_personalidades(ctx):
    """Mostra as personalidades disponíveis"""
    valid_traits = ["gamer", "dorminhoco", "comilão", "trabalhador", "engraçado", "nerd", "músico", "escritor", "fofo", "curioso", "otimista", "introvertido", "criativo"]
    await ctx.send(f"🧠 Personalidades disponíveis: {', '.join(valid_traits)}")

@bot.command(name="personalidade")
async def adicionar_personalidade(ctx, trait: str):
    """Adiciona um traço de personalidade manualmente"""
    valid_traits = ["gamer", "dorminhoco", "comilão", "trabalhador", "engraçado", "nerd", "músico", "escritor", "fofo", "curioso", "otimista", "introvertido", "criativo"]
    
    if trait.lower() not in valid_traits:
        await ctx.send(f"Traços válidos: {', '.join(valid_traits)}")
        return
    
    memory.update_personality(ctx.author.id, trait.lower())
    await ctx.send(f"✅ Personalidade '{trait}' adicionada ao seu perfil!")

@bot.command(name="piada")
async def piada(ctx, member: discord.Member = None):
    """Conta uma piada interna para alguém"""
    if member is None:
        member = ctx.author
    
    joke = memory.generate_inside_joke(member.id)
    if joke:
        await ctx.send(joke)
        profile = memory.get_user_profile(member.id)
        profile["piadas_contadas"] += 1
        memory.save_memory()
    else:
        await ctx.send(f"😅 Não conheço {member.display_name} o suficiente ainda!")

@bot.command(name="eventos")
async def eventos(ctx, member: discord.Member = None):
    """Mostra eventos importantes de um usuário"""
    if member is None:
        member = ctx.author
    
    profile = memory.get_user_profile(member.id)
    
    if not profile["eventos"]:
        await ctx.send(f"📭 {member.display_name} ainda não tem eventos registrados.")
        return
    
    embed = discord.Embed(
        title=f"📅 Eventos de {member.display_name}",
        color=discord.Color.gold()
    )
    
    eventos_texto = "\n".join([f"• {e['descricao']}" for e in profile["eventos"][-10:]])
    embed.description = eventos_texto
    
    await ctx.send(embed=embed)

# ============================================
# INICIAR BOT
# ============================================

# Cole o TOKEN do seu bot entre as aspas
bot.run("MTUzMTg3NDA5NzM4NDkxNTAzNQ.GtQD0w.YtdTolOhPxtG645cni-R-p2gNUhjWBttqIzZ2M")
