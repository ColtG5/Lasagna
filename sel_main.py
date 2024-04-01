import discord
import asyncio
import os
from dotenv import load_dotenv
from sel_scripts.check_course_existence import FindCourseExistence
from sel_scripts.check_course_open_waitlist import FindOpenWaitlist
from data.courses_storage import CoursesStorage

# async def async_check_course_existence(course_info):
#     course_name, semester, check_type = course_info
#     loop = asyncio.get_event_loop()
#     course_checker = FindCourseExistence(course=course_name, semester=semester)
#     # Use loop.run_in_executor to run the synchronous check_course_existence method in a thread pool
#     return await loop.run_in_executor(None, course_checker.check_course_existence)

# async def async_check_course_open_waitlist(course_info):
#     course_name, semester, check_type = course_info
#     loop = asyncio.get_event_loop()
#     course_checker = FindOpenWaitlist(course=course_name, semester=semester)
#     # Use loop.run_in_executor to run the synchronous check_course_open_waitlist method in a thread pool
#     return await loop.run_in_executor(None, course_checker.check_course_open_waitlist)


async def async_check_course(course_info):
    course_name, semester, check_type = course_info
    loop = asyncio.get_event_loop()
    course_checker = None
    if check_type == "Existence":
        course_checker = FindCourseExistence(course=course_name, semester=semester)
    elif check_type == "Open Waitlist":
        course_checker = FindOpenWaitlist(course=course_name, semester=semester)
    # Use loop.run_in_executor to run the synchronous check_course_existence method in a thread pool
    return await loop.run_in_executor(None, course_checker.check_course)


async def main_loop(bot: discord.Client):
    load_dotenv()
    await bot.wait_until_ready()

    while not bot.is_closed():
        print("***Checking all courses: ", end="")
        course_info_list = list(CoursesStorage.get_all_course_infos().keys())
        print(str(course_info_list) + "***")
        for course_info in course_info_list:
            course_name, semester, check_type = course_info
            print(f"Checking course {course_name} for {check_type} in {semester}... ", end="")

            try:
                course_check_true = await async_check_course(course_info)
                # bit hardcoded but idc
                if check_type == "Existence":
                    if course_check_true:
                        print("Course exists!")
                        await CoursesStorage.notify_users(course_info)
                    else:
                        print("Course does not exist.")
                elif check_type == "Open Waitlist":
                    if course_check_true:
                        print("Course has open waitlist!")
                        await CoursesStorage.notify_users(course_info)
                    else:
                        print("Course does not have open waitlist.")
            except Exception as e:
                print(f"Error checking course: {e}")

        print("***Done checking all courses***\n")

        await asyncio.sleep(5)

if __name__ == "__main__":
    main_loop()
