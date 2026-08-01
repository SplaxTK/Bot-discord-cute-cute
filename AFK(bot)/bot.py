import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import random

# ============================================
# VERSÃO E CONTROLE DE DEPLOY
# ============================================
VERSION = "2.0" 
DEPLOY_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

CHANNEL_ID = 1397347889835147449

# ============================================
# CONFIGURAÇÃO DO BOT
# ============================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ============================================
# PERSONALITY_KEYWORDS
# ============================================

PERSONALITY_KEYWORDS = {
    "gamer": ["jogo", "jogar", "games", "gamer","game", "rpg", "fps", "moba", "play", "console", "steam", "rank","gg", "noob", "farmar", "nerf","nerfs", "buff","buffs", "carry", "feedar","tryhard", "casual", "rage", "bait", "kickar", "skin", "drop", "grindar","main", "off-meta", "pog", "clutch", "kda","ovw","over","jogar"],

    "dorminhoco": ["sono", "dormir", "dormindo", "cama", "cansado", "noite", "acordei", "sonolento", "cochilo", "sono", "zZz", "cochilar", "cama", "travesseiro", "roncar", "preguiça","preguica","apagar", "madrugada", "despertar", "soninho", "bocejar","cobertor", "descansar", "sono eterno", "dormi demais", "pesadelo","soneca", "ninar"],

    "comilão": ["comer","banana","pao", "comi", "fome", "pizza", "hamburguer", "lanche", "bebida", "bebi", "churrasco","fome", "comer", "bucho", "lanche", "janta", "pão", "pizza","hambúrguer","hamburguer", "batata", "doce", "salgado", "refri", "gordura","gororoba", "ralar", "mastigar", "prato", "boca"],

    "trabalhador": ["trabalho", "trabalhar", "emprego", "estudo", "escritório","escritorio", "deadline", "tarefa", "projeto","correria", "prazo", "meta", "produzir", "esforço", "esforco", "entrega", "foco","trampo", "batalhar", "vencer", "expediente", "home office", "reunião","planilha", "hora extra", "merecido", "descanso", "projeto","resultado"],

    "engraçado": ["risada", "kkk", "haha", "hahaha", "engraçado", "piada", "meme", "humor","kkkk","ksksk","kkkj","*risos*","rsrsrs","rsrs", "haha", "meme", "zuera", "trolar", "piada", "cômico","comico","risada", "gargalhada", "palhaço","palhaco", "engraçadinho", "engracadinho","humor", "sarcasmo","ironia", "tirar sarro", "brincadeira", "morri", "kkkkkk", "risos"],

    "nerd": ["programar", "código", "codigo","c#","c++", "python","java", "javascript", "nerd", "tecnologia", "algoritmo", "debug", "terminal", "código","codigo", "bug", "deploy","commit", "script", "linux","terminal", "teoria", "anime", "mangá", "manga", "rpg", "dado", "nível", "nivel", "level", "farm","stats", "wiki", "tutorial", "geek","nota", "acorde"],

    "músico": ["música", "musica", "tocar", "cantar", "instrumento", "som", "ritmo", "violão", "violao",  "guitarra", "piano", "nota", "acorde", "melodia", "ritmo", "tom", "instrumento", "afinar","ensaio", "show", "palco", "cifra", "partitura", "som", "grave", "agudo","batida", "compasso", "harmonia", "cover", "autoral"],

    "escritor": ["escrever", "história", "historia", "livro", "poema", "texto", "roteiro", "redação", "redacao", "conto", "texto", "capítulo", "capitulo", "personagem", "enredo", "rascunho","publicar","leitor", "trama","final","narrar", "fanfic", "original", "livro", "ebook"],

    "fofo": ["fofo", "cute", "cuti", "adorável", "meigo", "lindo", "bonito", "carinho", "amor","lindo", "gato", "bonito", "cute-cute", "adorável", "adoravel","fofura", "pets","flores", "sorriso", "coração", "beijo", "abração", "carinho", "doce", "amorzinho", "fofo demais", "mimo", "pelúcia","pelucia", "rasgar", "encanto"],
    
        "fofo": ["fofo", "cute", "adorável", "adoravel", "meigo", "lindo", "bonito", "carinho", "amor", "gato", "fofura", "pets", "flores", "sorriso", "coração", "coracao", "beijo", "abraço", "abraco", "doce", "amorzinho", "fofo demais", "mimo", "pelúcia", "pelucia", "rasgar", "encanto"],
    
    "curioso": ["curioso", "por que", "porque", "pergunta", "saber", "explorar", "entender", "como", "explica", "detalhe", "curiosidade", "investigar", "descobrir", "novidade", "pesquisar", "fato", "teoria", "será", "sera", "interessante", "desvendar", "segredo", "mistério", "misterio", "fuçar", "fucar", "insight"],
    
    "otimista": ["otimista", "esperança", "esperanca", "positivo", "melhor", "bom", "amanhã", "amanha", "confiante", "quieto", "na minha", "sem energia", "social bateria", "melhor sozinho", "observar", "pensar", "falar pouco", "tímido", "timido", "reservado", "aconchego", "dentro de casa", "livro", "headset", "evitar", "multidão", "multidao", "silêncio", "silencio", "reflexão", "reflexao", "interior", "não fui", "nao fui"],
    
    "introvertido": ["quieto", "calmo", "reservado", "silêncio", "silencio", "sozinho", "isolado", "pouco", "na minha", "sem energia", "social bateria", "melhor sozinho", "observar", "pensar", "falar pouco", "tímido", "timido", "aconchego", "dentro de casa", "livro", "headset", "evitar", "multidão", "multidao", "reflexão", "reflexao", "interior", "não fui", "nao fui"],
    
    "criativo": ["criativo", "ideia", "inventar", "arte", "inspirado", "original", "imaginar", "inovar", "criar", "desenho", "pintura", "projeto", "diferente", "genial", "inspo", "conceito", "estilo", "flow", "imaginação", "imaginacao", "brainstorm", "loucura", "obra", "conceitual", "único", "unico"],
    
    "preguiçoso": ["dps", "depois", "faço não", "faco nao", "muito trampo", "preguiça", "preguica", "deitar", "sofá", "sofa", "dar mole", "enrolar", "remoto", "descansar", "sem saco", "coisas chatas", "deixa", "amanhã", "amanha", "ai que", "não agora", "nao agora", "cansei", "melhor não", "melhor nao", "foda-se", "fodase"],
    
    "depressivo": ["triste", "vazio", "sem ânimo", "sem animo", "pra que", "solidão", "solidao", "escuro", "cansaço", "cansaco", "desânimo", "desanimo", "não importa", "nao importa", "foda", "bad", "tédio", "tedio", "angústia", "angustia", "chorar", "sem sentido", "peso", "nuvem", "fracasso", "sofrer", "no fundo"],
    
    "cafeinado": ["café", "cafe", "energia", "elétrico", "eletrico", "shake", "acordar", "pilha", "vibrante", "focado", "insônia", "insonia", "xícara", "xicara", "expresso", "cafeína", "cafeina", "turbo", "agitação", "agitacao", "nervoso", "ansioso", "produzir", "correr", "explodir"],
    
    "furry": ["paw", "woof", "fursuit", "pelo", "cauda", "orelha", "furry", "fursona", "convenção", "convencao", "artist", "commissions", "fluffy", "uwu", "rawr", "beast", "animal", "patas", "snout"],
    
    "baitola": ["eita", "nossa", "cruzes", "bixona", "lacrar", "arrasar", "diva", "princesa", "tchutchuca", "bafão", "bafao", "trend", "desconstruir", "amigue", "mana", "todes", "comportamento", "afeto", "cuidado", "sensível", "sensivel", "espalhar"],
    
    "fofoqueiro": ["ouviu", "falaram", "sabe o que", "disse", "fofoca", "descobri", "segredo", "revelar", "fofocar", "saber", "detalhe", "quem", "com quem", "onde", "quando", "como", "aquela", "história", "historia", "fuxico", "fofoquinha"],
    
    "sedentário": ["parado", "sofá", "sofa", "maratona", "assistir", "cobertor", "snack", "mexer pouco", "sem treino", "relax", "de boa", "acomodado", "conforto", "não corro", "nao corro", "só deitado", "so deitado", "controle", "streaming", "pouco movimento", "vida mansa", "sem esforço", "sem esforco", "não saio", "nao saio"],
    
    "apaixonado": ["amor", "paixão", "paixao", "coração", "coracao", "lindo", "perfeito", "meu bem", "mimar", "beijo", "abraço", "abraco", "sentir", "ciúmes", "ciumes", "intenso", "romance", "declarar", "cuidar", "sonhar", "juntos", "eterno", "viu", "fofo dm"],
    
    "pão-duro": ["economizar", "barato", "desconto", "promoção", "promocao", "gastar pouco", "pagar", "meio a meio", "gratuito", "cupom", "renda", "sobrar", "reaproveitar", "moderação", "moderacao", "não vai", "nao vai", "caro", "fora do orçamento", "fora do orcamento", "ajustar", "planejar", "fazer render"],
    
    "mentiroso": ["confia", "juro", "verdade", "garanto", "pode crer", "não minto", "nao minto", "fato", "viu", "aconteceu", "real", "menti", "exagero", "conto", "fake", "invento", "ficção", "ficcao", "maluquice", "nunca", "sempre"],
    
    "pão-de-queijo": ["mineiro", "queijinho", "gostoso", "comer", "receita", "frito", "assado", "café", "cafe", "lanche", "tradição", "tradicao", "delícia", "delicia", "mineirês", "mineires", "uai", "sô", "so", "trem", "bão", "bao", "roça", "roca", "queijada", "polvilho", "sabor"],
    
    "viciado-em-série": ["episódio", "episodio", "próximo", "proximo", "tempada", "spoiler", "maratona", "personagem", "não parar", "nao parar", "ansiedade", "cliffhanger", "final", "ep", "netflix", "hbo", "disney", "assistir", "teoria", "review", "curtir", "viciar", "binge"],
    
    "gourmet": ["artesanal", "premium", "gourmet", "sabor", "sommelier", "harmonizar", "ingrediente", "massa", "cooking", "apresentação", "apresentacao", "nutrir", "leve", "sofisticado", "tendência", "tendencia", "fusion", "orgânico", "organico", "vegano", "gluten-free", "paladar", "exclusivo"],
    
    "chato": ["cansativo", "sério", "serio", "lógico", "logico", "óbvio", "obvio", "dramático", "dramatico", "reclamar", "pessoal", "técnico", "tecnico", "formal", "enjoado", "sempre", "nunca", "burocracia", "regra", "certo", "errado", "frescura", "desgastante"],
    
    "sortudo": ["sorte", "caramba", "azar", "deu certo", "coincidência", "coincidencia", "destino", "sorteio", "ganhar", "prêmio", "premio", "azarão", "azarao", "torcer", "fé", "fe", "aconteceu", "milagre", "incrível", "incrivel", "acho que", "benção", "bencao", "lucro", "quase", "ufa"],
    
    "ciumento": ["quem é", "quem e", "com quem", "conversando", "olhou", "curtiu", "seguiu", "amigo", "confiar", "desconfiar", "ciúmes", "ciumes", "proteger", "meu", "só meu", "so meu", "inseguro", "estranhar", "perguntar", "checar", "perturbar", "monitorar", "posse"],
    
    "grosseiro": ["aff", "vtnc", "foda-se", "fodase", "que se dane", "ignorar", "grosso", "rude", "sem educação", "sem educacao", "respirar", "sincericídio", "sincericidio", "direto", "bruto", "sem filtro", "corte", "ofender", "desrespeito", "tratar mal", "peito", "virar as costas", "grosseria"],
    
    "tímido": ["vergonha", "sem jeito", "não sei", "nao sei", "hesitar", "corar", "evitar olho", "falar baixo", "não quero chamar atenção", "nao quero chamar atencao", "dar um jeito", "enrolar", "amigável", "amigavel", "tímidez", "timidez", "disfarçar", "disfarcar", "observar", "não me nota", "nao me nota", "sumir", "desviar", "sussurrar", "sorrir sem graça", "ansiedade"],
    
    "esquecido": ["esqueci", "onde", "quando", "o que", "deixa", "anotar", "memória", "memoria", "branco", "sumiu", "perdi", "não lembro", "nao lembro", "confundir", "desatenção", "desatencao", "distraído", "distraido", "alzheimer", "repetir", "cadê", "cade", "hã", "ha", "esquecimento", "falha"],
    
    "marrento": ["sou assim", "melhor", "sabe mais", "arrogante", "desafiar", "provocar", "superior", "convencido", "bancar", "falar alto", "peitar", "marra", "estilo", "cabeça dura", "cabeca dura", "não aceito", "nao aceito", "vencedor", "tô na frente", "to na frente", "dominar", "competir", "vencer"],
    
    "fanático": ["melhor", "único", "unico", "verdadeiro", "fã", "fa", "defender", "torcer", "time", "teoria", "consistente", "sempre certo", "inabalável", "inabalavel", "puro", "cultuar", "guru", "mestre", "sectar", "paixão", "paixao", "incansável", "incansavel"],
    
    "pistoleiro": ["peitar", "tretar", "confrontar", "brigar", "gritar", "bater", "ameaçar", "ameacar", "atirador", "pistola", "rápido", "rapido", "provocar", "dominar", "medo", "coragem", "violento", "justiça", "justica", "vingança", "vinganca", "perigoso", "desafio"],
    
    "famosinho": ["famoso", "influencer", "seguidor", "engajamento", "trend", "nota", "mídia", "midia", "holofote", "fama", "vanity", "brand", "publicidade", "story", "patrocínio", "patrocinio", "prateleira", "visibilidade", "destaque", "glamour", "celebridade"],
    
    "louco": ["loucura", "doido", "surreal", "viajar", "chapado", "sem noção", "sem nocao", "explodir", "insano", "doidivanas", "piração", "piracao", "desvairado", "sem freio", "impulso", "coringar", "doido de pedra", "girar", "perder o controle", "maluco", "alucinado", "pasmo"],
    
    "perfeccionista": ["ajustar", "detalhe", "polir", "excelência", "excelencia", "precisão", "precisao", "corrigir", "revisar", "capricho", "perfeito", "refinar", "exigente", "padrão", "padrao", "clean", "simetria", "organizar", "cronometrar", "qualidade", "inspetor", "minucioso", "tudo certinho"],
    
    "barulhento": ["alto", "som", "explosão", "explosao", "gritaria", "batida", "estrondo", "vibração", "vibracao", "tumulto", "buzina", "música", "musica", "festança", "festanca", "bateção", "batecao", "barulheira", "algazarra", "zoada", "rebuliço", "rebulico", "escândalo", "escandalo", "trovão", "trovao", "avalanche", "ruído", "ruido"],
    
    "calmo": ["paz", "tranquilo", "serenar", "respirar", "meditar", "devagar", "leveza", "harmonia", "descanso", "quietude", "calmaria", "brando", "suave", "controlar", "sem pressa", "observar", "flutuar", "consciente", "relaxado"],
    
    "apaixonado-por-bot": ["bot", "comando", "automático", "automatico", "script", "trigger", "reply", "custom", "programar", "integração", "integracao", "api", "webhook", "automatizar", "help", "prefiro bot", "humano?", "robô", "robo", "engenharia", "resposta", "trigger word", "dev"],
    
    "desligado": ["hã", "ha", "o que", "tô fora", "to fora", "viajando", "desatento", "não vi", "nao vi", "perdido", "sonso", "distrair", "fora de si", "sem noção", "sem nocao", "confuso", "desligar", "ignorar", "não captei", "nao captei", "alienado", "offline", "neutro", "sem reação", "sem reacao", "huh"],
    
    "cabuloso": ["cabuloso", "legal", "maneiro", "show", "top", "bacana", "irado", "pesado", "forte", "impactante", "insano", "sensacional", "fenomenal", "sinistro", "da hora", "brabo", "monstro", "animal", "brutal", "cabulosão", "cabulosao"],
    
    "místico": ["energia", "espiritual", "cósmico", "cosmico", "vibração", "vibracao", "aura", "universo", "signo", "tarô", "taro", "cristais", "meditar", "guia", "sagrado", "ritual", "astral", "conexão", "conexao", "intuição", "intuicao", "luz", "sombra", "equilíbrio", "equilibrio"],
    
    "exibido": ["olha", "vídeo", "video", "foto", "olha eu", "ganhei", "tenho", "comprei", "conquista", "destaque", "glamour", "holofote", "atraente", "mostrar", "postar", "story", "selfie", "novo", "melhor", "primeiro", "exibir"],
    
    "crítico": ["avaliar", "julgar", "opinar", "fundamentar", "análise", "analise", "pontos fortes", "fracos", "coerência", "coerencia", "estrutura", "profundo", "perspectiva", "criticar", "exigente", "detalhar", "revisar", "argumento", "lógica", "logica", "contradição", "contradicao", "veracidade", "critério", "criterio"],
    
    "zé-ruela": ["zé", "ze", "ruela", "pé rapado", "pe rapado", "relaxado", "descolado", "malandro", "sagaz", "vira-lata", "jogar conversa", "sem compromisso", "gambiarra", "jeitinho", "andarilho", "improvisar", "zoeira", "trambique", "desenrolado", "praiano", "caiu na zoeira"],
    
    "emocionado": ["choro", "lágrima", "lagrima", "sensível", "sensivel", "tocado", "emoção", "emocao", "forte", "memórias", "memorias", "saudade", "impacto", "profundo", "verdade", "real", "sentir", "vibração", "vibracao", "história", "historia", "humano", "perda"],
    
    "fanfarrão": ["fanfarrão", "fanfarrao", "gabar", "se achar", "contar vantagem", "exagerar", "bravata", "falsa coragem", "enganação", "enganacao", "blefar", "jogar verde", "aparecer", "ostentar", "fantasia", "personagem", "herói", "heroi", "farsa", "carnaval", "teatral", "aparentar"],
    
    "#@$%": ["merda", "porra", "caralho", "puta", "foda", "vtnc", "filho da puta", "desgraca", "inferno", "buceta", "pau no cu", "caceta", "pqp", "vai se fuder", "arrombado", "escroto", "babaca", "otario", "xingamento", "krl", "vsfd", "tnc", "fdp", "vai tomar no cu", "desgraça", "desgraca", "otário", "otario"]
}

