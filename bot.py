from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from discord.ext import commands
import responses
import bot_reminder
import datetime
import sel_scripts.sel_main as sel_main

def run_bot():
    load_dotenv()
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

        # bot.loop.create_task(sel_main.main_loop())

    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        # await interaction.response.send_message(f"Hello {interaction.user.nick}!", ephemeral=True)
        await interaction.response.send_message(f"Hello {interaction.user.nick}!")

    @bot.tree.command(name="say")
    @app_commands.describe(thing_to_say="What should I say?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(
            f"{interaction.user.name} said: {thing_to_say}"
        )

    @bot.tree.command(
        name="new-daily-reminder", description="Create a new daily reminder!"
    )
    @app_commands.describe(
        reminder_title="What should I remind you about?",
        reminder_time="When should I remind you (24 hour time)? e.g. 09:30:00",
        nag_interval="How often should I nag you until you respond? e.g. 00:15:00",
    )
    async def new_reminder(
        interaction: discord.Interaction,
        reminder_title: str,
        reminder_time: str,
        nag_interval: str,
    ):
        try:
            reminder_datetime = datetime.datetime.strptime(reminder_time, "%H:%M:%S")
            print(reminder_time)
            nag_interval_datetime = datetime.datetime.strptime(nag_interval, "%H:%M:%S")
            print(nag_interval)
            if nag_interval_datetime.time() < datetime.time(0, 0, 10):
                raise Exception(
                    "Nag interval must be at least 10 seconds long! Jeez Louise!"
                )

            # actually make the reminder
            reminder = bot_reminder.Reminder(
                interaction.user,
                reminder_title,
                reminder_datetime,
                nag_interval_datetime,
            )

            # await interaction.response.send_message(f"Okay, I'll remind you about `{reminder_title}` at {reminder_datetime.strftime('%H:%M:%S %p')}.") - 24hr time
            await interaction.response.send_message(
                f"Okay, I'll remind you about `{reminder_title}` at {reminder_datetime.strftime('%I:%M %p')} every day."
            )

        except Exception as e:
            print(e)
            await interaction.response.send_message(f"{e}. Please try again.")
            return

    @bot.tree.command(name="list-reminders", description="List all reminders")
    async def list_reminders(interaction: discord.Interaction):
        reminders = bot_reminder.get_reminders()
        if not reminders:
            await interaction.response.send_message("No reminders set.")
            return

        reminder_str = ""
        for reminder in reminders:
            reminder_str += f"{reminder.title} at {reminder.time.strftime('%I:%M %p')}\n"

        await interaction.response.send_message(reminder_str)

    @bot.tree.command(name="delete-reminder", description="Delete a reminder")
    @app_commands.describe(reminder_title="Which reminder should I delete?")
    async def delete_reminder(interaction: discord.Interaction, reminder_title: str):
        reminder = bot_reminder.get_reminder(reminder_title)
        if not reminder:
            await interaction.response.send_message(
                f"No reminder with title `{reminder_title}` found."
            )
            return

        bot_reminder.delete_reminder(reminder)
        await interaction.response.send_message(f"Deleted reminder `{reminder_title}`.")

    @bot.tree.command(name="check-courses", description="Check all courses for if they exist")
    @app_commands.describe()
    async def check_courses(interaction: discord.Interaction):
        sel_main.main_loop(interaction)

    bot.run(os.environ.get("TOKEN"))
