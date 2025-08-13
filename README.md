# shortgit

`shortgit` is a tiny, opinionated CLI for bootstrapping Git/GitHub repos and pushing changes, optimized for data-heavy projects.

* Always creates a **GitHub** remote via `gh`
* Defaults to **public** visibility
* Writes a data-friendly **.gitignore** (`**/data/**`, `*.parquet`, `*.dta`, `*.pkl`, `*.xlsx`, etc.)
* Separation of concerns: `init` never pushes; use `push` to stage→commit→push

---

## Prerequisites

* `git` installed and on `PATH`
* GitHub CLI `gh` installed and authenticated: `gh auth login`
* Python 3.9+

---

## Installation

```bash
pip install .
```

(Optional for development):

```bash
pip install -e .
```

---

## Quick Start

```bash
# create a new repo in a new folder (public by default)
shortgit init myproject

# or, initialize the current directory
shortgit init . --name myproject

# do work, then push
shortgit push "initial structure"
```

---

## CLI Reference

> The full command reference is maintained in `CLI_REFERENCE.md`. Depending on your documentation tooling, you can include it directly below. We add common include directives so most toolchains will work out of the box; GitHub will simply show a link.

**Direct link:** [CLI\_REFERENCE.md](CLI_REFERENCE.md)

### Include (choose one supported by your docs tool)

<!-- MyST / Sphinx / MkDocs (myst-parser) -->

```{include} CLI_REFERENCE.md
```

<!-- MkDocs-Macros or markdown-include plugin (if enabled) -->

<!-- @include: ./CLI_REFERENCE.md -->

<!-- GitHub Markdown does not support includes; the link above will suffice on GitHub. -->

---

## Notes

* `shortgit init` creates `.gitignore` only if one does not already exist. You can customize it afterward.
* `shortgit push` can be run repeatedly and will set upstream on the first push by default.

---

## License

MIT
