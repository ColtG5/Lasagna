import datetime
import asyncio

class CoursesExistenceStorage:
    _courses_for_existence = {}

    @classmethod
    def _log_action(cls, message):
        with open("course_stuff_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    # adds a user to a course. creates course if course does not exist
    @classmethod
    def add_user_to_course(cls, course_name, user) -> bool:
        if course_name not in cls._courses_for_existence:
            cls._courses_for_existence[course_name] = []
            cls._log_action(f"Created new course: {course_name}.")
        
        if user not in cls._courses_for_existence[course_name]:
            cls._courses_for_existence[course_name].append(user)
            cls._log_action(f"Added user {user} to course {course_name}.")
            cls.write_state_to_file() # maybe here?
            return True
        return False

    # gets all users for a course
    @classmethod
    def get_course_users(cls, course_name):
        return cls._courses_for_existence.get(course_name, [])

    # gets all courses
    @classmethod
    def get_all_courses(cls):
        return cls._courses_for_existence

    # notify all users that this course has been added!! (and delete the course from storage since no need to check it anymore)
    @classmethod
    async def notify_users(cls, course_name):
        notification_tasks = []
        all_users_for_course = cls.get_course_users(course_name)
        for user in all_users_for_course:  
            task = asyncio.create_task(user.send(f"**Hey {user.name}, course {course_name} now exists in the schedule builder!**"))
            notification_tasks.append(task)

        # Wait for all notifications to be sent out
        if notification_tasks:
            await asyncio.gather(*notification_tasks)
        # log everyone we notified
        user_names = ", ".join([user.name for user in all_users_for_course])
        cls._log_action(f"Notified {user_names} for course {course_name} (and deleted that course).")


        if course_name in cls._courses_for_existence:
            del cls._courses_for_existence[course_name]
            # cls._log_action(f"Deleted course: {course_name}.")
        
        cls.write_state_to_file()

    # removes a user from a course
    @classmethod
    def remove_user_from_course(cls, course_name, user) -> True:
        if course_name in cls._courses_for_existence and user in cls._courses_for_existence[course_name]:
            cls._courses_for_existence[course_name].remove(user)
            cls._log_action(f"Removed user {user} from course {course_name}.")
            cls.write_state_to_file()
            return True
        return False
    
    # write state of courses_for_existence to a file
    @classmethod
    def write_state_to_file(cls):
        with open("courses_storage.txt", "w") as storage_file:
            for course_name, users in cls._courses_for_existence.items():
                user_data = [f"{user.name}|{user.id}" for user in users]
                storage_file.write(f"{course_name}: {', '.join(user_data)}\n")

    @classmethod
    # load state of courses_for_existence from a file
    async def load_state_from_file(cls, bot):
        cls._courses_for_existence.clear()  # Clear existing data
        with open("courses_storage.txt", "r") as storage_file:
            for line in storage_file:
                course_name, user_data_str = line.strip().split(": ")
                user_ids = [user_str.split("|")[1] for user_str in user_data_str.split(", ")]
                cls._courses_for_existence[course_name] = [await bot.fetch_user(int(user_id)) for user_id in user_ids]
