# shortgit — CLI Reference (init & push)

This document lists **all** arguments and options for `shortgit init` and `shortgit push`, with defaults, behaviors, and examples.

> Prereqs: `git` and `gh` must be on PATH, and `gh auth login` should be completed.

---

## `shortgit init`

Initialize a new git repository in a directory, make the initial commit, and create a GitHub remote (`origin`) using the GitHub CLI. **No pushing is done here.**

### Usage

```bash
shortgit init [PATH] [OPTIONS]
```

### Positional Arguments

* **`PATH`** *(default: `.`)* — Directory to initialize. If it does not exist, it will be created. If it already contains a `.git` directory, use `--force` to reinitialize.

### Options

* **`--name, -n <STR>`** *(default: directory name)*
  Name of the GitHub repository to create. If omitted, the last path component is used.

* **`--org <STR>`** *(default: your GitHub user)*
  GitHub owner/organization to create the repo under.

* **`--description, -d <STR>`** *(optional)*
  Description for the GitHub repository.

* **`--visibility, -v <public|private|internal>`** *(default: `public`)*
  Visibility of the GitHub repository.

* **`--branch, -b <STR>`** *(default: `main`)*
  Default branch name to create locally.

* **`--message, -m <STR>`** *(default: `initial commit`)*
  Commit message to use for the first commit.

* **`--gitignore / --no-gitignore`** *(default: `--gitignore`)*
  Whether to create a `.gitignore` if one does not exist.

* **`--ignore-data-exts / --no-ignore-data-exts`** *(default: `--ignore-data-exts`)*
  If enabled, the generated `.gitignore` includes patterns to ignore any `data/` directory at any depth and common data formats: `*.parquet, *.pq, *.feather, *.pkl, *.pickle, *.csv, *.tsv, *.txt, *.jsonl, *.json, *.dta, *.sas7bdat, *.xpt, *.sav, *.zsav, *.rds, *.RData, *.xlsx, *.xls, *.xlsm, *.xlsb, *.h5, *.hdf5, *.npz, *.npy`.

* **`--force`** *(default: disabled)*
  Allow reinitializing a directory that already contains a `.git` folder.

### Behavior

1. Ensures `git` and `gh` are available; requires `gh` to be authenticated.
2. Creates the directory if it doesn’t exist.
3. Optionally writes a `.gitignore` (with the data-friendly defaults).
4. Initializes a git repository on the chosen branch.
5. Stages all files and creates the first commit (or an empty commit if there’s nothing to commit).
6. Creates a GitHub repository via `gh repo create`, sets it as `origin`. **Does not push.**

### Examples

```bash
# Init in current directory; repo name defaults to folder name; public repo
shortgit init

# Init in current directory but use a custom repo name
shortgit init . --name shortgit

# Create a new folder and init there in one go
shortgit init myproject

# Create under an organization, private visibility, custom description
shortgit init . --org my-org --visibility private \
  --description "Data tooling"

# Reinitialize an existing working tree (will commit again and rewire origin)
shortgit init . --force
```

---

## `shortgit push`

Stage, commit, and push changes to the remote `origin`. Handles the very first push (sets upstream) and all subsequent pushes.

### Usage

```bash
shortgit push "commit message" [OPTIONS]
```

### Positional Arguments

* **`commit message`** *(required)* — Message for the commit created by this push.

### Options

* **`--path, -p <PATH>`** *(default: `.`)*
  Working directory of the git repository.

* **`--branch, -b <STR>`** *(default: current branch)*
  Branch to push. If omitted, the current branch is detected.

* **`--allow-empty`** *(default: disabled)*
  If set, creates an empty commit even if there are no staged changes.

* **`--upstream / --no-upstream`** *(default: `--upstream`)*
  On the first push, uses `git push -u origin <branch>` to set upstream. If upstream already exists, it falls back to a normal push.

### Behavior

1. Ensures the working directory is a git repository and that `origin` exists.
2. Stages all changes (`git add -A`).
3. Creates a commit with the given message (or an empty commit if `--allow-empty` is set; otherwise skips committing if nothing changed).
4. Pushes to `origin` on the selected branch. If `--upstream` is enabled, it sets the upstream on first push.

### Examples

```bash
# Normal push with a commit message
shortgit push "Implement feature X"

# Push a specific branch
shortgit push "Update" --branch dev

# Push even when there are no changes (creates an empty commit)
shortgit push "Tag release" --allow-empty

# Push without modifying upstream settings
shortgit push "Docs" --no-upstream
```

---

## Exit codes & errors

* Any failure from underlying `git` or `gh` commands raises a runtime error with captured stdout/stderr.
* Missing tools (`git`, `gh`), unauthenticated `gh`, nonexistent repository path, or missing `origin` (for `push`) are reported clearly.

---

## Tips

* If you prefer to always work in the current directory, use `shortgit init .` and optionally `--name` to set a different GitHub repo name.
* The generated `.gitignore` is only created if absent; you can safely customize it after initialization.
* You can run `shortgit push` repeatedly as your normal push workflow.
