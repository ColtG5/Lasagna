import discord
import asyncio
import os
from dotenv import load_dotenv
from sel_scripts.check_course_existence import FindCourse
from data.courses_storage import CoursesStorage


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
        course_names_copy = list(CoursesStorage.get_all_courses().keys())
        print(course_names_copy)
        for course_name in course_names_copy:
            print(f"Checking for course {course_name}")
            
            course_exists = await async_check_course_existence(course_name)

            if course_exists:
                # need to notify all users that signed up to hear when that course now exists
                notification_tasks = []
                all_users_for_course = CoursesStorage.get_course_users(course_name)
                for user in all_users_for_course:  
                    task = asyncio.create_task(user.send(f"**Hey {user.name}, course {course_name} now exists in the schedule builder!**"))
                    notification_tasks.append(task)

                # Wait for all notifications to be sent out
                if notification_tasks:
                    await asyncio.gather(*notification_tasks)

                CoursesStorage.delete_course(course_name) # should be able to delete the course now that it exists
                print(f"Done notifying users for course {course_name}")
            else:
                print(f"Course {course_name} does not exist yet")

        print("Done checking for course existence")
        await asyncio.sleep(30)

if __name__ == "__main__":
    main_loop()
