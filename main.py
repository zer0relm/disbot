import dotenv
import discord
from discord.ext import commands
from discord import commands
import sqlbot

import random


MY_GUILD = discord.Object(id=dotenv.dotenv_values("discord.env")['GUILD_ID'])

class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

sql_connector = sqlbot.SqlBot()

intents = discord.Intents.default()
intents.message_content = True
#client = MyClient(intents=intents)
client = discord.Bot(intents=intents)
shocked_emoji = client.get_emoji(1439750626656522390)
keyword_list = sql_connector.getKeywords()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #await bot.sync()

@client.event
async def on_message(message):
    global keyword_list
    if message.author == client.user:
        return
    for keyword in keyword_list:
        word = keyword[1].lower()
        emoji = keyword[2]
        user = keyword[3]

        if word in message.content.lower():
            if user != None:
                print(user)
                if user == str(message.author):
                    await message.add_reaction(emoji)
            else:
                await message.add_reaction(emoji)

    # if "sword" in message.content.lower():
    #     await message.add_reaction("<:gremlin_w_parent:1424791312409952257>")
    # elif "swords" in message.content.lower():
    #     await message.add_reaction()
    #     #sql_connector.getTicks()
    # elif "lizard" in message.content.lower():
    #     await message.add_reaction('\N{LIZARD}')

@client.slash_command(name="quote", description="returns a random quote")
async def quote(interaction: discord.Interaction):
    #await interaction.response.send_message(quote)
    quote = sql_connector.getRandomQuote()
    await interaction.response.send_message("Quote #{}: '{}' - {}".format(quote[0], quote[1], quote[3]))

@client.slash_command(name="add_quote", description="Add quote to list")
async def add_quote(interaction: discord.Interaction, quote: str, user: discord.User = None):
    if user is None:
        user = interaction.user.name
    quote_return = sql_connector.addQuote(quote, user)
    await interaction.response.send_message("Quote #{}: '{}' - {}".format(quote_return[0], quote_return[1], quote_return[3]))

@client.slash_command(name="get_specific_quote", description="Returns a specific quote")
async def get_specific_quote(interaction: discord.Interaction, quote_id: str):
    quote = sql_connector.getSpecificQuote(quote_id)
    await interaction.response.send_message("Quote #{}: '{}' - {}".format(quote[0], quote[1], quote[3]))

@client.slash_command(name="add_keyword", description="Add Keyword and emoji to list")
async def add_keyword(interaction: discord.Interaction, keyword: str, emoji: str, user: discord.User = None):
    global keyword_list
    print(str(emoji))
    if user is None:
        response = sql_connector.addKeyword(keyword, emoji)
        keyword_list = sql_connector.getKeywords()
        await interaction.response.send_message(f"Keyword #{response[0]}: {response[1]} for everyone", ephemeral=True)
    else:
        response = sql_connector.addUserKeyword(keyword, emoji, str(user))
        keyword_list = sql_connector.getKeywords()
        await interaction.response.send_message(f"Keyword #{response[0]}: {response[1]} for {response[2]}", ephemeral=True)

@client.slash_command(name="remove_keyword", description="Remove Keyword and emoji from list")
async def remove_keyword(interaction: discord.Interaction, keyword: str, user: discord.User = None):
    global keyword_list
    if user is None:
        sql_connector.removeKeyword(keyword)
    else:
        sql_connector.removeUserKeyword(keyword, user)
    await interaction.response.send_message(f"{keyword} removed", ephemeral=True)

# @client.slash_command(name="test_emojis", description="Test emojis on list")
# async def test_emoji(interaction: discord.Interaction, emoji: str):
#     print(emoji)
#     print(str(emoji))
#     print(emoji.startswith("<:"))
#     await interaction.response.send_message("recieved emoji '{}'".format(emoji))


client.run(dotenv.dotenv_values("discord.env")['DISCORD_TOKEN'])
