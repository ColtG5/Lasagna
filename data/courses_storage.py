import datetime
import discord
import asyncio
from typing import Dict, List, Tuple

class CoursesStorage:
    # {
    #   ("AAAA 000", "2024 Fall", "Open Waitlist"): [user1, user2, user3],
    #   ("AAAA 001", "2025 Winter", "Existence"): [user4, user5, user2],
    # }
    _courses_for_existence: Dict[Tuple[str, str, str], List[discord.User]] = {}

    @classmethod
    def _log_action(cls, message):
        with open("course_stuff_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    # adds a user to a course. creates course if course does not exist
    @classmethod
    def add_user_to_course(cls, course_info: Tuple[str, str, str], user: discord.User) -> bool:
        if course_info not in cls._courses_for_existence:
            cls._courses_for_existence[course_info] = []
            cls._log_action(f"Created new course: {course_info[0]} for semester {course_info[1]} checking for {course_info[2]}.")
        
        if user not in cls._courses_for_existence[course_info]:
            cls._courses_for_existence[course_info].append(user)
            cls._log_action(f"Added user {user} to course {course_info[0]} for semester {course_info[1]} checking for {course_info[2]}.")
            cls.write_state_to_file()
            return True
        return False

    # # gets all users for a course
    # @classmethod
    # def get_course_users(cls, course_info: Tuple[str, str]):
    #     return cls._courses_for_existence.get(course_info, [])

    # gets all courses
    @classmethod
    def get_all_course_infos(cls):
        return cls._courses_for_existence

    # notify all users that this course has been added!! (and delete the course from storage since no need to check it anymore)
    @classmethod
    async def notify_users(cls, course_info: Tuple[str, str, str]):
        if course_info in cls._courses_for_existence:
            users = cls._courses_for_existence[course_info]

            # kinda hard coded but oh well
            if (course_info[2] == "Open Waitlist"):
                notification_tasks = [asyncio.create_task(user.send(f"**Hey {user.name}, {course_info[0]} for {course_info[1]} now has an open waitlist!**")) for user in users]
            if (course_info[2] == "Existence"):
                notification_tasks = [asyncio.create_task(user.send(f"**Hey {user.name}, {course_info[0]} for {course_info[1]} now exists in schedule builder!**")) for user in users]
            
            await asyncio.gather(*notification_tasks)
            user_names = ", ".join(user.name for user in users)
            cls._log_action(f"Notified {user_names} for course {course_info}.")
            del cls._courses_for_existence[course_info]
            cls.write_state_to_file()

    # removes a user from a course
    @classmethod
    def remove_user_from_course(cls, course_info: Tuple[str, str, str], user: discord.User) -> bool:
        if course_info in cls._courses_for_existence and user in cls._courses_for_existence[course_info]:
            cls._courses_for_existence[course_info].remove(user)
            cls._log_action(f"Removed user {user.name} from course {course_info}.")
            cls.write_state_to_file()
            return True
        return False
    
    # write state of courses_for_existence to a file
    @classmethod
    def write_state_to_file(cls):
        with open("courses_storage.txt", "w") as storage_file:
            for (class_name, semester, check_type), users in cls._courses_for_existence.items():
                user_data = [f"{user.name} | {user.id}" for user in users]
                course_info_str = f"{class_name}, {semester}, {check_type}"
                storage_file.write(f"({course_info_str}) : {', '.join(user_data)}\n")

    # load state of courses_for_existence from a file
    @classmethod
    async def load_state_from_file(cls, bot):
        cls._courses_for_existence.clear()
        with open("courses_storage.txt", "r") as storage_file:
            for line in storage_file:
                if not line.strip():
                    continue

                line_cleaned = line.strip()[1:] # remove the leading "("
                course_info_str, user_data_str = line_cleaned.split(") : ") # split course info and user data, and remove trailing ")"
                
                class_name, semester, check_type = [info.strip() for info in course_info_str.split(",")]
                
                user_ids = [user_str.split(" | ")[1].strip() for user_str in user_data_str.split(", ")]
                
                users = await asyncio.gather(*[bot.fetch_user(int(user_id)) for user_id in user_ids])
                cls._courses_for_existence[(class_name, semester, check_type)] = users

