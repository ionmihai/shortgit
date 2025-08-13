# shortgit

`shortgit` is a simple CLI wrapper for quickly creating a GitHub repository, making an initial commit, and pushing changes without having to remember a long sequence of Git commands.

It is designed for users who **always use GitHub remotes** and want sensible defaults like a `.gitignore` that automatically excludes common data directories and file formats.

---

## Features

- **Create new GitHub repos in one command** using `gh repo create`
- **Auto-generate `.gitignore`** to ignore:
  - Any folder named `data`
  - Common data files: `.parquet`, `.pkl`, `.dta`, `.sas7bdat`, `.csv`, `.xls`, `.xlsx`, `.feather`
- **Automatic first commit** in `init`
- **Separate `push` command** for staging, committing, and pushing changes
- Works for both first-time pushes and subsequent updates

---

## Prerequisites

Before using `shortgit`, you must have:

1. **Git** installed and available in your `PATH`
2. **GitHub CLI (`gh`)** installed and authenticated:
   ```bash
   gh auth login
   ```
3. **Python 3.8+**
4. (Optional) A GitHub account with default visibility settings configured

---

## Installation

From source:

```bash
pip install .
```

---

## Quick Start

### Initialize a new GitHub repo

```bash
shortgit init "my-project-name"
```

This will:
- Create a new local git repo
- Add a `.gitignore` with defaults
- Stage and commit all files
- Create a GitHub repo with the same name as your local folder
- **No push is done at this stage**

---

### Push changes

```bash
shortgit push "my commit message"
```

This will:
- Stage all changes
- Commit with your message
- Push to the remote `origin` branch

---

## Example workflow

```bash
mkdir myproject && cd myproject
touch README.md
shortgit init "myproject"
# ...make changes...
shortgit push "add initial code"
```

---

## Commands

### `init`

**Usage:**
```bash
shortgit init [PROJECT_PATH] [--private]
```

**Arguments:**
- `PROJECT_PATH`: Path to the project (defaults to current dir)

**Options:**
- `--private`: Make repo private (default is public)

---

### `push`

**Usage:**
```bash
shortgit push "commit message"
```

Stages all changes, commits, and pushes.

---

## Notes

- This tool **always** creates a GitHub remote (`origin`).
- You can run `shortgit push` as often as needed after `init`.
- Designed for projects where large binary/data files should be excluded from git by default.

