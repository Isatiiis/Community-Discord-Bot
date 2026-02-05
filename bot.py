import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

FAQ_FILE = "faq.json"

def load_faq():
    if not os.path.exists(FAQ_FILE):
        return {}
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_faq(data):
    with open(FAQ_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_guild_faq(guild_id):
    faq = load_faq()
    return faq.get(str(guild_id), {})

def set_guild_faq(guild_id, guild_faq):
    faq = load_faq()
    faq[str(guild_id)] = guild_faq
    save_faq(faq)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot or message.guild is None:
        return

    guild_id = message.guild.id
    guild_faq = get_guild_faq(guild_id)

    content = message.content.lower()

    for keyword, response in guild_faq.items():
        if keyword in content:
            await message.channel.send(response)
            break

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def addfaq(ctx, keyword: str, *, response: str):
    guild_id = ctx.guild.id
    guild_faq = get_guild_faq(guild_id)

    guild_faq[keyword.lower()] = response
    set_guild_faq(guild_id, guild_faq)

    await ctx.send(f"✅ FAQ ajoutée pour ce serveur : **{keyword}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def removefaq(ctx, keyword: str):
    guild_id = ctx.guild.id
    guild_faq = get_guild_faq(guild_id)

    if keyword.lower() in guild_faq:
        del guild_faq[keyword.lower()]
        set_guild_faq(guild_id, guild_faq)
        await ctx.send(f"🗑️ FAQ supprimée : **{keyword}**")
    else:
        await ctx.send("❌ Ce mot-clé n’existe pas sur ce serveur.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

import os
bot.run(os.getenv("DISCORD_TOKEN"))


