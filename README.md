# template-init-script

A runnable starting point for a small `uv` Python command.
The example prints a placeholder message; replace it with your tool's behavior.

## Requirements

- Bash and `readlink -f` (as provided on Linux).
- `uv` on your PATH, with Python 3.10 or newer available to it.
- `~/.local/bin` on your PATH to run the installed command by name. If needed,
  add `export PATH="$HOME/.local/bin:$PATH"` to your shell startup file.

## Instructions for coding agents

Use this checklist when turning this template into a tool. `X` below stands for
the chosen suffix, not a literal character. For example, a tool named
`init-my-tool` lives in `init-my-tool/`, has a launcher named `init-my-tool`, and
uses `init_my_tool.py`. Use lowercase names and convert hyphens to underscores
in the Python filename.

1. From the directory where the new project should live, copy the template:

   ```bash
   init-template -t template-init-script init-my-tool
   cd init-my-tool
   ```

   This requires the `init-template` tool from `my-templates` to be installed
   and this template to be in its `templates/` directory. Alternatively, copy
   this template's contents into a new `init-my-tool/` folder, including hidden
   files but excluding `.git/`, `.venv/`, and `__pycache__/`. Do not overwrite an
   existing project. Keep this source template unchanged.

2. Rename `init-example` to `init-my-tool` and `init_example.py` to
   `init_my_tool.py`.

3. Replace every `init-example` and `init_example.py` reference in the launcher,
   `install.sh`, `uninstall.sh`, and Python implementation with the chosen names.
   In `pyproject.toml`, change `project.name` to `init-my-tool` and set a useful
   description. Update the Python module docstring and argparse description too.
   Regenerate the lockfile from the new project directory:

   ```bash
   uv lock
   chmod +x init-my-tool install.sh uninstall.sh
   ```

   Commit `uv.lock` with the project; do not leave its package name as
   `init-example` or edit the lockfile by hand.

4. Implement the requested behavior in `init_my_tool.py`:
   - Keep Python `>=3.10` and standard-library-only code (`dependencies = []`).
   - Keep `argparse` with an explicit `prog` matching the command name.
   - Use `sys.exit("error: ...")` for operational failures, importing `sys`
     when needed. Let argparse report invalid arguments.
   - Resolve user output paths relative to the caller's working directory.
     Use `Path(__file__).resolve().parent` for assets beside the script.
   - Never overwrite existing user files; treat symlinks, including broken
     symlinks, as occupied destinations. Use exclusive creation (`open(...,
     "x")`) when writing new files.
   - Preserve the launcher's symlink resolution, `"$@"` argument forwarding,
     and caller's working directory. Do not add a `cd` to the launcher.
   - Preserve the installers' ownership checks so unrelated commands are
     never replaced or removed.

5. Validate from a separate scratch directory using the checklist below, then
   replace this README with the new tool's purpose, arguments, examples,
   requirements, and install/uninstall instructions.

## Files

| File | Purpose |
| - | - |
| `init-example` | Executable Bash launcher; finds this project through symlinks and invokes `uv run`. |
| `init_example.py` | Python CLI implementation with an argparse entry point. |
| `install.sh` | Creates `~/.local/bin/init-example`; safe to run repeatedly. |
| `uninstall.sh` | Removes the installed symlink only when it points into this project folder. |
| `pyproject.toml` / `uv.lock` | Python version, project metadata, and reproducible dependency resolution. |
| `.gitignore` | Excludes the virtual environment and Python bytecode cache. |

The launcher runs `uv run --quiet --project "$DIR" python
"$DIR/init_example.py" "$@"`. The environment belongs to this project while
the Python process retains the caller's working directory.
