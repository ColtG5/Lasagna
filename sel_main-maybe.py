import discord
import asyncio
import os
from dotenv import load_dotenv
from sel_scripts.check_course_existence import FindCourse
from data.courses_storage import CoursesStorage


async def main_loop():
    load_dotenv()

    while True:
        print("Checking for course existence for courses...")
        course_names = CoursesStorage.get_all_courses()
        for course_name in course_names:
            print(f"Checking for course {course_name}")
            
            course_checker = FindCourse(course=course_name)
            course_exists = course_checker.check_course_existence()

            if course_exists:
                # need to notify all users that signed up to hear when that course now exists
                print(f"Course {course_name} exists! Notifying users...")
                for user_id in course_names[course_name]:
                    user = await bot.fetch_user(user_id)
                    await user.send(f"Hey {user.name}, course {course_name} now exists in the schedule builder!")

                CoursesStorage.delete_course(course_name) # should be able to delete the course now that it exists
                print(f"Done notifying users for course {course_name}")
            else:
                print(f"Course {course_name} does not exist yet")

        print("Done checking for course existence")
        await asyncio.sleep(30)

if __name__ == "__main__":
    main_loop()
