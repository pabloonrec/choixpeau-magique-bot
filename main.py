import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# ===== CONFIGURATION =====

WELCOME_CHANNEL_ID = 1527353878646095882
LOG_CHANNEL_ID = 1527353942021902496

HOUSES = {
    "Grifforia": {
        "role_id": 1527352433314107482,
        "color": discord.Color.red(),
        "emoji": "🦁",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/assets/grifforia.png"
    },
    "Serdaelis": {
        "role_id": 1465348744441757981,
        "color": discord.Color.blue(),
        "emoji": "🦅",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/serdaelis.png"
    },
    "Poursouf": {
        "role_id": 1527352587500650637,
        "color": discord.Color.gold(),
        "emoji": "🦡",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/poursouf.png"
    },
    "Serpentis": {
        "role_id": 1527352623454486708,
        "color": discord.Color.green(),
        "emoji": "🐍",
        "image": "https://raw.githubusercontent.com/pabloonrec/choixpeau-magique-bot/main/serpentis.png"
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
    "Ton destin est presque écrit..."
]

# ===== BOT =====

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def choisir_maison(guild):

    nombres = {}

    for maison, data in HOUSES.items():
        role = guild.get_role(data["role_id"])
        nombres[maison] = len(role.members)

    minimum = min(nombres.values())

    candidates = [
        maison
        for maison, total in nombres.items()
        if total <= minimum + 1
    ]

    return random.choice(candidates)


@bot.event
async def on_ready():
    print("=" * 40)
    print(f"{bot.user} est connecté !")
    print("=" * 40)


@bot.event
async def on_member_join(member):

    salon = bot.get_channel(WELCOME_CHANNEL_ID)
    logs = bot.get_channel(LOG_CHANNEL_ID)

    if salon is None:
        return

    message = await salon.send(
        f"🎉 Bienvenue {member.mention}\n\n🎩 Le Choixpeau Magique arrive..."
    )

    animation = [
        "🎩 Le Choixpeau t'observe...",
        "👀 Il lit dans ton regard...",
        "📖 Il fouille dans ton esprit...",
        f'💭 "{random.choice(PHRASES)}"',
        "⏳ Une décision difficile...",
        "████░░░░░░ 40 %",
        "███████░░░ 70 %",
        "██████████ 100 %",
        "✨ LE CHOIX EST FAIT !"
    ]

    for texte in animation:
        await asyncio.sleep(2)
        await message.edit(content=texte)

    maison = choisir_maison(member.guild)

    role = member.guild.get_role(HOUSES[maison]["role_id"])

    if role:
        await member.add_roles(role)

    embed = discord.Embed(
        title="🏰 Le Choixpeau Magique a parlé !",
        description=(
            f"Félicitations {member.mention}\n\n"
            f"Bienvenue dans la maison\n\n"
            f"# {HOUSES[maison]['emoji']} {maison}"
        ),
        color=HOUSES[maison]["color"]
    )

    embed.set_image(url=HOUSES[maison]["image"])

    embed.set_footer(text="✨ Quatre maisons • Une destinée")

    await salon.send(embed=embed)

    if logs:

        log = discord.Embed(
            title="📜 Nouvelle répartition",
            color=discord.Color.dark_gold()
        )

        log.add_field(
            name="Joueur",
            value=member.mention,
            inline=False
        )

        log.add_field(
            name="Maison",
            value=maison,
            inline=False
        )

        await logs.send(embed=log)


bot.run(TOKEN)
