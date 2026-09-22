"""Course Management System - demo program.

Run it with:

    python main.py

Each section below shows one OOP idea with real output from the classes.
"""

from user import User
from student import Student
from mentor import Mentor
from course import Course
from enrollment import Enrollment

REPORT_FILE = "report.local.txt"


def title(text):
    """Print a section heading."""
    print()
    print("=" * 70)
    print(text)
    print("=" * 70)


def main():
    # ------------------------------------------------------------------
    title("1. ABSTRACTION - User cannot be created directly")
    # ------------------------------------------------------------------
    try:
        User("Nobody", "nobody@example.com")
    except TypeError as error:
        print("Creating a User failed, as expected:")
        print("  ", error)
    print("Only Student and Mentor, which fill in role() and describe(), can be created.")

    # ------------------------------------------------------------------
    title("2. INHERITANCE - Student and Mentor are Users")
    # ------------------------------------------------------------------
    ada = Student("Ada Lovelace", "ada@example.com", "Computer Science")
    alan = Student.from_dict({"name": "Alan Turing", "email": "alan@example.com",
                              "program": "Mathematics"})
    grace = Student("Grace Hopper", "grace@example.com", "Software Engineering")
    liskov = Mentor.senior("Barbara Liskov", "barbara@example.com", "OOP")
    knuth = Mentor("Donald Knuth", "knuth@example.com", "Algorithms", hourly_rate=150)

    for person in [ada, liskov]:
        print(person.show_profile(), "   <- show_profile() is inherited from User")
    print("Is Ada a User?", isinstance(ada, User))
    print("Is Barbara a User?", isinstance(liskov, User))
    print("Students created:", Student.created, "| Mentors created:", Mentor.created,
          "| Total users:", User.count())

    # ------------------------------------------------------------------
    title("3. ENCAPSULATION - private data behind properties")
    # ------------------------------------------------------------------
    ada.add_grade("PY-101", 88)
    copy_of_grades = ada.get_grades()
    copy_of_grades["FAKE-999"] = 100
    print("Someone edited the copy returned by get_grades():", copy_of_grades)
    print("The real grades are untouched:              ", ada.get_grades())

    print("\nBad values are refused, not stored:")
    for description, action in [
        ("ada.email = 'broken-email'", lambda: setattr(ada, "email", "broken-email")),
        ("ada.add_grade('PY-101', 150)", lambda: ada.add_grade("PY-101", 150)),
        ("liskov.hourly_rate = 9000", lambda: setattr(liskov, "hourly_rate", 9000)),
        ("ada.user_id = 'STU-999'", lambda: setattr(ada, "user_id", "STU-999")),
    ]:
        try:
            action()
            print("  ", description, "-> NOT BLOCKED")
        except (ValueError, AttributeError) as error:
            print("  ", description, "->", error)
    print("Ada still has:", ada.email, "| grades:", ada.get_grades())

    # ------------------------------------------------------------------
    title("4. POLYMORPHISM - same method name, different answers")
    # ------------------------------------------------------------------
    people = [ada, alan, grace, liskov, knuth]
    for person in people:
        print(person.role().ljust(8), "|", person.describe())
    print("\nThe loop above never checks which class it is holding.")

    # ------------------------------------------------------------------
    title("5. INSTANCE, STATIC AND CLASS METHODS")
    # ------------------------------------------------------------------
    print("Instance method  liskov.calculate_fee(10) =", liskov.calculate_fee(10))
    print("Instance method  ada.average()            =", ada.average())
    print()
    print("Static method    User.is_valid_email('a@b.com')  =", User.is_valid_email("a@b.com"))
    print("Static method    User.is_valid_email('a.b.com')  =", User.is_valid_email("a.b.com"))
    print("Static method    Student.grade_letter(72)        =", Student.grade_letter(72))
    print("Static method    Course.is_valid_code('PY-101')  =", Course.is_valid_code("PY-101"))
    print("   (all called on the class, with no object needed)")
    print()
    print("Class method     Student.from_dict(...)  ->", alan.name, "|", alan.program)
    print("Class method     Mentor.senior(...)      ->", liskov.name, "| rate:", liskov.hourly_rate)

    # ------------------------------------------------------------------
    title("6. COURSES AND ENROLLMENTS")
    # ------------------------------------------------------------------
    python_course = Course("PY-101", "Python Basics", capacity=2, mentor=liskov)
    data_course = Course.from_text("DS-201,Data Structures,10")
    web_course = Course("WEB-150", "Web Foundations", capacity=5)
    data_course.set_mentor(knuth)

    catalogue = [python_course, data_course, web_course]
    for course in catalogue:
        print(course.describe())

    print("\nEnrolling students:")
    first = Enrollment(ada, python_course)
    second = Enrollment(alan, python_course)
    third = Enrollment(grace, data_course)
    for enrollment in [first, second, third]:
        print("  ", enrollment)

    print("\nThe course is now full, so the next student is turned away:")
    try:
        Enrollment(grace, python_course)
    except ValueError as error:
        print("  ", error)

    print("\nAda finishes the course:")
    letter = first.complete(88)
    print("   grade:", letter, "| status:", first.status)
    print("   Ada grades:", ada.get_grades())

    print("\nAlan drops the course, which frees his seat:")
    second.drop("timetable clash")
    print("  ", second.describe())
    print("   seats left in PY-101:", python_course.seats_left())

    print("\nGrace takes the free seat:")
    fourth = Enrollment(grace, python_course)
    print("  ", fourth)
    print("   PY-101 students now:", python_course.student_names())

    print("\nClass method enroll_in_many() puts Alan on two courses at once:")
    batch = Enrollment.enroll_in_many(alan, [web_course, data_course])
    for enrollment in batch:
        print("  ", enrollment)

    # ------------------------------------------------------------------
    title("7. SUMMARY REPORT")
    # ------------------------------------------------------------------
    lines = []
    lines.append("COURSE MANAGEMENT SYSTEM - SUMMARY")
    lines.append("")
    lines.append("People:")
    for person in people:
        lines.append("  " + person.show_profile())
    lines.append("")
    lines.append("Courses:")
    for course in catalogue:
        lines.append("  " + course.describe())
    lines.append("")
    lines.append("Report card:")
    lines.append(ada.report_card())
    lines.append("")
    lines.append("Totals: users=" + str(User.count())
                 + ", courses=" + str(Course.total_courses)
                 + ", enrollments=" + str(Enrollment.total_enrollments))

    report = "\n".join(lines)
    print(report)

    with open(REPORT_FILE, "w", encoding="utf-8") as report_file:
        report_file.write(report + "\n")
    print()
    print("Report also saved to", REPORT_FILE)
    print("That file is listed in .gitignore, so Git does not track it.")


if __name__ == "__main__":
    main()
