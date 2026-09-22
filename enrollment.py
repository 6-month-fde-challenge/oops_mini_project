"""Enrollment - the link between one student and one course.

The Enrollment keeps the facts that belong to neither class on its own:
when the student joined, whether they are still on the course, and the
final score.
"""

from datetime import date


class Enrollment:
    """One student joined to one course."""

    total_enrollments = 0

    def __init__(self, student, course):
        # Ask the course for a seat first. If the course is full or the
        # student is already on it, this raises and no enrollment is made.
        course.add_student(student)

        Enrollment.total_enrollments += 1
        self.student = student
        self.course = course
        self.date_joined = date.today()
        self.reference = self.make_reference(student.user_id, course.code)
        self.__status = "active"          # private: active, completed or dropped
        self.__score = None               # private: filled in when completed

    # ------------------------------------------------------------------
    # Encapsulation: status and score are read-only from outside.
    # They change only through complete() and drop().
    # ------------------------------------------------------------------
    @property
    def status(self):
        return self.__status

    @property
    def score(self):
        return self.__score

    def is_active(self):
        """Return True while the student is still taking the course."""
        return self.__status == "active"

    # ------------------------------------------------------------------
    # Instance methods
    # ------------------------------------------------------------------
    def complete(self, score):
        """Finish the course with a score and save the grade on the student."""
        if not self.is_active():
            raise ValueError(self.reference + " is already " + self.__status)
        letter = self.student.add_grade(self.course.code, score)
        self.__score = score
        self.__status = "completed"
        return letter

    def drop(self, reason=""):
        """Leave the course and give the seat back to it."""
        if not self.is_active():
            raise ValueError(self.reference + " is already " + self.__status)
        self.course.remove_student(self.student)
        self.__status = "dropped"
        self.reason = reason

    def describe(self):
        """Return one line describing this enrollment."""
        grade = self.student.grade_letter(self.__score) if self.__score is not None else "-"
        return (self.reference + " | " + self.student.name + " | " + self.course.code
                + " | " + self.__status + " | grade: " + grade)

    # ------------------------------------------------------------------
    # Static method - builds the reference text, no object needed
    # ------------------------------------------------------------------
    @staticmethod
    def make_reference(student_id, course_code):
        """Build a reference like ENR-STU001-PY101."""
        return "ENR-" + student_id.replace("-", "") + "-" + course_code.replace("-", "")

    # ------------------------------------------------------------------
    # Class method - enroll one student in several courses at once
    # ------------------------------------------------------------------
    @classmethod
    def enroll_in_many(cls, student, courses):
        """Return a list of Enrollments, skipping courses that are full."""
        enrollments = []
        for course in courses:
            if course.is_full():
                print("  skipped " + course.code + ": no seats left")
                continue
            enrollments.append(cls(student, course))
        return enrollments

    def __str__(self):
        return self.student.name + " -> " + self.course.code + " (" + self.__status + ")"
