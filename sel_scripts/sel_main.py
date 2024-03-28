import time
from find_cpsc599 import (
    FindCpsc599,
)  # Replace 'your_script_name' with the actual name of your Python file containing the FindCpsc599 class.


async def check_if_course_exists(check_function):
    """
    Executes a given course check function and prints the result.

    Args:
    check_function (function): A function to check course availability.
    """
    result = await check_function()
    if result:
        print("The course was found!!!!")
    else:
        print("The course was NOT found :(")


async def main_loop():
    # Instance of the FindCpsc599 class
    cpsc599_checker = FindCpsc599()
    cpsc599_checker.setup_method()  # Remember to call teardown_method() appropriately if using setup/teardown in the loop

    try:
        while True:
            await check_if_course_exists(cpsc599_checker.find_cpsc599)

            # Wait for 2 minutes before checking again
            await time.sleep(120)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    finally:
        cpsc599_checker.teardown_method()
