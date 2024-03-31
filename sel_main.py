import discord
import asyncio
import os
from dotenv import load_dotenv
from sel_scripts.check_course_existence import FindCourse
from data.courses_storage import CoursesExistenceStorage

async def async_check_course_existence(course_name):
    loop = asyncio.get_event_loop()
    course_checker = FindCourse(course=course_name)
    # Use loop.run_in_executor to run the synchronous check_course_existence method in a thread pool
    return await loop.run_in_executor(None, course_checker.check_course_existence)

async def main_loop(bot: discord.Client):
    load_dotenv()
    await bot.wait_until_ready()

    while not bot.is_closed():
        print("Checking for course existence for courses: ", end="")
        course_names_copy = list(CoursesExistenceStorage.get_all_courses().keys())
        print(course_names_copy)
        for course_name in course_names_copy:
            print(f"Checking for course {course_name}")
            
            course_exists = await async_check_course_existence(course_name)

            if course_exists:
                await CoursesExistenceStorage.notify_users(course_name)
                print(f"Course {course_name} exists! Notified users for course {course_name}")
            else:
                print(f"Course {course_name} does not exist yet")

        print("Done checking for course existence")
        await asyncio.sleep(5)

if __name__ == "__main__":
    main_loop()
