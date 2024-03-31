import discord
import asyncio
import os
from dotenv import load_dotenv
from sel_scripts.check_course_existence import FindCourse

def main_loop(interaction: discord.Interaction):
    load_dotenv()

    course = "CPSC 599"
    username = os.getenv("UCAL_USERNAME")
    password = os.getenv("UCAL_PASSWORD")
    find_cpsc599 = FindCourse(course, username, password)
    find_cpsc599.setup_method()

    if find_cpsc599.does_course_exist():
        print(f"{course} exists")
        interaction.response.send_message(f"{course} exists")
    else:
        print(f"{course} does not exist")
        interaction.response.send_message(f"{course} does not exist")
    find_cpsc599.teardown_method()

if __name__ == "__main__":
    main_loop()