# ============================================
# PERSONALITY_JOKES
# ============================================

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
    ],
    "preguiçoso": [
        "🛋️ O {nome} é tão preguiçoso que até o sofá cansou de esperar!",
        "🛋️ O {nome} tem preguiça até de ter preguiça!",
        "🛋️ O {nome} é tão parado que o relógio desistiu de contar!",
        "🛋️ O {nome} demora tanto que o bot já foi e voltou!",
        "🛋️ O {nome} é tão preguiçoso que o 'depois' virou estilo de vida!"
    ],
    "depressivo": [
        "🌧️ O {nome} está tão pra baixo que até o bot ficou triste!",
        "🌧️ O {nome} vê o copo meio vazio... e o copo inteiro também!",
        "🌧️ O {nome} é tão depressivo que a música triste pede pra animar ele!",
        "🌧️ O {nome} está tão melancólico que até as nuvens têm dó!",
        "🌧️ O {nome} é tão negativo que o 'bom dia' vira 'mais um dia'!"
    ],
    "cafeinado": [
        "☕ O {nome} é tão cafeinado que o café pede pra ele desacelerar!",
        "☕ O {nome} toma tanto café que já virou café com leite!",
        "☕ O {nome} é tão elétrico que a xícara treme junto!",
        "☕ O {nome} tem tanto café no sangue que o coração bate samba!",
        "☕ O {nome} é tão cafeinado que até o bot ficou acelerado!"
    ],
    "furry": [
        "🐾 O {nome} é tão furry que o cachorro do vizinho pede autógrafo!",
        "🐾 O {nome} tem tanto pelo que a máquina de tosa pediu arrego!",
        "🐾 O {nome} é tão furry que até o lobo mau pede dicas de estilo!",
        "🐾 O {nome} late tão bem que o bot quase entendeu!",
        "🐾 O {nome} é tão furry que a ração virou comida gourmet!"
    ],
    "baitola": [
        "🌈 O {nome} é tão baitola que o arco-íris pediu pose!",
        "🌈 O {nome} tem tanta 'frescura' que a flor ficou com inveja!",
        "🌈 O {nome} é tão delicado que até a borboleta pede licença!",
        "🌈 O {nome} arrasa tanto que a passarela pediu música!",
        "🌈 O {nome} é tão 'vida loka' que o Boy George é fã!"
    ],
    "fofoqueiro": [
        "📢 O {nome} é tão fofoqueiro que o telefone sem fio virou radio novela!",
        "📢 O {nome} conta tanto segredo que até o bot pediu spoiler!",
        "📢 O {nome} é tão fofoqueiro que a fofoca virou esporte nacional!",
        "📢 O {nome} sabe tanto da vida alheia que merece um prêmio!",
        "📢 O {nome} é tão fofoqueiro que até o vento para pra ouvir!"
    ],
    "sedentário": [
        "🪑 O {nome} é tão sedentário que o sofá tem nome próprio!",
        "🪑 O {nome} se move tanto que o Google Maps pediu ajuda!",
        "🪑 O {nome} é tão parado que o controle remoto se sente culpado!",
        "🪑 O {nome} fica tão sentado que a cadeira pediu aumento!",
        "🪑 O {nome} é tão sedentário que a academia desistiu de ligar!"
    ],
    "apaixonado": [
        "❤️ O {nome} é tão apaixonado que até o coração do bot acelerou!",
        "❤️ O {nome} ama tanto que o romantismo virou doença!",
        "❤️ O {nome} é tão amoroso que o chat virou novela das 8!",
        "❤️ O {nome} tem tanto amor que o coração pede desconto!",
        "❤️ O {nome} é tão apaixonado que até o Tinder deu like!"
    ],
    "pão-duro": [
        "💰 O {nome} é tão mão de vaca que o bolso pede esmola!",
        "💰 O {nome} economiza tanto que até o dinheiro pede pra sair!",
        "💰 O {nome} é tão pão-duro que compra água e reclama do peso!",
        "💰 O {nome} gasta tão pouco que o cartão entrou em depressão!",
        "💰 O {nome} é tão econômico que o troco pede desconto!"
    ],
    "mentiroso": [
        "🤥 O {nome} mente tanto que o nariz virou Pinóquio 2.0!",
        "🤥 O {nome} é tão mentiroso que até a verdade pediu provas!",
        "🤥 O {nome} conta tanta mentira que a fake news virou fã!",
        "🤥 O {nome} é tão criativo pra mentir que merece um Oscar!",
        "🤥 O {nome} é tão mentiroso que o bot desconfia até do 'oi'!"
    ],
    "pão-de-queijo": [
        "🧀 O {nome} é tão pão-de-queijo que Mineirão pediu adoção!",
        "🧀 O {nome} é tão gostoso que o café pediu bis!",
        "🧀 O {nome} é tão pão-de-queijo que derrete na boca e no coração!",
        "🧀 O {nome} tem tanto recheio que a massa pede socorro!",
        "🧀 O {nome} é tão tradicional que o queijo pede desconto!"
    ],
    "viciado-em-série": [
        "📺 O {nome} é tão viciado em série que a Netflix pediu pra ele dar pausa!",
        "📺 O {nome} maratona tanto que o controle pede férias!",
        "📺 O {nome} é tão viciado que o próximo episódio já tem nome!",
        "📺 O {nome} vê série tão rápido que a temporada pede intervalo!",
        "📺 O {nome} é tão fã que a TV virou segundo lar!"
    ],
    "gourmet": [
        "🍽️ O {nome} é tão gourmet que o salgadinho vira entrada!",
        "🍽️ O {nome} transforma miojo em prato de estrela Michelin!",
        "🍽️ O {nome} é tão refinado que a água tem notas de degustação!",
        "🍽️ O {nome} tempera tão bem que até o sal pede bis!",
        "🍽️ O {nome} é tão gourmet que o pão com ovo vira brunch!"
    ],
    "chato": [
        "😒 O {nome} é tão chato que o silêncio pede pelo amor de Deus!",
        "😒 O {nome} reclama tanto que até o bot pediu queixa!",
        "😒 O {nome} é tão chato que o tédio virou entretenimento!",
        "😒 O {nome} é tão implicante que o espelho se recusa a refletir!",
        "😒 O {nome} é tão chato que a paciência virou mito!"
    ],
    "sortudo": [
        "🍀 O {nome} é tão sortudo que a sorte pediu pra ele parar!",
        "🍀 O {nome} ganha tanto que o azar se demitiu!",
        "🍀 O {nome} é tão sortudo que o bilhete de loteria é CPF!",
        "🍀 O {nome} atrai tanta sorte que o trevo de quatro folhas fica com ciúmes!",
        "🍀 O {nome} é tão sortudo que a desgraça passou reto!"
    ],
    "ciumento": [
        "😠 O {nome} é tão ciumento que o próprio reflexo é suspeito!",
        "😠 O {nome} vigia tanto que até o bot pediu senha!",
        "😠 O {nome} é tão ciumento que o olho fica pesado de tanto olhar!",
        "😠 O {nome} desconfia tanto que a sombra virou rival!",
        "😠 O {nome} é tão ciumento que o ciúme tem ciúme dele!"
    ],
    "grosseiro": [
        "😤 O {nome} é tão grosseiro que o bom dia saiu xingando!",
        "😤 O {nome} fala tão mal que até o dicionário se ofendeu!",
        "😤 O {nome} é tão rude que a educação pediu demissão!",
        "😤 O {nome} trata tão mal que o tratamento virou agressão!",
        "😤 O {nome} é tão grosseiro que a gentileza entrou em luto!"
    ],
    "timido": [
        "😳 O {nome} é tão tímido que a sombra se escondeu!",
        "😳 O {nome} fala tão baixo que o próprio eco não ouve!",
        "😳 O {nome} é tão tímido que a timidez ganhou timidez!",
        "😳 O {nome} se esconde tanto que a invisibilidade pediu dicas!",
        "😳 O {nome} é tão tímido que até o anonimato tem vergonha!"
    ],
    "esquecido": [
        "🤔 O {nome} é tão esquecido que esqueceu o próprio nome na lista!",
        "🤔 O {nome} esquece tanto que até o lembrete pediu lembrança!",
        "🤔 O {nome} é tão esquecido que a memória virou lenda!",
        "🤔 O {nome} esqueceu onde guardou o esquecimento!",
        "🤔 O {nome} é tão esquecido que o post-it se sente inútil!"
    ],
    "marrento": [
        "😎 O {nome} é tão marrento que o espelho se curvou!",
        "😎 O {nome} se acha tanto que o ego tem CNPJ!",
        "😎 O {nome} é tão brabo que o respeito pede desconto!",
        "😎 O {nome} anda tão na moda que a passarela virou rua!",
        "😎 O {nome} é tão marrento que a humildade tomou chá de sumiço!"
    ],
    "fanático": [
        "🔥 O {nome} é tão fanático que o time pediu espaço!",
        "🔥 O {nome} defende tanto que a torcida virou religião!",
        "🔥 O {nome} é tão apaixonado que o escudo virou tatuagem!",
        "🔥 O {nome} vibra tanto que o estádio sentiu inveja!",
        "🔥 O {nome} é tão fanático que a rivalidade tem nome próprio!"
    ],
    "pistoleiro": [
        "🔫 O {nome} é tão pistoleiro que o bang bang pediu música!",
        "🔫 O {nome} mira tão bem que o alvo pediu arrego!",
        "🔫 O {nome} é tão rápido que a bala perdeu a vez!",
        "🔫 O {nome} atira tão bem que o faroeste virou piada!",
        "🔫 O {nome} é tão pistoleiro que o duelo tem fila!"
    ],
    "famosinho": [
        "⭐ O {nome} é tão famosinho que o anonimato pediu foto!",
        "⭐ O {nome} é tão estrela que a fama virou sobrenome!",
        "⭐ O {nome} é tão conhecido que o desconhecido pediu apresentação!",
        "⭐ O {nome} tem tanto hype que o holofote pediu licença!",
        "⭐ O {nome} é tão famosinho que o Instagram pediu exclusividade!"
    ],
    "louco": [
        "🤪 O {nome} é tão louco que a sanidade pediu música!",
        "🤪 O {nome} viaja tanto que o GPS se perdeu!",
        "🤪 O {nome} é tão doido que a realidade pediu licença!",
        "🤪 O {nome} tem tanta criatividade que o mundo real é muito pequeno!",
        "🤪 O {nome} é tão louco que a razão virou exceção!"
    ],
    "perfeccionista": [
        "✨ O {nome} é tão perfeccionista que o 'quase' virou xingamento!",
        "✨ O {nome} ajusta tanto que o relógio pediu calma!",
        "✨ O {nome} é tão detalhista que o detalhe tem detalhe!",
        "✨ O {nome} revisa tanto que o erro pediu desculpas!",
        "✨ O {nome} é tão perfeccionista que o próprio Deus pediu revisão!"
    ],
    "barulhento": [
        "📢 O {nome} é tão barulhento que o silêncio pediu mudança!",
        "📢 O {nome} faz tanto barulho que a vizinhança virou banda!",
        "📢 O {nome} é tão alto que o volume pediu pra baixar!",
        "📢 O {nome} fala tão forte que o eco pediu espaço!",
        "📢 O {nome} é tão barulhento que o som virou personagem!"
    ],
    "calmo": [
        "😌 O {nome} é tão calmo que a tempestade pediu terapia!",
        "😌 O {nome} é tão tranquilo que o caos virou amigo!",
        "😌 O {nome} respira tão fundo que a paz pediu meditação!",
        "😌 O {nome} é tão sereno que o estresse pediu demissão!",
        "😌 O {nome} é tão calmo que a pressa virou história!"
    ],
    "apaixonado-por-bot": [
        "🤖 O {nome} é tão apaixonado por bot que o coração virou código!",
        "🤖 O {nome} ama tanto bots que o Tinder deu match com IA!",
        "🤖 O {nome} é tão fã de robôs que o amor é binário!",
        "🤖 O {nome} trocaria humanos por bots sem pensar duas vezes!",
        "🤖 O {nome} é tão apaixonado por bots que o coração é uma CPU!"
    ],
    "desligado": [
        "🔌 O {nome} é tão desligado que o interruptor deu risada!",
        "🔌 O {nome} perde o foco tanto que até o wi-fi caiu!",
        "🔌 O {nome} é tão avoado que a nuvem tem dó!",
        "🔌 O {nome} desconecta tanto que a energia pediu recarga!",
        "🔌 O {nome} é tão desligado que o bot quase desistiu!"
    ],
    "cabuloso": [
        "🔥 O {nome} é tão cabuloso que o perigo virou fã!",
        "🔥 O {nome} é tão perigoso que o cuidado tem medo!",
        "🔥 O {nome} tem tanta atitude que o respeito é automático!",
        "🔥 O {nome} é tão cabuloso que o crime virou piada!",
        "🔥 O {nome} é tão sinistro que o medo pediu abrigo!"
    ],
    "místico": [
        "🔮 O {nome} é tão místico que a astrologia pediu consultoria!",
        "🔮 O {nome} fala com os astros e os astros atendem!",
        "🔮 O {nome} é tão espiritual que a energia virou CPF!",
        "🔮 O {nome} prevê tanto que a sorte tem horário marcado!",
        "🔮 O {nome} é tão místico que o horóscopo virou autobiografia!"
    ],
    "exibido": [
        "📸 O {nome} é tão exibido que o espelho pediu exclusividade!",
        "📸 O {nome} posta tanto que o instagram pediu intervalo!",
        "📸 O {nome} é tão vaidoso que a selfie tem diretor!",
        "📸 O {nome} se mostra tanto que a modéstia virou alienígena!",
        "📸 O {nome} é tão exibido que o holofote tem contrato!"
    ],
    "crítico": [
        "📝 O {nome} é tão crítico que a crítica pediu revisão!",
        "📝 O {nome} aponta tanto erro que o acerto virou lenda!",
        "📝 O {nome} é tão analítico que a análise tem sub-análise!",
        "📝 O {nome} comenta tanto que o comentário precisa de comentário!",
        "📝 O {nome} é tão crítico que elogiar virou desafio!"
    ],
    "zé-ruela": [
        "😏 O {nome} é tão zé-ruela que a malandragem tem certificado!",
        "😏 O {nome} é tão esperto que a esperteza virou profissão!",
        "😏 O {nome} dá tanta volta que o caminho mais curto desistiu!",
        "😏 O {nome} é tão jeitoso que o jeitinho tem manual!",
        "😏 O {nome} é tão zé-ruela que o santo pediu proteção!"
    ],
    "emocionado": [
        "😭 O {nome} é tão emocionado que até o bot chorou com ele!",
        "😭 O {nome} se emociona tanto que a lágrima pediu lenço!",
        "😭 O {nome} é tão sensível que a música triste é muito alegre!",
        "😭 O {nome} chora com tudo, até com a conta de luz!",
        "😭 O {nome} é tão emocionado que a emoção tem nome!"
    ],
    "#@$%": [
        "🤬 O {nome} é tão #@$% que até a censura pediu calma!",
        "🤬 O {nome} fala tanta #@$% que o travessão virou amigo!",
        "🤬 O {nome} é tão #@$% que os palavrões têm que ser codificados!",
        "🤬 O {nome} solta tanto #@$% que o Twitter bloqueou!",
        "🤬 O {nome} é tão #@$% que o filtro familiar surtou!",
        "🤬 O {nome} solta tanto palavrão que o dicionário pediu auxílio!",
        "🤬 O {nome} xinga tão bem que a vovó pediu tradução!",
        "🤬 O {nome} é tão desbocado que o filtro de palavras pediu demissão!",
        "🤬 O {nome} fala tanta besteira que o bot ficou sem saber o que dizer!",
        "🤬 O {nome} é tão criativo com xingamentos que o roteirista pediu dicas!"
]
}

