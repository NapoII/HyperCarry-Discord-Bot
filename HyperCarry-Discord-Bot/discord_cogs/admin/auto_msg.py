"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes


------------------------------------------------
"""
# 
from discord.ext import commands, tasks
from util.__funktion__ import *
import random
import discord
from discord import app_commands
from discord import app_commands, ui
from discord import Color
import asyncio
from datetime import datetime

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)

token_config_dir = os.path.normpath(os.path.join(bot_folder, "cfg", "token.ini"))

# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")

steam_token = read_config(token_config_dir, "steam", "steam_token")
json_path_server_channel_data = os.path.join(current_dir, "server_channel_data.json")

bot_cmd_channel = read_config(config_dir, "channel", "bot_cmd_channel_id")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1


class auto_bot_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir

    @commands.Cog.listener()
    async def on_message(self, message):

        # Check if the message is from a bot to avoid potential loops
        if message.author.bot:
            return
        
        try:
            if "-ticket" in message.channel.name:
                return
        except:
            pass
        
        words_in_message = message.content.lower().split()

        trigger_words = [
    "ban",
    "cheater",
    "esp",
    "hack",
    "cheat",
    "report",
    "sppeal",
    "bug",
    "ticket",
    "hilfe",
    "support",
    "probleme",
    "fehler",
    "benoetigt",
    "assistance",
    "help",
    "trouble",
    "issue",
    "error",
    "require",
    "notwendig"
]
        
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend: help_embed msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend: help_embed msg:\n {message.content}\n")

            if not hasattr(self.bot, 'last_triggered') or time.time() - self.bot.last_triggered > 600:
                open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
                embed = discord.Embed(
                            description=f"Hello <@!{message.author.id}>,\nif you need personalized assistance,\nplease <#{open_a_ticket_channel_id}>.\nOur support team will assist you promptly.",
                        colour=0x81cffe)
                embed.set_thumbnail(url="https://i.imgur.com/NhaGVxy.png")
                await message.channel.send(embed=embed)

                self.bot.last_triggered = time.time()  # Update last_triggered time
            else:
                pass


        trigger_words = [
    "server",
    "ip",
    "conect"]
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend:ip_embed msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend: ip_embed msg:\n {message.content}\n")
     
            
            if not hasattr(self.bot, 'last_triggered') or time.time() - self.bot.last_triggered > 600:
                all_game_servers_channel_id = read_config(config_dir,"channel", "all_game_servers_channel_id", "int")

                embed = discord.Embed(description=f"Hello <@!{message.author.id}>,\nYou can find all our servers with their IPs and connect commands here:\n<#{all_game_servers_channel_id}>",
                                    colour=0x81cffe)

                embed.set_thumbnail(url="https://i.imgur.com/85Ntdof.png")
                await message.channel.send(embed=embed)

                self.bot.last_triggered = time.time()  # Update last_triggered time
            else:
                pass


        trigger_words = [
    "role",
    "roles"]
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend: role_embed msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend: role_embed msg:\n {message.content}\n")

            if not hasattr(self.bot, 'last_triggered') or time.time() - self.bot.last_triggered > 600:
                roles_n_rules_channel_id = read_config(config_dir,"channel", "roles_n_rules_channel_id", "int")

                embed = discord.Embed(description=f"Hello <@!{message.author.id}>,\nYou can pick up the roles for the games yourself in the channel:\n<#{roles_n_rules_channel_id}>",
                                    colour=0x81cffe)

                embed.set_thumbnail(url="https://i.imgur.com/x9dHTAY.png")
                await message.channel.send(embed=embed)

                self.bot.last_triggered = time.time()  # Update last_triggered time
            else:
                pass


        trigger_words = [
    "ark",
    "dinosaurier",
    "zähmen",
    "dino",
    "raubtiere",
    "dinozähmung",
    "rex",
    "raptor",
    "trike",
    "stegosaurus",
    "spinosaurus",
    "pteranodon",
    "tyrannosaurus",
    "brachiosaurus"]
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend:🦕 msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend:🦕 msg:\n {message.content}\n")

            await message.add_reaction("🦕")


        trigger_words = [
    "abstimmung",
    "voting",
    "stimme",
    "wählen",
    "umfrage",
    "entscheidung",
    "wahl",
    "wahlzettel",
    "kandidaten",
    "mehrheit",
    "demokratie",
    "teilnahme",
    "entscheiden",
    "optionen",
    "sondierung",
    "vote",
    "poll",
    "ballot",
    "election",
    "choice",
    "decision",
    "candidate",
    "majority",
    "democracy",
    "participation",
    "decide",
    "options",
    "survey",
    "elect",
    "cast your vote",
    "polling",
    "balloting"
]
        
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend:✅❌ msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend:✅❌ msg:\n {message.content}\n")

            await message.add_reaction("✅")
            await message.add_reaction("❌")


        trigger_words = [
    "csgo",
    "m4",
    "bombe",
    "terrorist",
    "counter-terrorist",
    "sprengstoff",
    "defuse",
    "befehl",
    "einsatz",
    "feind",
    "ziel",
    "rückzug",
    "messer",
    "headshot",
    "pubg",
    "borderlands",
    "battlefield",
    "cod",
]
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend:🔫 msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend:🔫 msg:\n {message.content}\n")

            await message.add_reaction("🔫")


        trigger_words = [
    "litty",
    "fresh",
    "swag",
    "lit",
    "chill",
    "fope",
    "nice",
    "sick",
    "Wavy",
    "gnarly",
    "fancy",
    "rad",
    "fly",
    "awesome",
    "geil",
    "krass",
    "cool",
    "gönnt",
    "lol"
]
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nemoti: 😎 msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nemoti: 😎 msg:\n {message.content}\n")

            await message.add_reaction("😎")


        trigger_words = [
    "scheiße",
    "mist",
    "uncool",
    "fuck",
    "fick dich",
    "huso",
    "huhrensohn",
    "misgeburt",
    "hund"
]
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend:💩 msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend:💩 msg:\n {message.content}\n")

            
            await message.add_reaction("💩")


        trigger_words = [
    "hi",
    "hello",
    "moin",
    "hallo",
    "gude",
    ]
        if any(word.lower() in words_in_message for word in trigger_words):
            if isinstance(message.channel, discord.TextChannel):
                print(f"auto_msg --> user: {message.author.name} channel: {message.channel.name}\nsend:👋 msg:\n {message.content}\n")
            else:
                print(f"auto_msg --> user: {message.author.name} channel: DM\nsend:👋 msg:\n {message.content}\n")

            await message.add_reaction("👋")


async def setup(bot: commands.Bot): 
    await bot.add_cog(auto_bot_msg(bot), guild=discord.Object(guild_id))