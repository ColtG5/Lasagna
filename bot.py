from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from discord.ext import commands
import responses
import bot_responses

load_dotenv()


def run_bot():
    # intents = discord.Intents.default()
    # intents.message_content = True
    bot = commands.Bot(command_prefix="!L ", intents=discord.Intents.all())
    # bot.remove_command('help')

    @bot.event
    async def on_ready():
        print(f"{bot.user} is running!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)!")
        except Exception as e:
            print(e)

    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        # await interaction.response.send_message(f"Hello {interaction.user.nick}!", ephemeral=True)
        await interaction.response.send_message(f"Hello {interaction.user.nick}!")

    @bot.tree.command(name="say")
    @app_commands.describe(thing_to_say="What should I say?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}")

    @bot.tree.command(name="new_reminder")
    @app_commands.describe(reminder="What should I remind you about?", reminder_time="When should I remind you?", nag_interval="How often should I remind you?")
    async def new_reminder(interaction: discord.Interaction, reminder: str, reminder_time: str, nag_interval: str):
        await interaction.response.send_message(f"Okay, I'll remind you about {reminder} at {reminder_time} every {nag_interval}.")

    


    # @bot.event
    # async def on_message(message):
    #     if message.author == bot.user or str(message.content)[:3] != "!L ": 
    #         return
        
    #     user_message = str(message.content[3:])
    #     print(f"{message.author}: {user_message} ({message.channel} in {message.guild})")
        
    #     for i in dir(bot_responses):
    #         function = getattr(bot_responses, i)
    #         if i.startswith('f_') and callable(function):
    #             await function(bot, message, user_message)


    bot.run(os.environ.get('TOKEN'))


    