# ============================================
# SISTEMA DE MEMÓRIA
# ============================================

class MemorySystem:
    def __init__(self):
        self.data_file = "server_memory.json"
        self.memory = self.load_memory()
        self.last_joke_times = {}
        self.user_joke_history = defaultdict(list)
        self.joke_cooldown_seconds = 30  
        self.max_history_size = 10
        self.tempo_call_tracking = {}  # {user_id: tempo_inicial}

    
    def load_memory(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_memory(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def get_user_profile(self, user_id):
        user_id_str = str(user_id)
        if user_id_str not in self.memory:
            self.memory[user_id_str] = {
                "nome": "",
                "personalidade": [],
                "entrada": datetime.now().isoformat(),
                "ultima_msg": datetime.now().isoformat(),
                "piadas_contadas": 0,
                "eventos": [],
                "estatisticas": {
                    "total_mensagens": 0,
                    "total_caracteres": 0,
                    "total_emojis": 0,
                    "emojis_usados": {},
                    "tempo_call": 0,
                    "entradas_call": 0,
                    "ultima_entrada_call": None,
                    "total_palavras": 0
                }
            }
            self.save_memory()
        return self.memory[user_id_str]
    
    def update_personality(self, user_id, trait):
        profile = self.get_user_profile(user_id)
        if trait not in profile["personalidade"]:
            profile["personalidade"].append(trait)
            if len(profile["personalidade"]) > 10:
                profile["personalidade"].pop(0)
            self.save_memory()
    
    def get_time_in_server(self, user_id):
        profile = self.get_user_profile(user_id)
        entrada = datetime.fromisoformat(profile["entrada"])
        tempo = datetime.now() - entrada
        return tempo

    # ============================================
    # SISTEMA DE PIADAS
    # ============================================
    
    def can_send_joke(self, user_id):
        user_id_str = str(user_id)
        now = datetime.now()
        last_time = self.last_joke_times.get(user_id_str)
        
        if last_time is not None:
            if now - last_time < timedelta(seconds=self.joke_cooldown_seconds):
                return False, None
        
        used_jokes = set(self.user_joke_history.get(user_id_str, []))
        self.last_joke_times[user_id_str] = now
        return True, used_jokes

    def mark_joke_as_used(self, user_id, joke_text):
        user_id_str = str(user_id)
        self.user_joke_history[user_id_str].append(joke_text)

        if len(self.user_joke_history[user_id_str]) > 10:  
            self.user_joke_history[user_id_str] = self.user_joke_history[user_id_str][-10:] 

    def generate_inside_joke(self, user_id):
        profile = self.get_user_profile(user_id) 
        personality = profile["personalidade"]
        
        if not personality:
            self.update_personality(user_id, "engraçado")
            personality = ["engraçado"] 
        
        candidates = [] 
        for trait in personality:
            if trait in PERSONALITY_JOKES: 
                candidates.extend(PERSONALITY_JOKES[trait]) 

        can_send, used_jokes = self.can_send_joke(user_id)
        if not can_send:
            return "COOLDOWN" 

        available = [j for j in candidates if j not in used_jokes]

        if not available:
            self.user_joke_history[str(user_id)] = [] 
            available = candidates 
        joke_template = random.choice(available)

        joke = joke_template.format(nome=profile["nome"] or "usuário")

        self.mark_joke_as_used(user_id, joke_template)
        
        return joke

    # ============================================
    # ESTATÍSTICAS DE MENSAGEM
    # ============================================
    
    def update_message_stats(self, user_id, text):
      
        profile = self.get_user_profile(user_id)
        stats = profile["estatisticas"]
        
        stats["total_mensagens"] += 1
        stats["total_caracteres"] += len(text)
        stats["total_palavras"] += len(text.split())
        
        emojis = self.count_emojis(text)
        stats["total_emojis"] += len(emojis)
        
        for emoji in emojis:
            if emoji in stats["emojis_usados"]:
                stats["emojis_usados"][emoji] += 1
            else:
                stats["emojis_usados"][emoji] = 1
        
        self.save_memory()

    def count_emojis(self, text):
       
        import re
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Símbolos e pictogramas
            "\U0001F680-\U0001F6FF"  # Transporte e símbolos
            "\U0001F700-\U0001F77F"  # Símbolos alquímicos
            "\U0001F780-\U0001F7FF"  # Símbolos geométricos
            "\U0001F800-\U0001F8FF"  # Setas suplementares
            "\U0001F900-\U0001F9FF"  # Símbolos suplementares
            "\U0001FA00-\U0001FA6F"  # Xadrez e símbolos
            "\U0001FA70-\U0001FAFF"  # Símbolos diversos
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Símbolos diversos
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.findall(text)

    # ============================================
    # ESTATÍSTICAS DE CALL
    # ============================================
    
    def start_call_tracking(self, user_id):
        
        user_id_str = str(user_id)
        self.tempo_call_tracking[user_id_str] = datetime.now()
        
        profile = self.get_user_profile(user_id)
        stats = profile["estatisticas"]
        stats["entradas_call"] += 1
        stats["ultima_entrada_call"] = datetime.now().isoformat()
        self.save_memory()
        print(f"📞 {profile['nome']} entrou na call! Rastreando tempo...")
    
    def stop_call_tracking(self, user_id):
       
        user_id_str = str(user_id)
        if user_id_str in self.tempo_call_tracking:
            inicio = self.tempo_call_tracking[user_id_str]
            tempo_segundos = (datetime.now() - inicio).total_seconds()
            
            profile = self.get_user_profile(user_id)
            stats = profile["estatisticas"]
            stats["tempo_call"] += int(tempo_segundos)
            
            minutos = int(tempo_segundos // 60)
            segundos = int(tempo_segundos % 60)
            self.add_event(user_id, f"Ficou em call por {minutos}m{segundos}s")
            
            del self.tempo_call_tracking[user_id_str]
            self.save_memory()
            
            print(f"📞 {profile['nome']} saiu da call! Tempo: {minutos}m{segundos}s")
            return int(tempo_segundos)
        return 0
    
    def get_user_stats(self, user_id):
     
        profile = self.get_user_profile(user_id)
        return profile.get("estatisticas", {})

    # ============================================
    # SISTEMA DE EVENTOS
    # ============================================
    
    def add_event(self, user_id, descricao):
      
        profile = self.get_user_profile(user_id)
        profile["eventos"].append({
            "descricao": descricao,
            "data": datetime.now().isoformat()
        })
        if len(profile["eventos"]) > 20:
            profile["eventos"] = profile["eventos"][-20:]
        self.save_memory()


# ============================================
# INICIALIZA O SISTEMA DE MEMÓRIA
# ============================================

memory = MemorySystem()  


# ============================================
# COMANDOS PARA ESTATÍSTICAS
# ============================================

@bot.command(name="status")
async def stats_command(ctx, member: discord.Member = None):
  
    if member is None:
        member = ctx.author
    
    stats = memory.get_user_stats(member.id)  
    
    if not stats or stats.get("total_mensagens", 0) == 0:
        await ctx.send(f"📊 {member.display_name} ainda não tem estatísticas!")
        return

    tempo_call = stats.get("tempo_call", 0)
    horas = tempo_call // 3600
    minutos = (tempo_call % 3600) // 60

    top_emojis = sorted(stats.get("emojis_usados", {}).items(), key=lambda x: x[1], reverse=True)[:5]
    top_emojis_text = ", ".join([f"{emoji} ({qtd})" for emoji, qtd in top_emojis]) if top_emojis else "Nenhum"
    
    embed = discord.Embed(
        title=f"📊 Estatísticas de {member.display_name}",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="💬 Mensagens",
        value=f"Total: {stats.get('total_mensagens', 0)}",
        inline=True
    )
    
    embed.add_field(
        name="📝 Caracteres",
        value=f"Total: {stats.get('total_caracteres', 0)}",
        inline=True
    )
    
    embed.add_field(
        name="📖 Palavras",
        value=f"Total: {stats.get('total_palavras', 0)}",
        inline=True
    )
    
    embed.add_field(
        name="😀 Emojis",
        value=f"Total: {stats.get('total_emojis', 0)}",
        inline=True
    )
    
    embed.add_field(
        name="📞 Tempo em Call",
        value=f"{horas}h {minutos}min",
        inline=True
    )
    
    embed.add_field(
        name="🚪 Entradas em Call",
        value=f"{stats.get('entradas_call', 0)} vezes",
        inline=True
    )
    
    embed.add_field(
        name="🔥 Top 5 Emojis",
        value=top_emojis_text,
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name="top_emojis")
async def top_emojis_command(ctx):
   
    emoji_count = {}
    
    for user_id, profile in memory.memory.items():
        stats = profile.get("estatisticas", {})
        emojis = stats.get("emojis_usados", {})
        for emoji, qtd in emojis.items():
            emoji_count[emoji] = emoji_count.get(emoji, 0) + qtd
    
    top = sorted(emoji_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    if not top:
        await ctx.send("📊 Nenhum emoji registrado ainda!")
        return
    
    texto = "🔥 **Top 10 Emojis do Servidor:**\n"
    for i, (emoji, qtd) in enumerate(top, 1):
        texto += f"{i}. {emoji} - {qtd} vezes\n"
    
    await ctx.send(texto)


@bot.command(name="top_mensagens")
async def top_mensagens_command(ctx):
 
    usuarios = []
    
    for user_id, profile in memory.memory.items():
        stats = profile.get("estatisticas", {})
        mensagens = stats.get("total_mensagens", 0)
        if mensagens > 0:
            usuarios.append((profile["nome"], mensagens))
    
    top = sorted(usuarios, key=lambda x: x[1], reverse=True)[:10]
    
    if not top:
        await ctx.send("📊 Nenhuma mensagem registrada ainda!")
        return
    
    texto = "📊 **Top 10 Mais Mensagens:**\n"
    for i, (nome, qtd) in enumerate(top, 1):
        texto += f"{i}. {nome} - {qtd} mensagens\n"
    
    await ctx.send(texto)


# ============================================
# EVENTOS DE VOZ (CALL) - CORRIGIDO
# ============================================

@bot.event
async def on_voice_state_update(member, before, after):
    """Apenas rastreia tempo de call - NUNCA desconecta o bot"""
    
    # Usuário ENTROU na call
    if before.channel is None and after.channel is not None:
        # Só rastreia se não for o próprio bot
        if member != bot.user:
            memory.start_call_tracking(member.id)
            await after.channel.send(f"🎤 {member.display_name} entrou na call!")
    
    # Usuário SAIU da call
    elif before.channel is not None and after.channel is None:
        if member != bot.user:
            tempo = memory.stop_call_tracking(member.id)
            if tempo:
                minutos = int(tempo // 60)
                segundos = int(tempo % 60)
                await before.channel.send(f"👋 {member.display_name} saiu da call! Ficou {minutos}m{segundos}s")
# ============================================
# FUNÇÕES AUXILIARES 
# ============================================

def detect_personality(text, user_id):
   
    text_lower = text.lower()
    
    profile = memory.get_user_profile(user_id)
    current_personalities = profile.get("personalidade", [])
    
    scores = {trait: 1 for trait in current_personalities}
    
    for trait, keywords in PERSONALITY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text_lower:
                score += 2 if " " in keyword else 1
        if score > 0:
            scores[trait] = scores.get(trait, 0) + score
    
    top_traits = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:5]
    new_personalities = [trait for trait, _ in top_traits]
    
    if set(new_personalities) != set(current_personalities):
        profile["personalidade"] = new_personalities
        memory.save_memory()


async def check_important_events(message):

    user_id = message.author.id
    profile = memory.get_user_profile(user_id)
    stats = profile.get("estatisticas", {})
    
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
    
    if stats.get("total_mensagens", 0) == 100:
        await message.channel.send(f"🎉 {message.author.display_name} atingiu 100 mensagens!")
        memory.add_event(user_id, "100 mensagens!")

    if stats.get("total_caracteres", 0) >= 1000:
        # Verifica se já não foi registrado antes
        eventos = [e["descricao"] for e in profile.get("eventos", [])]
        if "1000 caracteres!" not in str(eventos):
            await message.channel.send(f"📝 {message.author.display_name} já escreveu 1000 caracteres!")
            memory.add_event(user_id, "1000 caracteres!")

# ============================================
# EVENTO DE MENSAGEM 
# ============================================

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    if len(message.content.strip()) < 3:
        await bot.process_commands(message)
        return
    
    user_id = message.author.id
    profile = memory.get_user_profile(user_id)
    profile["nome"] = message.author.display_name
    profile["ultima_msg"] = datetime.now().isoformat()
    
    memory.update_message_stats(user_id, message.content)
    
    memory.save_memory()

    detect_personality(message.content, user_id)

    await check_important_events(message)
    
    trait_count = len(profile["personalidade"])
    joke_chance = 0.06 + min(0.08, 0.01 * trait_count)

    if random.random() < joke_chance:
        can_send, _ = memory.can_send_joke(user_id)
        if can_send:
            joke = memory.generate_inside_joke(user_id)
            if joke and joke != "COOLDOWN":
                await message.channel.send(joke)
                profile = memory.get_user_profile(user_id)
                profile["piadas_contadas"] += 1
                memory.save_memory()

    await bot.process_commands(message)

# ============================================
# COMANDOS
# ============================================

@bot.command(name="perfil")
async def perfil(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    profile = memory.get_user_profile(member.id)
    stats = profile.get("estatisticas", {})

    ultima_msg = datetime.fromisoformat(profile["ultima_msg"]).strftime("%d/%m/%Y %H:%M")

    ultima_call = stats.get("ultima_entrada_call")
    if ultima_call:
        ultima_call_formatada = datetime.fromisoformat(ultima_call).strftime("%d/%m/%Y %H:%M")
    else:
        ultima_call_formatada = "Nunca entrou em call"

    embed = discord.Embed(
        title=f"📊 Perfil de {member.display_name}",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="🧠 Personalidade",
        value=", ".join(profile["personalidade"]) or "Ainda descobrindo...",
        inline=False
    )

    embed.add_field(
        name="💬 Última mensagem",
        value=ultima_msg,
        inline=True
    )
    embed.add_field(
        name="📞 Última vez em call",
        value=ultima_call_formatada,
        inline=True
    )

    await ctx.send(embed=embed)

@bot.command(name="join>//<")
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ Você precisa estar em um canal de voz!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        if ctx.voice_client.channel == channel:
            await ctx.send(f"🔊 Já estou no canal {channel.name}!")
            return
        await ctx.voice_client.move_to(channel)
        await ctx.send(f"🔊 Movido para {channel.name}!")
        return
    
    try:
        # 🔥 ADICIONA RECONNECT E UM TIMEOUT MAIOR
        await channel.connect(timeout=60.0, reconnect=True)
        await ctx.send(f"🔊 Conectado ao canal {channel.name}!")
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para entrar neste canal de voz!")
    except discord.ClientException:
        await ctx.send("❌ Já estou conectado em outro canal de voz!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao conectar: {e}")

@bot.command(name="leave>//<")
async def leave(ctx):
    if not ctx.voice_client:
        await ctx.send("❌ Não estou em nenhum canal de voz!")
        return
    
    await ctx.voice_client.disconnect()
    await ctx.send("🔇 Desconectado do canal de voz!")

# ============================================
# WEB SERVER PARA KEEP ALIVE (DISCLOUD)
# ============================================

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está online e funcionando!"

@app.route('/health')
def health():
    return "OK", 200

def run_web():
    try:
        app.run(host='0.0.0.0', port=8080, debug=False)
    except Exception as e:
        print(f"⚠️ Web server error: {e}")

# Inicia o web server em uma thread separada
threading.Thread(target=run_web, daemon=True).start()
print("🌐 Web server iniciado na porta 8080")

# ============================================
# INICIA O BOT
# ============================================

DISCORD_TOKEN = "MTUzMTg3NDA5NzM4NDkxNTAzNQ.Gi1sYN.eEzA-ecpPlp4tHnkwPI4vpQHnjuxkvAb20UqsM"
if DISCORD_TOKEN:
    print(f"✅ Token encontrado! Iniciando bot...")
    bot.run(DISCORD_TOKEN)
else:
    print("❌ ERRO: Token não encontrado!")
    print("Verifique se DISCORD_TOKEN está no discloud.config")
