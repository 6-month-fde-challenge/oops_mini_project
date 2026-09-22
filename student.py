"""Student - a user who joins courses and receives grades.

INHERITANCE: Student inherits everything from User (name, email, ID,
profile) and only adds what a student needs.
"""

from user import User


class Student(User):
    """A learner in the system."""

    id_prefix = "STU"          # overrides the prefix from User
    created = 0                # students are numbered STU-001, STU-002 ...
    PASS_MARK = 40

    def __init__(self, name, email, program="General"):
        super().__init__(name, email)          # reuse the User constructor
        self.program = program
        self.__grades = {}                     # private: {course_code: score}

    # ------------------------------------------------------------------
    # POLYMORPHISM: the two methods User left abstract, answered in the
    # way a Student answers them
    # ------------------------------------------------------------------
    def role(self):
        return "Student"

    def describe(self):
        return (self.name + " studies " + self.program + " and has completed "
                + str(len(self.__grades)) + " course(s).")

    # ------------------------------------------------------------------
    # Instance methods
    # ------------------------------------------------------------------
    def add_grade(self, course_code, score):
        """Save a score for a course (the only way into the private dict)."""
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValueError("Score must be a number between 0 and 100")
        self.__grades[course_code] = score
        return self.grade_letter(score)

    def get_grades(self):
        """Return a COPY of the grades, so the private dict stays safe."""
        return dict(self.__grades)

    def average(self):
        """Return the average score, or 0 when there are no grades yet."""
        if not self.__grades:
            return 0.0
        return round(sum(self.__grades.values()) / len(self.__grades), 2)

    def has_passed(self, course_code):
        """Return True if the student passed that course."""
        return self.__grades.get(course_code, 0) >= self.PASS_MARK

    def report_card(self):
        """Return a small report built from the private grades."""
        lines = ["Report card for " + self.name + " (" + self.user_id + ")"]
        if not self.__grades:
            lines.append("  no grades yet")
        else:
            for code, score in sorted(self.__grades.items()):
                lines.append("  " + code + ": " + str(score) + " (" + self.grade_letter(score) + ")")
            lines.append("  average: " + str(self.average()))
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Static method - converting a score to a letter needs no object
    # ------------------------------------------------------------------
    @staticmethod
    def grade_letter(score):
        """Turn a score into a letter grade."""
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        if score >= 55:
            return "C"
        if score >= 40:
            return "D"
        return "F"

    # ------------------------------------------------------------------
    # Class method - a second way to build a Student
    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data):
        """Create a Student from a dictionary, for example loaded from a file."""
        return cls(data["name"], data["email"], data.get("program", "General"))
