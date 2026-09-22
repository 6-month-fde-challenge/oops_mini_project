# Course Management System

A small Course Management System written in Python to practise object oriented
programming. It models the four things a real training institute deals with -
**people**, **courses** and the **enrollments** that join them - and it was
built through a normal Git workflow: feature branches, meaningful commits,
merges and a pull request.

The whole project is plain Python. There is nothing to install and no
third party library to download.

- **Repository:** https://github.com/6-month-fde-challenge/oops_mini_project
- **Pull request:** https://github.com/6-month-fde-challenge/oops_mini_project/pull/1
- Module 04 of the 6 month FDE challenge.

---

## Table of contents

1. [What it does](#what-it-does)
2. [OOP concepts demonstrated](#oop-concepts-demonstrated)
3. [Architecture and classes](#architecture-and-classes)
4. [Project structure](#project-structure)
5. [Installation](#installation)
6. [How to run it](#how-to-run-it)
7. [Features](#features)
8. [Usage examples](#usage-examples)
9. [The .gitignore file](#the-gitignore-file)
10. [Git workflow](#git-workflow)

---

## What it does

The system keeps track of:

- **Students**, who join courses and collect grades,
- **Mentors**, who teach courses and are paid by the hour,
- **Courses**, which have a code, a title, a mentor and a limited number of seats,
- **Enrollments**, which record that a student joined a course, and what happened next.

The rules it enforces are the ones a real system would need:

- a course cannot take more students than it has seats,
- a student cannot join the same course twice,
- a mentor cannot teach more than three courses,
- a grade must be between 0 and 100,
- an email address must look like a real one,
- an enrollment cannot be completed or dropped twice.

---

## OOP concepts demonstrated

Every concept the project set out to cover is used for a real purpose, not
just mentioned:

| Concept | Where it is used | Example |
|---|---|---|
| **Abstraction** | `User` inherits from `ABC` and declares `role()` and `describe()` as abstract, so `User` itself can never be created | `user.py` |
| **Inheritance** | `Student` and `Mentor` both extend `User` and reuse its name, email, ID and profile handling through `super().__init__()` | `student.py`, `mentor.py` |
| **Encapsulation** | Private attributes (`__email`, `__grades`, `__hourly_rate`, `__students`, `__status`) are reachable only through properties and methods that validate first | all files |
| **Polymorphism** | `role()` and `describe()` are called on a list of mixed `Student` and `Mentor` objects, and each class answers in its own way | `main.py`, section 4 |
| **Instance methods** | `add_grade()`, `calculate_fee()`, `add_student()`, `complete()`, `drop()` - they work on one object and its own data | all files |
| **`@staticmethod`** | `User.is_valid_email()`, `Student.grade_letter()`, `Mentor.is_valid_rate()`, `Course.is_valid_code()`, `Enrollment.make_reference()` - helpers that need no object | all files |
| **`@classmethod`** | `Student.from_dict()`, `Mentor.senior()`, `Course.from_text()`, `Enrollment.enroll_in_many()`, `User.count()` - second ways to build objects, and class level counters | all files |

---

## Architecture and classes

```
                    +---------------------------+
                    |      User  (abstract)     |
                    |---------------------------|
                    |  name, _user_id, __email  |
                    |---------------------------|
                    |  show_profile()           |
                    |  is_valid_email()  static |
                    |  count()           class  |
                    |  role()            abstract
                    |  describe()        abstract
                    +---------------------------+
                          ^                ^
                          |  inherits      |  inherits
              +-----------+                +-----------+
              |                                        |
   +----------------------+                 +----------------------+
   |       Student        |                 |        Mentor        |
   |----------------------|                 |----------------------|
   | program, __grades    |                 | subject, courses,    |
   |                      |                 | __hourly_rate        |
   |----------------------|                 |----------------------|
   | add_grade()          |                 | assign_course()      |
   | get_grades()         |                 | calculate_fee()      |
   | average()            |                 | is_available()       |
   | report_card()        |                 | is_valid_rate() stat |
   | grade_letter() stat  |                 | senior()       class |
   | from_dict()    class |                 |                      |
   +----------------------+                 +----------------------+
              |                                        |
              |  enrolled through                      |  teaches
              |                                        v
              |                            +----------------------+
              |                            |        Course        |
              |                            |----------------------|
              |                            | code, title, mentor, |
              |                            | __capacity,          |
              |                            | __students           |
              |                            |----------------------|
              |                            | add_student()        |
              |                            | remove_student()     |
              |                            | seats_left()         |
              |                            | is_valid_code() stat |
              |                            | from_text()    class |
              |                            +----------------------+
              |                                        ^
              |                                        |
              |        +----------------------+        |
              +------->|      Enrollment      |<-------+
                       |----------------------|
                       | student, course,     |
                       | date_joined,         |
                       | reference,           |
                       | __status, __score    |
                       |----------------------|
                       | complete()           |
                       | drop()               |
                       | make_reference() stat|
                       | enroll_in_many() cls |
                       +----------------------+
```

### The five classes

| Class | File | Responsibility |
|---|---|---|
| `User` | `user.py` | Abstract base class. Holds the name, the ID and the private email, and forces every subclass to answer `role()` and `describe()`. |
| `Student` | `student.py` | A learner. Keeps a private dictionary of grades, works out the average and prints a report card. |
| `Mentor` | `mentor.py` | A teacher. Keeps a private hourly rate, tracks the courses taught and refuses more than three. |
| `Course` | `course.py` | One subject in the catalogue. Keeps a private list of students and a seat limit. |
| `Enrollment` | `enrollment.py` | Joins one student to one course, and records the status and the final score. |

### How they work together

- A `Course` may have one `Mentor`. Giving a course a mentor also tells the
  mentor about the course, so both sides agree.
- An `Enrollment` asks the `Course` for a seat **before** it is created. If the
  course is full, nothing is created at all.
- `Enrollment.complete(score)` saves the grade on the `Student`; the student is
  the only place grades live.
- `Enrollment.drop()` gives the seat back to the `Course`, so another student
  can take it.

---

## Project structure

```
oops_mini_project/
├── user.py           # abstract User base class
├── student.py        # Student(User)
├── mentor.py         # Mentor(User)
├── course.py         # Course
├── enrollment.py     # Enrollment
├── main.py           # demo program - run this one
├── .gitignore        # files Git must not track
└── README.md         # this file
```

---

## Installation

You need **Python 3.8 or newer**. Nothing else - the project uses only the
standard library.

```bash
# 1. clone the repository
git clone https://github.com/6-month-fde-challenge/oops_mini_project.git

# 2. go into the folder
cd oops_mini_project

# 3. check your Python version
python --version
```

Optionally, work inside a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS or Linux
source .venv/bin/activate
```

There is no `pip install` step, because there are no dependencies.

---

## How to run it

```bash
python main.py
```

The program prints seven sections, one for each idea, using real output from
the classes. It also writes a summary to `report.local.txt`, which `.gitignore`
keeps out of the repository.

---

## Features

- **Five classes** covering people, courses and enrollments.
- **Validation everywhere it matters**: email format, grade range, hourly rate
  band, course code format, seat limits and course limits per mentor.
- **Private data** that outside code cannot corrupt. `get_grades()` and
  `student_names()` hand back copies, so editing the copy changes nothing.
- **Automatic IDs**: students are numbered `STU-001`, `STU-002`, mentors
  `MEN-001`, `MEN-002`, each class counting its own.
- **Enrollment lifecycle**: active, completed or dropped, with the seat
  returned to the course when a student drops out.
- **Two ways to build most objects**: the normal constructor, or a
  `@classmethod` such as `Student.from_dict()` and `Course.from_text()`.
- **A report card** per student and a summary report for the whole system.
- **A runnable demo** that proves each rule by trying to break it and printing
  the error that comes back.

---

## Usage examples

### Creating people

```python
from student import Student
from mentor import Mentor

ada = Student("Ada Lovelace", "ada@example.com", "Computer Science")
liskov = Mentor.senior("Barbara Liskov", "barbara@example.com", "OOP")

print(ada.show_profile())
print(liskov.show_profile())
print("Total users:", Student.count())
```

```
[Student] STU-001 | Ada Lovelace | ada@example.com
[Mentor] MEN-001 | Barbara Liskov | barbara@example.com
Total users: 2
```

### Abstraction: the base class cannot be created

```python
from user import User

User("Nobody", "nobody@example.com")
```

```
TypeError: Can't instantiate abstract class User without an implementation
for abstract methods 'describe', 'role'
```

### Encapsulation: private data stays private

```python
ada.add_grade("PY-101", 88)

copy = ada.get_grades()      # get_grades() returns a COPY
copy["FAKE-999"] = 100       # so editing it changes nothing real

print(copy)
print(ada.get_grades())

ada.email = "broken-email"   # refused by the property setter
```

```
{'PY-101': 88, 'FAKE-999': 100}
{'PY-101': 88}
ValueError: Invalid email address: broken-email
```

### Polymorphism: one loop, different answers

```python
for person in [ada, liskov]:
    print(person.role(), "->", person.describe())
```

```
Student -> Ada Lovelace studies Computer Science and has completed 1 course(s).
Mentor -> Barbara Liskov teaches OOP and handles 1 of 3 courses.
```

### Courses and enrollments

```python
from course import Course
from enrollment import Enrollment

python_course = Course("PY-101", "Python Basics", capacity=2, mentor=liskov)
data_course = Course.from_text("DS-201,Data Structures,10")

enrollment = Enrollment(ada, python_course)
print(enrollment)
print("Seats left:", python_course.seats_left())

print("Grade:", enrollment.complete(88))
print(ada.get_grades())
```

```
Ada Lovelace -> PY-101 (active)
Seats left: 1
Grade: A
{'PY-101': 88}
```

### The rules being enforced

```python
Enrollment(grace, python_course)   # when the course is already full
```

```
ValueError: PY-101 is full (2 seats)
```

```python
enrollment.complete(90)            # when it is already completed
```

```
ValueError: ENR-STU001-PY101 is already completed
```

---

## The .gitignore file

`.gitignore` lists the files Git must never track. The rule used here: anything
**generated**, **machine specific** or **private** stays out of the repository,
and only hand written source and documentation go in.

```gitignore
# Python cache files created every time the program runs
__pycache__/
*.pyc

# Virtual environment
.venv/
venv/

# Files the demo writes at runtime (not source code)
*.local.txt

# The assignment brief and personal notes - kept locally, not published
task.txt
notes.txt

# Editor / OS files
.vscode/
.idea/
.DS_Store
Thumbs.db
```

You can see it working. After running `python main.py`, the folder contains
`__pycache__/` and `report.local.txt`, but `git status` stays clean, and
`git check-ignore` explains exactly which rule hid each one:

```console
$ git status --short
$ git check-ignore -v report.local.txt __pycache__
.gitignore:10:*.local.txt       report.local.txt
.gitignore:2:__pycache__/       __pycache__
```

---

## Git workflow

The repository was built from scratch on the command line. Nothing was created
through the GitHub website.

### 1. Starting the repository and connecting it to GitHub

```bash
git init -b main
gh repo create 6-month-fde-challenge/oops_mini_project --public --description "..."
git remote add origin https://github.com/6-month-fde-challenge/oops_mini_project.git
git remote -v

git add .gitignore README.md
git commit -m "chore: set up repository with .gitignore"
git push -u origin main
```

### 2. Branches

Each piece of work was built on its own branch and merged back into `main`.

| Branch | What it added | How it reached `main` |
|---|---|---|
| `feature/user-classes` | `user.py`, `student.py`, `mentor.py` | local merge with `--no-ff` |
| `feature/course-and-enrollment` | `course.py`, `enrollment.py` | **pull request #1**, merged on GitHub |
| `feature/demo-app` | `main.py` | local merge with `--no-ff` |
| `docs/readme` | this `README.md` | local merge with `--no-ff` |

The pattern for a branch that was merged locally:

```bash
git checkout -b feature/user-classes
# ... write the code ...
git add user.py
git commit -m "feat: add abstract User base class"
git push -u origin feature/user-classes

git checkout main
git merge --no-ff feature/user-classes -m "Merge branch feature/user-classes into main"
git push origin main
```

`--no-ff` forces a merge commit even when a fast forward would be possible, so
the branch stays visible in the history instead of disappearing into a straight
line.

### 3. The pull request

`feature/course-and-enrollment` went through a real pull request instead of a
local merge:

```bash
git push -u origin feature/course-and-enrollment
gh pr create --base main --head feature/course-and-enrollment \
    --title "feat: add Course and Enrollment classes" --body-file pr-body.md
gh pr review 1 --comment --body "Reviewed both classes and ran them together locally..."
gh pr merge 1 --merge
git checkout main
git pull origin main
```

**Pull request #1:** https://github.com/6-month-fde-challenge/oops_mini_project/pull/1
(merged)

The review is recorded as a review **comment** rather than a green approval,
because GitHub does not let you approve your own pull request and this project
was built by one person on one account.

### 4. The resulting history

```console
$ git log --graph --oneline --all
```

The full graph is printed in [HISTORY.md](HISTORY.md), which is captured
straight from the terminal after the last merge.

### Commands used in this project

| Command | Why it was needed |
|---|---|
| `git init -b main` | start the repository with `main` as the default branch |
| `git remote add origin <url>` | connect the local repository to GitHub |
| `git checkout -b <branch>` | start a feature branch |
| `git add` / `git commit -m` | stage and save a piece of work |
| `git push -u origin <branch>` | publish a branch and track it |
| `git merge --no-ff <branch>` | merge a branch and keep it visible in the history |
| `git pull origin main` | bring the pull request merge back down to the local copy |
| `git log --graph --oneline --all` | see the branch structure |
| `git status` / `git check-ignore -v` | confirm that ignored files really are ignored |
| `gh repo create` | create the GitHub repository from the terminal |
| `gh pr create` / `gh pr review` / `gh pr merge` | open, review and merge the pull request |

---

## Author

Veerandra Kumar - module 04 of the 6 month FDE challenge.
