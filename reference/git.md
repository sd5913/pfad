# Git, the six commands you use

Git is a folder that remembers. It does nothing until you tell it to, and what it
remembers is not "the latest version" but *every* version, each with a note saying
what changed and whose name is on it. That is the whole idea, and six commands get
you all of it.

You will use these six every week for the rest of the semester. Everything else in
git — and there is a lot — is for later.

## What the words mean

| Word | What it actually is |
|---|---|
| **repository** | A folder git is watching. There is a `.git/` inside it; that is the difference. |
| **working tree** | The files as they are on disk right now — what you see in VS Code. |
| **staged** | Marked to go into the next commit. `git add` puts a change here; nothing else does. |
| **commit** | A snapshot of the staged changes, with a message and your name. Permanent. |
| **remote** | A copy of the repository somewhere else, usually GitHub. Yours is called `origin`. |
| **push** / **pull** | Send your commits to the remote / bring the remote's commits down. |
| **clone** | Download a whole repository, entire history included, to your machine. |
| **branch** | One line of history. Two branches are two versions of the same folder. |

## The six

```bash
git clone https://github.com/sd5913/pfad    # once, to get a repository onto this machine
cd pfad

git status                                  # what has changed since the last commit?
git add .                                   # stage everything that changed
git commit -m "Say what you did"            # snapshot the staged changes, with a note
git push                                    # send the snapshots to GitHub
git pull                                    # bring GitHub's down
```

Two things about that list.

**The `clone` shown above, `push` and `pull` contact GitHub.** `status`, `add`
and `commit` work locally, so you can commit forty times on a plane. Until you
push, GitHub has not seen those commits. Other commands, such as `fetch`, also
contact a remote; a remote can be local rather than on the internet.

**`status` is free.** Run it before and after every other command until you can
predict what it will say. It is the cheapest debugging in the course.

```
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	PROCESS.md

nothing added to commit but untracked files present
```

`git status --short` gives you the same thing in one line per file: `??` means git
has never seen this file, `M` means changed, `A` means a new file you have staged.

### add, then commit, then push — three steps, not one

This trips everyone once. `add` stages, `commit` snapshots, `push` sends. After
`commit` your work is safe on your machine and invisible to everybody else.

In VS Code's **Source Control** panel (`Ctrl+Shift+G`) the three are the `+` next
to a file, the message box and the tick, and **Sync Changes**. Same commands with
buttons on them — which is why you type them once first. After **Commit** the box
empties and nothing has left your computer; the button changes to **Sync Changes**
and you have to press it.

### What a commit message is for

It is a note to the you of next month, and to the person marking your repo. It
should say **what changed and why**, not that something changed.

```
cut the photography section to one paragraph     ← good
fix Nake link                                     ← good
first draft of the argument about materials       ← good
Update README.md                                  ← says nothing
update                                            ← says nothing
```

The check counts these. If most of your messages are `update` you get a note
saying so, because a history of `update` is not a history.

## Looking at what you have

```bash
git log --oneline      # the history, one commit per line, newest first
git ls-files           # every file git actually has
git remote -v          # where origin points
git branch -a          # every branch this clone knows about
```

`git log --oneline` prints a short id and the message:

```
f897924 reference/files.md: folders, paths and the names that start with a dot
8972675 assignment 2: start from sd5913/assignment-2-template
1513cb3 week03: drift integrates in sub-steps so the water follows the field
```

**`git ls-files` is the one people forget, and it answers the most common
question in this course: "why is my file not on GitHub?"** A file that is on disk
but not in that list is not in the repository, however many times you push. Either
you never ran `git add` on it, or `.gitignore` is excluding it. `git ls-files .github`
is how you check that the workflow really got committed.

`git remote -v` prints the address git pushes to. **`origin`** is just the default
name for "the remote I cloned from" — there is nothing magic about the word, it is
a nickname for a URL:

```
origin	https://github.com/sd5913/pfad.git (fetch)
origin	https://github.com/sd5913/pfad.git (push)
```

## Branches, and why this repo has two

```bash
git branch -a        # every branch
git switch 2025      # last year's course
ls                   # different files entirely
git switch 2026      # back to the present
```

Do that and watch the files on disk change under you, then change back. You did
not download anything the second time: `git clone` brought the whole repository,
both branches, the first time.

That is what a branch is. Not a folder, not a copy — one line of history that
happens to disagree with another line of history. `2026` and `2025` share a remote
and a clone and nothing else. In the group project you will use them properly, so
that three people can change the same code without standing on each other.

## `.gitignore`

A plain text list of names git will never commit. It is why `.venv/` and
`__pycache__/` do not end up in your repository, and it is the difference between
a repo somebody can read and a repo with four hundred files in it.

What it is, why the name starts with a dot, and what belongs in it:
[`files.md`](files.md).

## Why the check wants commits on more than one day

Run the check inside your assignment repo and one of the lines is about history:

```
  FAIL  4 commits, all on one day — spread the work over more than one sitting
  ok    7 commits over 3 days
```

Three commits over two days is the bar, and it is deliberately low. It is not a
word count in disguise and it is not there to make you perform effort. It is there
because **working in increments you can name is the habit that makes the group
project survivable**, and an essay is a cheap place to build it. A repository with
one commit called `initial commit` is indistinguishable from a paste, and it is
also a repository you cannot go back in.

You cannot clear this line on the day. Commit again tomorrow, from home, and it
clears itself.

## The Actions tab, and one exact address

Put a file at `.github/workflows/check.yml` in your repo and GitHub runs the check
on its own machine every time you push, and puts a green tick or a red cross next
to your latest commit. The **Actions** tab shows each run and the same checklist
you saw in the terminal.

```bash
mkdir -p .github/workflows
curl -fsSL https://raw.githubusercontent.com/sd5913/pfad/2026/assignments/check.yml -o .github/workflows/check.yml
git add .github
git commit -m "Add the assignment check"
git push
```

**On Windows PowerShell write `curl.exe`, not `curl`.** The PowerShell that ships
with Windows has its own command called `curl` which is not curl, takes different
arguments, and fails on that line. The `.exe` is not decoration; it tells
PowerShell you mean the real program.

**The directory must be `.github/workflows/`.** Our example uses `check.yml`,
but GitHub accepts other filenames with a `.yml` or `.yaml` extension there,
including `Check.yml`. The leading dot and plural `workflows` matter. The
workflow also needs an `on:` trigger matching the event you expect; merely
placing any YAML file there does not make it run on every push. See
[GitHub’s workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

The folder starts with a dot, so Finder and Explorer hide it. `git status` does
not, and `git ls-files .github` tells you whether git really has it.

> You can also skip the terminal: open `assignments/check.yml` in your `pfad`
> clone, copy all of it, and paste it into a new file at that exact path.

## Windows, where it differs

- **New terminal after installing anything.** An installer changes your `PATH`;
  a window that was already open never notices. This is the single most common
  reason `'git' is not recognized` appears after a successful install.
- **`curl.exe`, not `curl`**, in PowerShell. As above.
- **Paths use `\`** — `..\pfad\week01\first-repo\sketch.py`. Git itself always
  writes `/`, in every message and in `.gitignore`, on every platform.
- **`pwd` works in PowerShell** as an alias for `Get-Location`; use either to
  display your current folder. `cd` is an alias for `Set-Location`, which changes
  folders, not the equivalent of `pwd`. `Get-ChildItem -Force` (or `ls -Force`)
  includes hidden entries, like `ls -a` in a Unix shell.

## When it goes wrong

Every git error you are likely to meet, with what to do about it, is in
[`errors.md`](errors.md).
