# Projet : Thèa Maro
# Version : PoC_0.1
# Date : 2024-12-14
# Description : Bot Discord pour la prise de commande
#

# Modul import
from dotenv import load_dotenv
import os
import discord
import json
import time

# Token loading
load_dotenv()
token = os.getenv("TOKEN")

# Load a channel ID
with open("asset/json/Channel_id.json", "r") as f:
    data = json.load(f)

bot = discord.Bot()

# we need to limit the guilds for testing purposes
# so other users wouldn't see the command that we're testing


# Bot is ready
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot}")
    await create_embed_commande()


# Function to create a new embed and button
async def create_embed_commande():
    channel_commande = bot.get_channel(data["Channel"]["Creat_ticket_channel"])
    print("\nSuppresion des messages du serveur {}.\n".format(channel_commande.name))
    try:
        async for message in channel_commande.history(limit=2):
            await message.delete()
            try:
                time.sleep(1)
            except:
                pass
        Commande = discord.Embed(
            title="Prendre commande",
            description="Pour passer votre commande il vous sufira d'appuiler sur le bouton si dessous.",
            color=0x00FF00,
        )

        # envoyer l'embed
        await channel_commande.send(embed=Commande, view=TIKET())
    except discord.Forbidden:
        print(
            f"le bot n'as pas les permitions de supprimers dans le channel {channel_commande.name()}."
        )


class TIKET(discord.ui.View):
    @discord.ui.button(
        label="Passer commande", style=discord.ButtonStyle.blurple
    )  # or .primary
    async def Button_Tiket(self, interaction, button):
        # récupération de l'utilisateur qui a appuyer sur le bouton
        user = interaction.user
        """role_acheteur = data["role_acheteur"]
        # on vérifie si l'utilisateur a le rôle acheteur
        # est qu'il n'a pas déjà un salon ticket de cette utilisateur
        if discord.utils.get(user.roles, id=role_acheteur) == None:
            # on crée un salon de ticket dans la catégorie ticket
            await interaction.response.send_message(
                "Vous n'avez pas le rôle Astronaute !", ephemeral=True
            )
            return"""
        # on vérifie si l'utilisateur n'a pas déjà un salon ticket de cette utilisateur
        nom = "commande-de-" + str(user.name)
        if (
            (
                str(discord.utils.get(user.guild.channels, name=nom.lower()))
                == nom.lower()
            )
        ) == False:
            await interaction.response.send_message(
                "Creation du salon !", ephemeral=True
            )
            await Tiket(user)
            return
        else:
            await interaction.response.send_message(
                "Vous avez déjà un salon de commande !", ephemeral=True
            )
            return


# on crée la fonction Tiket qui crée un salon de commande
@bot.event
async def Tiket(user):
    category_id = bot.get_channel(data["category_commande"])
    # on crée un salon de ticket dans la catégorie ticket
    await category_id.create_text_channel(
        name=f"commande-de-" + str(user.name),
        topic=f"Ticket de commande de {user.name}",
    )
    name = f"commande-de-" + str(user.name)
    channel = discord.utils.get(user.guild.channels, name=name.lower())
    channel_id = channel.id
    channel_commande = bot.get_channel(channel_id)
    # on ajoute les permissions au salon pour que seul l'utilisateur et les modérateurs puissent y accéder
    await channel_commande.set_permissions(
        user, read_messages=True, send_messages=True, read_message_history=True
    )
    """# on enregistre la creation du salon dans le fichier log
    messsage = "[{}] : le salon {} a été crée par {}.\n".format(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        channel_commande.name,
        user.name,
    )
    # avec l'encoding utf-8
    with open("asset/log/salon_commande.log", "a", encoding="utf-8") as f:
        f.write(messsage)
    """
    # on envoie un message
    embed = discord.Embed(
        title="Commander",
        description="Pour commander il vous suffira de selectionnée la catégorie voulue",
        color=0x00FF00,
    )
    embed.add_field(
        name="Fonctionnement",
        value='Pour commander il vous suffit de faire 2 commande\nla premier !commande "user"\nla deuxième !ajout_commande "id_produit" "nombre_de_produit"\n vous pouvez ajouter autant de produit que vous voulez\n\nPour voir la commande il faut faire : \n !affiche_command \n si vous voulais l\'enregistrée il suffit de faire : \n!enregistre_commande',
        inline=False,
    )
    embed.add_field(
        name="attention",
        value="si vous n'avais pas enregistrée votre commande elle ne sera pas prise en compte",
        inline=False,
    )

    await channel_commande.send(
        "Bonjour {} bienvenue dans votre salon de commande ! Un de nos <@&{}> vas s'en occupé".format(
            user.mention, data["role_vendeur"]
        ),
        embed=embed,
    )
    pass


bot.run(token)
