import asyncio
from sel_scripts.find_cpsc599 import FindCpsc599

# Assume more scripts like FindCpsc599 can be added here
files_to_run = [FindCpsc599]

async def check_course_existence(check_class):
    obj = check_class()
    obj.setup_method()
    try:
        # Run the blocking method in a separate thread
        exists = await asyncio.to_thread(obj.does_cpsc599_exist)
        if exists:
            print(f"{check_class.__name__}: CPSC 599 exists!")
        else:
            print(f"{check_class.__name__}: CPSC 599 does not exist!")
    finally:
        obj.teardown_method()

async def main_loop():
    while True:
        # Run checks for all courses concurrently
        await asyncio.gather(*(check_course_existence(check_class) for check_class in files_to_run))
        await asyncio.sleep(60)  # Non-blocking sleep for 60 seconds

if __name__ == "__main__":
    asyncio.run(main_loop())
