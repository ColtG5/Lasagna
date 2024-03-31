import datetime

class CoursesStorage:
    _courses_for_existence = {}

    @classmethod
    def _log_action(cls, message):
        """Helper method to log actions to a file."""
        """what is this"""
        "huh"
        'bruh'
        with open("course_stuff_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    # adds a user to a course. creates course if course does not exist
    @classmethod
    def add_user_to_course(cls, course_name, user_id) -> bool:  
        if course_name not in cls._courses_for_existence:
            cls._courses_for_existence[course_name] = []
            cls._log_action(f"Created new course: {course_name}.")
        
        if user_id not in cls._courses_for_existence[course_name]:
            cls._courses_for_existence[course_name].append(user_id)
            cls._log_action(f"Added user {user_id} to course {course_name}.")
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

    # deletes a course (prob shouldn't need this)
    @classmethod
    def delete_course(cls, course_name):
        if course_name in cls._courses_for_existence:
            del cls._courses_for_existence[course_name]
            cls._log_action(f"Deleted course: {course_name}.")

    # removes a user from a course
    @classmethod
    def remove_user_from_course(cls, course_name, user_id) -> True:
        if course_name in cls._courses_for_existence and user_id in cls._courses_for_existence[course_name]:
            cls._courses_for_existence[course_name].remove(user_id)
            cls._log_action(f"Removed user {user_id} from course {course_name}.")
            return True
        return False