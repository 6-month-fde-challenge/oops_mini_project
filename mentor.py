"""Mentor - a user who teaches courses.

Mentor inherits from the same User base class as Student, but answers the
abstract methods in its own way. That is POLYMORPHISM: one method name,
different behaviour depending on the class.
"""

from user import User


class Mentor(User):
    """A teacher in the system."""

    id_prefix = "MEN"          # overrides the prefix from User
    created = 0                # mentors are numbered MEN-001, MEN-002 ...
    MAX_COURSES = 3            # a mentor may teach at most three courses

    def __init__(self, name, email, subject="General", hourly_rate=50):
        super().__init__(name, email)
        self.subject = subject
        self.__hourly_rate = 0                 # private, set through the property
        self.hourly_rate = hourly_rate
        self.courses = []                      # course codes this mentor teaches

    # ------------------------------------------------------------------
    # Encapsulation: the rate is private and checked before it is stored
    # ------------------------------------------------------------------
    @property
    def hourly_rate(self):
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        if not self.is_valid_rate(value):
            raise ValueError("Hourly rate must be a number between 10 and 500")
        self.__hourly_rate = value

    # ------------------------------------------------------------------
    # Polymorphism: same method names as Student, different answers
    # ------------------------------------------------------------------
    def role(self):
        return "Mentor"

    def describe(self):
        return (self.name + " teaches " + self.subject + " and handles "
                + str(len(self.courses)) + " of " + str(self.MAX_COURSES) + " courses.")

    # ------------------------------------------------------------------
    # Instance methods
    # ------------------------------------------------------------------
    def assign_course(self, course_code):
        """Give this mentor one more course to teach."""
        if len(self.courses) >= self.MAX_COURSES:
            raise ValueError(self.name + " already teaches " + str(self.MAX_COURSES) + " courses")
        if course_code in self.courses:
            raise ValueError(self.name + " already teaches " + course_code)
        self.courses.append(course_code)

    def is_available(self):
        """Return True if the mentor can take another course."""
        return len(self.courses) < self.MAX_COURSES

    def calculate_fee(self, hours):
        """Return the fee for a number of teaching hours."""
        if hours < 0:
            raise ValueError("Hours cannot be negative")
        return round(self.hourly_rate * hours, 2)

    # ------------------------------------------------------------------
    # Static method - checks a value without needing a mentor object
    # ------------------------------------------------------------------
    @staticmethod
    def is_valid_rate(rate):
        """Return True if the rate is a number inside the allowed range."""
        return isinstance(rate, (int, float)) and 10 <= rate <= 500

    # ------------------------------------------------------------------
    # Class method - a shortcut for creating a senior mentor
    # ------------------------------------------------------------------
    @classmethod
    def senior(cls, name, email, subject):
        """Create a mentor on the senior rate."""
        return cls(name, email, subject, hourly_rate=200)
