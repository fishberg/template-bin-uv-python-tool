# template-bin-uv-python-tool

A runnable template for `uv`-managed Python command-line tools installed to
`~/.local/bin`.
The example prints a placeholder message; replace it with your tool's behavior.

## Requirements

- Bash and `readlink -f` (as provided on Linux).
- `uv` on your PATH, with Python 3.10 or newer available to it.
- `~/.local/bin` on your PATH to run the installed command by name. If needed,
  add `export PATH="$HOME/.local/bin:$PATH"` to your shell startup file.

## Install and run

From the project directory:

```bash
./install.sh
example-tool
example-tool --help
```

The installer creates `~/.local/bin/example-tool` as a symlink to the launcher
in this project. Keep the project folder in place while the command is installed;
the launcher uses its Python source and uv environment. The first run lets uv
prepare the environment. You can also run `./example-tool` without installing it.

To uninstall, run this from the project directory:

```bash
./uninstall.sh
```

Installation and uninstallation are safe to repeat and refuse to replace or
remove unrelated commands. Uninstallation leaves the project folder and its
environment available.

## Instructions for coding agents

Use this checklist when turning this template into a tool. For example, a tool named
`my-tool` lives in `my-tool/`, has a launcher named `my-tool`, and
uses `my_tool.py`. Use lowercase names and convert hyphens to underscores
in the Python filename.

1. Rename `example-tool` to `my-tool` and `example_tool.py` to
   `my_tool.py`.

2. Replace every `example-tool` and `example_tool.py` reference in the launcher,
   `install.sh`, `uninstall.sh`, and Python implementation with the chosen names.
   In `pyproject.toml`, change `project.name` to `my-tool` and set a useful
   description. Update the Python module docstring and argparse description too.
   Regenerate the lockfile from the new project directory:

   ```bash
   uv lock
   chmod +x my-tool install.sh uninstall.sh
   ```

   Commit `uv.lock` with the project; do not leave its package name as
   `example-tool` or edit the lockfile by hand.

3. Implement the requested behavior in `my_tool.py`:
   - Keep Python `>=3.10`. The example starts without dependencies
     (`dependencies = []`); add packages as needed with `uv add <package>` and
     commit both `pyproject.toml` and `uv.lock`.
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

4. Validate from a separate scratch directory using the checklist below, then
   replace this README with the new tool's purpose, arguments, examples,
   requirements, and install/uninstall instructions.

## Validation checklist

- Check shell syntax with `bash -n example-tool install.sh uninstall.sh`.
- From a separate scratch directory, invoke the launcher by its absolute path.
  Check normal output, `--help`, and rejection of unknown arguments. Verify that
  any relative input/output paths use the scratch directory.
- Using a temporary `HOME`, install twice, run the installed command from the
  scratch directory, and uninstall twice. Keep `uv` on PATH during these checks.
- Verify both installers refuse to touch an unrelated file, an unrelated
  symlink, and a broken symlink at the command's installation path.
- Run `uv lock --check` to confirm the lockfile matches the project metadata.

## Files

| File | Purpose |
| - | - |
| `example-tool` | Executable Bash launcher; finds this project through symlinks and invokes `uv run`. |
| `example_tool.py` | Python CLI implementation with an argparse entry point. |
| `install.sh` | Creates `~/.local/bin/example-tool`; safe to run repeatedly. |
| `uninstall.sh` | Removes the installed symlink only when it points into this project folder. |
| `pyproject.toml` / `uv.lock` | Python version, project metadata, and reproducible dependency resolution. |
| `.gitignore` | Excludes the virtual environment and Python bytecode cache. |

The launcher runs `uv run --quiet --project "$DIR" python
"$DIR/example_tool.py" "$@"`. The environment belongs to this project while
the Python process retains the caller's working directory.
