# Projet : Thèa Maro
# Version : PoC_0.1


# Modul import
from dotenv import load_dotenv
import os
import discord


# Token loading
load_dotenv()
token = os.getenv("TOKEN")


bot = discord.Bot()

# we need to limit the guilds for testing purposes
# so other users wouldn't see the command that we're testing



bot.run(token)
