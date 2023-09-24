from dotenv import load_dotenv
import os
import discord
import responses
import bot_responses

load_dotenv()


def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is running!")

    @client.event
    async def on_message(message):
        if message.author == client.user or str(message.content)[:3] != "!L ": 
            return
        
        user_message = str(message.content[3:])
        print(f"{message.author}: {user_message} ({message.channel} in {message.guild})")
        
        for i in dir(bot_responses):
            function = getattr(bot_responses, i)
            if i.startswith('f_') and callable(function):
                await function(client, message, user_message)


    client.run(os.environ.get('TOKEN'))


    