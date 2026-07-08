# Pyim Version 1.0.0
# License: MIT License

# Pyim is an optional built-in text editor for Pyash. 
# It is a simple line-based editor that allows you to edit text files from the command line.

# Pyash will still function even if "pyim.py" is not available, but you will not be able to use the "pyim" command to edit files.

import os
import shlex
import sys

safe_path = None


def set_safe_path(fn):
    global safe_path
    safe_path = fn


def _emit(message=""):
    stream = getattr(sys, "__stdout__", None) or sys.stdout
    text = str(message)
    if text and not text.endswith("\n"):
        text += "\n"
    stream.write(text)
    try:
        stream.flush()
    except Exception:
        pass


def _read_line(prompt=""):
    stream = getattr(sys, "__stdout__", None) or sys.stdout
    if prompt:
        stream.write(prompt)
        try:
            stream.flush()
        except Exception:
            pass
    line = sys.stdin.readline()
    if line.endswith("\n"):
        line = line[:-1]
    return line


def pyim(args):
    if not args:
        _emit("pyim: missing file operand")
        _emit("Usage: pyim <filename>")
        return

    filename = args[0]
    if safe_path is None:
        _emit("pyim: internal error: safe_path not initialized")
        return
    try:
        target_path = safe_path(filename)
    except PermissionError:
        _emit(f"pyim: cannot access '{filename}': Permission denied (outside shell folder)")
        return

    lines = []
    if os.path.exists(target_path):
        try:
            with open(target_path, "r", encoding="utf-8") as handle:
                lines = handle.read().splitlines()
        except Exception as exc:
            _emit(f"pyim: error reading file: {exc}")
            return

    _emit(f"pyim: editing {filename}")
    _emit("Commands: help, p, i <n> <text>, a <n> <text>, r <n> <text>, d <n>, s <old> <new>, :w, :q, :wq")

    def write_file():
        try:
            with open(target_path, "w", encoding="utf-8") as handle:
                handle.write("\n".join(lines) + ("\n" if lines else ""))
            _emit(f"pyim: wrote {filename}")
            return True
        except Exception as exc:
            _emit(f"pyim: error writing file: {exc}")
            return False

    while True:
        try:
            raw_command = _read_line("pyim> ")
        except (KeyboardInterrupt, EOFError):
            _emit("\npyim: aborted")
            return

        if not raw_command:
            continue

        if raw_command in {":q", ":x", "q", "x", ":quit", ":exit", "quit", "exit"}:
            return
        if raw_command in {":w", "w"}:
            write_file()
            continue
        if raw_command in {":wq", "wq"}:
            if write_file():
                return
            continue

        parts = shlex.split(raw_command)
        cmd = parts[0]

        if cmd == "help":
            _emit("pyim commands:")
            _emit("  p                    - print file contents")
            _emit("  i <n> <text>         - insert text before line n")
            _emit("  a <n> <text>         - append text after line n")
            _emit("  r <n> <text>         - replace line n")
            _emit("  d <n>                - delete line n")
            _emit("  s <old> <new>        - substitute text in entire file")
            _emit("  :w                   - save file")
            _emit("  :q                   - quit without saving")
            _emit("  :wq                  - save and quit")
            continue

        if cmd == "p":
            if not lines:
                _emit("(empty file)")
            for index, line in enumerate(lines, 1):
                _emit(f"{index:4}  {line}")
            continue

        if cmd in {"i", "a", "r", "d"}:
            if len(parts) < 2:
                _emit(f"pyim: {cmd}: missing line number")
                continue
            try:
                line_number = int(parts[1])
            except ValueError:
                _emit(f"pyim: {cmd}: invalid line number: {parts[1]}")
                continue

            if line_number < 1 or line_number > len(lines) + (1 if cmd in {"i", "a"} else 0):
                _emit(f"pyim: {cmd}: line number out of range")
                continue

            text = raw_command.split(None, 2)[2] if len(raw_command.split(None, 2)) > 2 else ""

            if cmd == "d":
                if line_number > len(lines):
                    _emit("pyim: d: line number out of range")
                    continue
                del lines[line_number - 1]
                continue

            if cmd == "r":
                if line_number > len(lines):
                    _emit("pyim: r: line number out of range")
                    continue
                lines[line_number - 1] = text
                continue

            if cmd == "i":
                lines.insert(line_number - 1, text)
                continue

            if cmd == "a":
                insert_at = line_number if line_number <= len(lines) else len(lines)
                lines.insert(insert_at, text)
                continue

        if cmd == "s":
            if len(parts) < 3:
                _emit("pyim: s: missing old and new text")
                continue
            old = parts[1]
            new = parts[2]
            lines = [line.replace(old, new) for line in lines]
            continue

        print(f"pyim: unknown command: {cmd}")