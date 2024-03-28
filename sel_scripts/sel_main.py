import time
import asyncio
from sel_scripts.find_cpsc599 import FindCpsc599
files_to_run = [FindCpsc599]

async def check_if_courses_exist():
    for file in files_to_run:
        obj = file()
        obj.setup_method()
        if obj.does_cpsc599_exist():
            print("CPSC 599 exists!")
        else:
            print("CPSC 599 does not exist!")
        obj.teardown_method()

async def main_loop():
    while True:
        await check_if_courses_exist()
        await asyncio.sleep(60)

