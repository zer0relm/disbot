import dotenv
import discord
from discord.ext import commands
from discord import app_commands, SelectMenu
import sqlbot

import random


MY_GUILD = discord.Object(id=dotenv.dotenv_values("test_discord.env")['GUILD_ID'])

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
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

sql_connector = sqlbot.sqlBot()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
shocked_emoji = client.get_emoji(1439750626656522390)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #await bot.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "sword" in message.content.lower():
        await message.add_reaction("<:emoji_1:1439750626656522390>")
    elif "swords" in message.content.lower():
        await message.add_reaction()
        #sql_connector.getTicks()
    elif "lizard" in message.content.lower():
        await message.add_reaction('\N{LIZARD}')

@client.tree.command(name="quote", description="returns a random quote")
async def quote(interaction: discord.Interaction):
    #await interaction.response.send_message(quote)
    quote = sql_connector.getRandomQuote()
    await interaction.response.send_message("Quote #{}: '{}' - {}".format(quote[0], quote[1], quote[3]))

@client.tree.command(name="add_quote", description="Add quote to list")
async def add_quote(interaction: discord.Interaction, quote: str, user: str = None):
    if user is None:
        user = interaction.user.name
    quote_return = sql_connector.addQuote(quote, user)
    await interaction.response.send_message("Quote #{}: '{}' - {}".format(quote_return[0], quote_return[1], quote_return[3]))

# @client.tree.command(name="register_mental_illness", description="Add tick to list")
# async def add_tick(interaction: discord.Interaction, tick: str, user: discord.User = None):
#     if user is None:
#         response = sql_connector.addTick(tick)
#         await interaction.response.send_message(f"Tick #{response[0]}: {response[1]} for everyone", ephemeral=True)
#     else:
#         response = sql_connector.addUserTick(tick, str(user.name))
#         await interaction.response.send_message(f"Tick #{response[0]}: {response[1]} for {response[2]}", ephemeral=True)
#
# @client.tree.command(name="get_tick")
# async def get_tick(interaction: discord.Interaction):
#     ticks = sql_connector.getTicks()
#     for word in ticks:
#         print(word)
#     await interaction.response.send_message("Successfully fetched ticks", ephemeral=True)


client.run(dotenv.dotenv_values("test_discord.env")['DISCORD_TOKEN'])
