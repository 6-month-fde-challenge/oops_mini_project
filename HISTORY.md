# Git history of this project

Everything below is real terminal output, copied straight from this repository
after the last merge. It is committed so the branch structure, the merges and
the pull requests can be seen without leaving the files. The same graph is
printed in the Git workflow section of the README.

## Branch structure and commit history

```console
$ git log --graph --oneline --all --decorate
*   a35dd81 (HEAD -> main, origin/main, origin/HEAD) Merge pull request #3 from 6-month-fde-challenge/docs/commit-graph
|\  
| * 94986e4 (origin/docs/commit-graph, docs/commit-graph) docs: print the commit graph inside the README
|/  
*   0ed5f7e Merge pull request #2 from 6-month-fde-challenge/add-more-summary
|\  
| * 2138d60 (origin/add-more-summary, add-more-summary) added a new feature
|/  
* 0b490bb changes made
* 5aef2a2 docs: add HISTORY.md with the captured git output
*   ee4d2c4 Merge branch docs/readme into main
|\  
| * d12096c (origin/docs/readme, docs/readme) docs: add full README
|/  
*   5a34e82 Merge branch feature/demo-app into main
|\  
| * d266175 (origin/feature/demo-app, feature/demo-app) feat: add main.py demo program
|/  
*   835fe9a Merge pull request #1 from 6-month-fde-challenge/feature/course-and-enrollment
|\  
| * f56ca9c (origin/feature/course-and-enrollment, feature/course-and-enrollment) feat: add Enrollment class linking a student to a course
| * 6225c4e feat: add Course class with private student list
|/  
*   e046cbd Merge branch feature/user-classes into main
|\  
| * dd8f1e0 (origin/feature/user-classes, feature/user-classes) feat: add Student and Mentor classes that inherit from User
| * 7b7c857 feat: add abstract User base class
|/  
* 2d485df chore: set up repository with .gitignore
```

## Branches, local and on GitHub

```console
$ git branch -a
  add-more-summary
  docs/commit-graph
  docs/readme
  feature/course-and-enrollment
  feature/demo-app
  feature/user-classes
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/add-more-summary
  remotes/origin/docs/commit-graph
  remotes/origin/docs/readme
  remotes/origin/feature/course-and-enrollment
  remotes/origin/feature/demo-app
  remotes/origin/feature/user-classes
  remotes/origin/main
```

## Pull requests

```console
$ gh pr list --state all
3	docs: print the commit graph inside the README	docs/commit-graph	MERGED	2026-09-22T18:07:27Z
2	added a new feature	add-more-summary	MERGED	2026-09-22T15:49:39Z
1	feat: add Course and Enrollment classes	feature/course-and-enrollment	MERGED	2026-09-22T12:06:40Z
```

## The .gitignore working

After running `python main.py`, the folder holds `__pycache__/` and
`report.local.txt`. Git does not see either of them, and `git check-ignore -v`
names the rule and the line number that hid each one:

```console
$ ls
HISTORY.md
README.md
__pycache__
course.py
enrollment.py
main.py
mentor.py
report.local.txt
student.py
task.txt
user.py

$ git status --short

$ git check-ignore -v report.local.txt __pycache__ task.txt
.gitignore:10:*.local.txt	report.local.txt
.gitignore:2:__pycache__/	__pycache__
.gitignore:13:task.txt	task.txt
```
