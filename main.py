import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# ========= CONFIGURATION =========

WELCOME_CHANNEL_ID = 1235618505059995835
LOG_CHANNEL_ID = 1527415268983312676

HOUSES = {
    "Grifforia": {
        "role_id": 1526983959009825031,
        "color": discord.Color.red(),
        "emoji": "🦁",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/assets/grifforia.png"
    },

    "Serdaelis": {
        "role_id": 1526984147531333852,
        "color": discord.Color.blue(),
        "emoji": "🦅",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/assets/serdaelis.png"
    },

    "Poursouf": {
        "role_id": 1526984357758238901,
        "color": discord.Color.gold(),
        "emoji": "🦡",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/assets/poursouf.png"
    },

    "Serpentis": {
        "role_id": 1526984414800646336,
        "color": discord.Color.green(),
        "emoji": "🐍",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/assets/serpentis.png"
    }
}

PHRASES = [
    "Hmmm...",
    "Je vois beaucoup de courage...",
    "Je sens une grande ambition...",
    "Tu caches un immense potentiel...",
    "Une décision difficile...",
    "Ton avenir sera grand...",
    "Je lis dans ton esprit...",
    "Ton destin est presque écrit...",
    "Une âme fidèle...",
    "Tu es plein de ressources...",
    "Quel choix difficile...",
    "Le Choixpeau hésite..."
]

# ========= BOT =========

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ========= CHOIX DE LA MAISON =========

def choisir_maison(guild):

    nombres = {}

    for maison, data in HOUSES.items():

        role = guild.get_role(data["role_id"])

        if role is None:
            print(f"[ERREUR] Rôle introuvable : {maison}")
            continue

        nombres[maison] = len(role.members)

    if len(nombres) == 0:
        return random.choice(list(HOUSES.keys()))

    minimum = min(nombres.values())

    candidates = []

    for maison, total in nombres.items():

        if total <= minimum + 1:
            candidates.append(maison)

    return random.choice(candidates)

@bot.event
async def on_ready():

    print("="*40)
    print(f"{bot.user} est connecté !")
    print("="*40)
    @bot.event
async def on_member_join(member):

    salon = bot.get_channel(WELCOME_CHANNEL_ID)
    logs = bot.get_channel(LOG_CHANNEL_ID)

    if salon is None:
        print("[ERREUR] Salon de bienvenue introuvable.")
        return

    message = await salon.send(
        f"🎉 **Bienvenue {member.mention} !**\n\n"
        "🎩 **Le Choixpeau Magique arrive...**"
    )

    animation = [
        "🎩 **Le Choixpeau t'observe...**",
        "👀 Il analyse ton esprit...",
        f"💭 *{random.choice(PHRASES)}*",
        "📖 Il fouille dans tes souvenirs...",
        "⚖️ Une décision difficile...",
        "🟩⬜⬜⬜⬜ 20%",
        "🟩🟩🟩⬜⬜ 60%",
        "🟩🟩🟩🟩🟩 100%",
        "✨ **LE CHOIX EST FAIT !**"
    ]

    for texte in animation:
        await asyncio.sleep(2)
        await message.edit(content=texte)

    maison = choisir_maison(member.guild)

    role = member.guild.get_role(HOUSES[maison]["role_id"])

    if role is None:
        await salon.send(
            f"❌ Impossible de trouver le rôle **{maison}**.\n"
            "Vérifie l'ID du rôle dans le code."
        )
        return

    try:
        await member.add_roles(role)
    except discord.Forbidden:
        await salon.send(
            "❌ Je n'ai pas la permission d'attribuer les rôles.\n"
            "Place mon rôle au-dessus des maisons."
        )
        return

    embed = discord.Embed(
        title="🏰 Le Choixpeau Magique a parlé !",
        description=(
            f"Bienvenue {member.mention}\n\n"
            f"Tu rejoins la maison\n\n"
            f"# {HOUSES[maison]['emoji']} **{maison}**"
        ),
        color=HOUSES[maison]["color"]
    )

    file = discord.File(
    f"assets/{maison.lower()}.png",
    filename=f"{maison.lower()}.png"
)

embed.set_image(
    url=f"attachment://{maison.lower()}.png"
)

await salon.send(file=file, embed=embed)

    embed.set_footer(
        text="✨ Quatre maisons • Une destinée"
    )

    await salon.send(embed=embed)

    if logs is not None:

        log = discord.Embed(
            title="📜 Nouvelle répartition",
            color=discord.Color.dark_gold()
        )

        log.add_field(
            name="👤 Joueur",
            value=member.mention,
            inline=False
        )

        log.add_field(
            name="🏰 Maison",
            value=maison,
            inline=False
        )

        log.add_field(
            name="🎭 Rôle",
            value=role.mention,
            inline=False
        )

        log.set_thumbnail(url=member.display_avatar.url)

        await logs.send(embed=log)
        # ========= LANCEMENT DU BOT =========

if __name__ == "__main__":
    if TOKEN is None:
        print("=" * 50)
        print("ERREUR : DISCORD_TOKEN est introuvable !")
        print("Vérifie ton fichier .env ou la variable Railway.")
        print("=" * 50)
    else:
        bot.run(TOKEN)
