import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# CONFIGURATION
WELCOME_CHANNEL_ID = 1527353878646095882
LOG_CHANNEL_ID = 1527353942021902496

HOUSES = {
    "Grifforia": {
        "role_id": 1527352433314107482,
        "color": discord.Color.red(),
        "emoji": "🦁"
    },
    "Serdaelis": {
        "role_id": 1465348744441757981,
        "color": discord.Color.blue(),
        "emoji": "🦅"
    },
    "Poursouf": {
        "role_id": 1527352587500650637,
        "color": discord.Color.gold(),
        "emoji": "🦡"
    },
    "Serpentis": {
        "role_id": 1527352623454486708,
        "color": discord.Color.green(),
        "emoji": "🐍"
    }
}

PHRASES = [
    "Hmmm...",
    "Je vois beaucoup de potentiel...",
    "Une âme intéressante...",
    "Je sens du courage...",
    "Je vois de l'ambition...",
    "Une décision difficile...",
    "Quel choix compliqué...",
    "Tu pourrais accomplir de grandes choses...",
    "Je perçois une force intérieure...",
    "Ton avenir est prometteur..."
]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def choose_house(guild):
    houses_count = {}

    for house_name, house_data in HOUSES.items():
        role = guild.get_role(house_data["role_id"])
        houses_count[house_name] = len(role.members) if role else 0

    min_count = min(houses_count.values())

    candidates = [
        house
        for house, count in houses_count.items()
        if count <= min_count + 1
    ]

    return random.choice(candidates)


@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")


@bot.event
async def on_member_join(member):

    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if not welcome_channel:
        return

    await welcome_channel.send(
        f"🎉 Bienvenue {member.mention} !\n\n🎩 Le Choixpeau Magique arrive..."
    )

    msg = await welcome_channel.send("🎩 Le Choixpeau t'observe...")

    for _ in range(4):
        await asyncio.sleep(2)
        await msg.edit(content=f'🎩 "{random.choice(PHRASES)}"')

    await asyncio.sleep(2)
    await msg.edit(content="🎩 **LE CHOIX EST FAIT !**")

    house = choose_house(member.guild)

    role = member.guild.get_role(HOUSES[house]["role_id"])

    if role:
        await member.add_roles(role)

    embed = discord.Embed(
        title=f"{HOUSES[house]['emoji']} {house}",
        description=(
            "Le Choixpeau Magique a parlé !\n\n"
            f"Bienvenue dans la maison **{house}** !"
        ),
        color=HOUSES[house]["color"]
    )

    embed.set_footer(text="Répartition officielle")

    await welcome_channel.send(embed=embed)

    if log_channel:
        log_embed = discord.Embed(
            title="📜 Nouvelle répartition",
            color=discord.Color.dark_gold()
        )

        log_embed.add_field(
            name="Joueur",
            value=member.mention,
            inline=False
        )

        log_embed.add_field(
            name="Maison",
            value=house,
            inline=False
        )

        await log_channel.send(embed=log_embed)


bot.run(TOKEN)
