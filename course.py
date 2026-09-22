"""Course - a subject that students can join.

A Course is not a User, so it does not inherit from it. It is a separate
class that keeps its own list of students private.
"""


class Course:
    """One course in the catalogue, for example PY-101 Python Basics."""

    total_courses = 0

    def __init__(self, code, title, capacity=20, mentor=None):
        if not self.is_valid_code(code):
            raise ValueError("Invalid course code: " + str(code) + " (use a form like PY-101)")
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")

        self.code = code.upper()
        self.title = title
        self.mentor = mentor
        self.__capacity = capacity        # private
        self.__students = []              # private list of Student objects
        Course.total_courses += 1

        if mentor is not None:
            mentor.assign_course(self.code)

    # ------------------------------------------------------------------
    # Encapsulation: the seat count can be read but not edited directly
    # ------------------------------------------------------------------
    @property
    def capacity(self):
        return self.__capacity

    def seats_left(self):
        """Return how many free seats are left."""
        return self.__capacity - len(self.__students)

    def is_full(self):
        """Return True when there are no seats left."""
        return self.seats_left() == 0

    # ------------------------------------------------------------------
    # Instance methods
    # ------------------------------------------------------------------
    def add_student(self, student):
        """Put a student on the course, if there is room for them."""
        if self.is_full():
            raise ValueError(self.code + " is full (" + str(self.__capacity) + " seats)")
        if student in self.__students:
            raise ValueError(student.name + " is already enrolled in " + self.code)
        self.__students.append(student)

    def remove_student(self, student):
        """Take a student off the course and free their seat."""
        if student not in self.__students:
            raise ValueError(student.name + " is not enrolled in " + self.code)
        self.__students.remove(student)

    def student_names(self):
        """Return a COPY of the student names, so the private list is safe."""
        return [student.name for student in self.__students]

    def set_mentor(self, mentor):
        """Give the course a mentor and tell the mentor about the course."""
        mentor.assign_course(self.code)
        self.mentor = mentor

    def describe(self):
        """Return one line describing the course."""
        mentor_name = self.mentor.name if self.mentor else "not assigned"
        return (self.code + " " + self.title + " | mentor: " + mentor_name
                + " | " + str(len(self.__students)) + "/" + str(self.__capacity) + " seats taken")

    # ------------------------------------------------------------------
    # Static method - checks a code without needing a course object
    # ------------------------------------------------------------------
    @staticmethod
    def is_valid_code(code):
        """Return True for codes like PY-101: letters, a dash, then numbers."""
        if not isinstance(code, str) or code.count("-") != 1:
            return False
        letters, numbers = code.split("-")
        return letters.isalpha() and numbers.isdigit()

    # ------------------------------------------------------------------
    # Class method - build a Course from one line of text
    # ------------------------------------------------------------------
    @classmethod
    def from_text(cls, text):
        """Create a Course from a line like 'PY-101,Python Basics,25'."""
        parts = [part.strip() for part in text.split(",")]
        if len(parts) != 3:
            raise ValueError("Expected 3 values: code,title,capacity")
        return cls(parts[0], parts[1], int(parts[2]))

    def __str__(self):
        return self.code + " - " + self.title
