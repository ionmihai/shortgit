# src/shortgit/cli.py
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from enum import Enum
import typer

HELP_TEXT = (
    "shortgit — initialize and push Git/GitHub repositories.\n\n"
    "\b\n"  # <— tells Click/Typer: keep the following block as-is
    "Commands:\n"
    "  init    Initialize a new GitHub repository with sensible defaults\n"
    "  push    Stage, commit, and push all changes to the remote\n"
    "\n"
    "Run 'shortgit init --help' or 'shortgit push --help' for command-specific options.\n"
)

app = typer.Typer(add_completion=False, help=HELP_TEXT, context_settings={"max_content_width": None})

class Visibility(str, Enum):
    public = "public"
    private = "private"
    internal = "internal"

def run(cmd, cwd: Optional[Path]=None) -> str:
    r = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}")
    return r.stdout.strip()

def ensure_tool(name: str, url: str):
    if shutil.which(name) is None:
        raise RuntimeError(f"'{name}' not found on PATH. Install it: {url}")

def make_gitignore(repo_dir: Path, also_ignore_data_exts: bool=True, extra_patterns: Optional[list[str]]=None):
    gi = repo_dir / ".gitignore"
    if gi.exists(): return
    lines = [
        "# Python",
        "__pycache__/", "*.py[cod]", "*.egg-info/", ".pytest_cache/", ".mypy_cache/", ".ruff_cache/",
        ".venv/", "venv/","*.env","",".env.*","*.env",
        "# Build artifacts",
        "build/", "dist/",
        "# IDE",
        ".idea/", ".vscode/",
        "# Data directories",
        "**/data/**",
        "# Common data files",
        "*.parquet",
    ]
    if extra_patterns: lines += extra_patterns
    gi.write_text("\n".join(lines) + "\n", encoding="utf-8")

def git_init(repo_dir: Path, branch: str):
    try:
        run(["git","init","-b",branch], cwd=repo_dir)
    except RuntimeError:
        run(["git","init"], cwd=repo_dir)
        run(["git","symbolic-ref","HEAD",f"refs/heads/{branch}"], cwd=repo_dir)

def current_branch(repo_dir: Path) -> str:
    return run(["git","rev-parse","--abbrev-ref","HEAD"], cwd=repo_dir)

@app.command()
def init(
    path: Path = typer.Argument(Path("."), help="Directory to initialize"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="GitHub repo name (default: directory name)"),
    org: Optional[str] = typer.Option(None, "--org", help="GitHub org/owner; default: your user"),
    description: Optional[str] = typer.Option(None, "--description", "-d"),
    visibility: Visibility = typer.Option(Visibility.public, "--visibility", "-v"),
    default_branch: str = typer.Option("main","--branch","-b"),
    commit_message: str = typer.Option("initial commit","--message","-m"),
    create_gitignore: bool = typer.Option(True, "--gitignore/--no-gitignore"),
    ignore_data_exts: bool = typer.Option(True, "--ignore-data-exts/--no-ignore-data-exts"),
    force_reinit: bool = typer.Option(False, "--force", help="Reinitialize if .git exists"),
):
    ensure_tool("git","https://git-scm.com/downloads")
    ensure_tool("gh","https://cli.github.com/")
    path.mkdir(parents=True, exist_ok=True)

    if (path/".git").exists() and not force_reinit:
        raise RuntimeError(f"{path} already has a .git directory. Use --force to re-init.")

    if create_gitignore:
        make_gitignore(path, also_ignore_data_exts=ignore_data_exts)

    git_init(path, default_branch)
    run(["git","add","-A"], cwd=path)
    try:
        status = run(["git","status","--porcelain"], cwd=path)
        if status.strip():
            run(["git","commit","-m",commit_message], cwd=path)
        else:
            run(["git","commit","--allow-empty","-m",commit_message], cwd=path)
    except RuntimeError as e:
        raise RuntimeError(f"git commit failed: {e}") from e

    try:
        run(["gh","auth","status"])
    except RuntimeError as e:
        raise RuntimeError("`gh` is not authenticated. Run `gh auth login` first.") from e

    repo_name = name or path.name
    args = ["gh","repo","create",repo_name,"--source",str(path),"--remote","origin", f"--{visibility}"]
    if description: args += ["--description", description]
    if org: args += ["--owner", org]
    run(args, cwd=path)

    typer.echo(f'Initialized repo at {path} on branch "{default_branch}".')
    if org: typer.echo(f"Created GitHub repo: {org}/{repo_name} (visibility: {visibility.value})")
    else:   typer.echo(f"Created GitHub repo: {repo_name} (visibility: {visibility.value})")
    typer.echo('Next step: run `shortgit push \"your first commit message\"` to push.')

@app.command()
def push(
    message: str = typer.Argument(..., help='Commit message (use quotes)'),
    path: Path = typer.Option(Path("."), "--path", "-p"),
    branch: Optional[str] = typer.Option(None, "--branch", "-b", help="Branch to push (default: current)"),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Allow empty commit if nothing changed"),
    set_upstream: bool = typer.Option(True, "--upstream/--no-upstream", help="Use -u on first push"),
):
    ensure_tool("git","https://git-scm.com/downloads")
    if not (path/".git").exists():
        raise RuntimeError(f"{path} is not a git repository. Run `shortgit init` first.")

    run(["git","add","-A"], cwd=path)
    try:
        status = run(["git","status","--porcelain"], cwd=path)
        if status.strip():
            run(["git","commit","-m",message], cwd=path)
        elif allow_empty:
            run(["git","commit","--allow-empty","-m",message], cwd=path)
        else:
            typer.echo("No changes to commit. Proceeding to push any existing commits.")
    except RuntimeError as e:
        if "nothing to commit" in str(e):
            typer.echo("Nothing to commit. Proceeding to push.")
        else:
            raise

    try:
        run(["git","remote","get-url","origin"], cwd=path)
    except RuntimeError:
        raise RuntimeError("No 'origin' remote configured. Run `shortgit init` or add a remote manually.")

    br = branch or current_branch(path)
    try:
        if set_upstream:
            run(["git","push","-u","origin",br], cwd=path)
        else:
            run(["git","push","origin",br], cwd=path)
    except RuntimeError as e:
        if set_upstream and "set-upstream" in str(e).lower():
            run(["git","push","origin",br], cwd=path)
        else:
            raise
    typer.echo(f"Pushed branch '{br}' to origin.")

def main(): app()
if __name__ == "__main__": main()
