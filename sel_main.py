import discord
import asyncio
import os
from dotenv import load_dotenv
from sel_scripts.check_course_existence import FindCourse
from data.courses_storage import CoursesExistenceStorage

async def async_check_course_existence(course_info):
    course_name, semester = course_info
    loop = asyncio.get_event_loop()
    course_checker = FindCourse(course=course_name, semester=semester)
    # Use loop.run_in_executor to run the synchronous check_course_existence method in a thread pool
    return await loop.run_in_executor(None, course_checker.check_course_existence)

async def main_loop(bot: discord.Client):
    load_dotenv()
    await bot.wait_until_ready()

    while not bot.is_closed():
        print("Checking for course existence for courses: ", end="")
        course_info_list = list(CoursesExistenceStorage.get_all_course_infos().keys())
        print(course_info_list)
        for course_info in course_info_list:
            course_name, semester = course_info
            print(f"Checking for course {course_name}")
            
            course_exists = await async_check_course_existence(course_info=course_info)

            if course_exists:
                await CoursesExistenceStorage.notify_users(course_info=course_info)
                print(f"Course {course_name} exists! Notified users for course {course_name} in semester {semester}")
            else:
                print(f"Course {course_name} in semester {semester} does not exist yet")

        print("Done checking for course existence\n\n")
        await asyncio.sleep(5)

if __name__ == "__main__":
    main_loop()
