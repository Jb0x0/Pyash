# Pyash Version 1.2.0
# License: MIT License

# This is a shell EMULATOR, it is also restricted to a shell folder, so you can't access files outside of it. This is for security reasons.

# Please read INSTRUCTIONS.txt (located in the "pyash" folder) if this is your first time using Pyash.

import os
import sys
import random
import subprocess
import shutil
import stat
import time
import shlex
import platform
import io
import atexit
from contextlib import redirect_stdout
from datetime import datetime

try:
    import pyim  # This displays an error in most IDEs/Text editors, but as long as the pyim.py file is in the same directory/folder as this file, it can be imported.
except ImportError:
    class _PyimFallback:
        @staticmethod
        def set_safe_path(*args, **kwargs):
            return None

        @staticmethod
        def pyim(args=None):
            print("pyim: pyim.py not found")

    pyim = _PyimFallback()

try:
    from colorama import Fore as ColoramaFore, Style as ColoramaStyle, init as colorama_init
    _COLORAMA_AVAILABLE = True
except ImportError:
    _COLORAMA_AVAILABLE = False

    class _ColorFallback:
        def __getattr__(self, name):
            return ""

    ColoramaFore = _ColorFallback()
    ColoramaStyle = _ColorFallback()

    def colorama_init(*args, **kwargs):
        return None

Fore = ColoramaFore
Style = ColoramaStyle
COLORAMA_ENABLED = _COLORAMA_AVAILABLE


def set_colorama_enabled(enabled):
    global Fore, Style, COLORAMA_ENABLED
    if enabled and _COLORAMA_AVAILABLE:
        from colorama import Fore as ColoramaFore, Style as ColoramaStyle
        Fore = ColoramaFore
        Style = ColoramaStyle
    else:
        class _ColorFallback:
            def __getattr__(self, name):
                return ""

        Fore = _ColorFallback()
        Style = _ColorFallback()

    COLORAMA_ENABLED = enabled and _COLORAMA_AVAILABLE
    colorama_init(autoreset=True)
    return COLORAMA_ENABLED

try:
    import readline
except ImportError:
    readline = None

set_colorama_enabled(COLORAMA_ENABLED)

command_history = []
shell_root = ""
SHELL_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".pyash_shell_path")
HISTORY_FILE = None


def setup_history():
    global HISTORY_FILE
    if not shell_root:
        HISTORY_FILE = os.path.join(os.getcwd(), ".pyash_history")
    else:
        HISTORY_FILE = os.path.join(shell_root, ".pyash_history")

    try:
        history_dir = os.path.dirname(HISTORY_FILE)
        if history_dir and not os.path.exists(history_dir):
            os.makedirs(history_dir, exist_ok=True)
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "a", encoding="utf-8"):
                pass

        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.rstrip("\n")
                    if line and line not in command_history:
                        command_history.append(line)

        if readline is not None:
            try:
                readline.read_history_file(HISTORY_FILE)
            except FileNotFoundError:
                pass
            except OSError:
                pass

            try:
                readline.set_history_length(1000)
            except Exception:
                pass
    except OSError:
        pass


def save_history():
    if not HISTORY_FILE:
        return

    try:
        history_dir = os.path.dirname(HISTORY_FILE)
        if history_dir and not os.path.exists(history_dir):
            os.makedirs(history_dir, exist_ok=True)

        with open(HISTORY_FILE, "w", encoding="utf-8") as handle:
            for entry in command_history:
                handle.write(entry + "\n")
    except OSError:
        pass

    if readline is not None:
        try:
            readline.write_history_file(HISTORY_FILE)
        except OSError:
            pass


def add_history_entry(command):
    if not command:
        return
    if command_history and command_history[-1] == command:
        return
    command_history.append(command)
    if HISTORY_FILE:
        try:
            history_dir = os.path.dirname(HISTORY_FILE)
            if history_dir and not os.path.exists(history_dir):
                os.makedirs(history_dir, exist_ok=True)
            with open(HISTORY_FILE, "a", encoding="utf-8") as handle:
                handle.write(command + "\n")
        except OSError:
            pass
    if readline is not None:
        try:
            readline.add_history(command)
        except Exception:
            pass


atexit.register(save_history)


def clear_screen(args):
    os.system("clear")
clear_scr = clear_screen


def safe_path(target):
    if target is None:
        raise PermissionError("Access denied: Outside sandbox.")

    target_str = os.fspath(target)
    if not isinstance(target_str, str):
        raise TypeError("Path must be a string")

    candidate = os.path.abspath(os.path.join(os.getcwd(), os.path.expanduser(target_str)))
    root_real = os.path.realpath(shell_root or os.getcwd())
    resolved_target = os.path.realpath(candidate)

    try:
        if os.path.commonpath([root_real, resolved_target]) != root_real:
            raise PermissionError("Access denied: Outside sandbox.")
    except ValueError:
        raise PermissionError("Access denied: Outside sandbox.")

    return resolved_target


pyim.set_safe_path(safe_path)


def read_shell_config():
    if not os.path.exists(SHELL_CONFIG_FILE):
        return None
    try:
        with open(SHELL_CONFIG_FILE, "r", encoding="utf-8") as f:
            path = f.read().strip()
        if path:
            return os.path.abspath(os.path.expanduser(path))
    except Exception:
        return None
    return None


def write_shell_config(path):
    try:
        with open(SHELL_CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(os.path.abspath(path))
    except Exception as e:
        print(f"shell: could not save shell location: {e}")


def resolve_setup_path(base_dir, target):
    return os.path.abspath(os.path.join(base_dir, os.path.expanduser(target)))


def choose_shell_location():
    current_dir = os.path.abspath(os.getcwd())
    clear_screen([])
    print(f"{Fore.BLUE}Please read INSTRUCTIONS.txt if this is your first time using Pyash.")
    print("\nShell folder not found.")
    print("Choose where to create it.")
    print("Commands: cd <dir>, cd .., pwd, ls, select <dir>, quit")

    while True:
        try:
            print(f"\nCurrent directory: {current_dir}")
            try:
                entries = sorted(
                    entry for entry in os.listdir(current_dir)
                    if os.path.isdir(os.path.join(current_dir, entry))
            )
            except OSError:
                entries = []

            for entry in entries:
                print(f"  {Fore.BLUE}{entry}/{Style.RESET_ALL}")

            if not entries:
                print(f"{Fore.GREEN}Directory empty{Style.RESET_ALL}")

            print()
            choice = input("shell-setup> ").strip()
            if not choice:
                continue

            if choice.lower() in {"quit", "exit"}:
                print("\nExiting shell emulator.")
                sys.exit(0)
            if choice.lower() == "pwd":
                print(current_dir)
                continue
            if choice.lower() == "ls":
                continue
            if choice.lower() in {"list", "dir"}:
                print("Unknown command. Use 'ls' for a directory listing.")
                continue
            if choice.lower() == "select":
                return current_dir

            if choice.lower().startswith("select "):
                target = choice[7:].strip()
                if not target:
                    continue
                target_path = resolve_setup_path(current_dir, target)
                if not os.path.exists(target_path):
                    print(f"select: {target}: No such file or directory")
                    continue
                if not os.path.isdir(target_path):
                    print(f"select: {target}: Not a directory")
                    continue
                current_dir = target_path
                print(f"Selected {current_dir}")
                return current_dir

            if choice.startswith("cd "):
                target = choice[3:].strip()
                if not target:
                    continue
                target_path = resolve_setup_path(current_dir, target)
                if not os.path.exists(target_path):
                    print(f"cd: {target}: No such file or directory")
                    continue
                if not os.path.isdir(target_path):
                    print(f"cd: {target}: Not a directory")
                    continue
                current_dir = target_path
                continue

            if choice == "cd ..":
                current_dir = os.path.dirname(current_dir) or "/"
                continue

            print("Unknown command. Use 'cd <dir>', 'cd ..', 'pwd', 'ls', 'select', or 'quit'.")
        
        except KeyboardInterrupt:
            print("\nExiting shell emulator.")
            sys.exit(0)

def setup_shell_dir():
    global shell_root

    configured_path = read_shell_config()
    if configured_path and os.path.isdir(configured_path):
        os.chdir(configured_path)
        shell_root = configured_path
        return

    default_shell_dir = os.path.join(os.getcwd(), "shell")
    if os.path.isdir(default_shell_dir):
        os.chdir(default_shell_dir)
        shell_root = default_shell_dir
        write_shell_config(default_shell_dir)
        return

    selected_dir = choose_shell_location()
    if selected_dir is None:
        selected_dir = os.getcwd()

    shell_dir = os.path.join(selected_dir, "shell")
    try:
        os.makedirs(shell_dir, exist_ok=True)
    except OSError as e:
        print(f"shell: could not create shell directory: {e}")
        shell_dir = os.path.join(os.getcwd(), "shell")
        os.makedirs(shell_dir, exist_ok=True)

    os.chdir(shell_dir)
    shell_root = shell_dir
    write_shell_config(shell_dir)
    print(f"Shell folder ready at: {shell_root}")


setup_shell_dir()
setup_history()
clear_screen([])

if not _COLORAMA_AVAILABLE:
    print("!!! Colorama not detected !!!\n\nTerminal will not have colored output. Install colorama for colored output.\n")


def get_prompt():
    user = os.getenv("USER") or "user"
    host = "pyash-emul"
    cwd = os.getcwd().replace(shell_root, "~")
    return f"{Fore.GREEN}{user}@{host}{Style.RESET_ALL}:{Fore.BLUE}{cwd}{Style.RESET_ALL}$ "

def ls(args):
    show_all = False  # -a
    long_format = False  # -l
    paths = []

    for arg in args:
        if arg.startswith('-'):
            if 'a' in arg:
                show_all = True
            if 'l' in arg:
                long_format = True
        else:
            paths.append(arg)

    path = paths[0] if paths else '.'

    try:
        path = safe_path(path)
        entries = os.listdir(path)
        if not show_all:
            entries = [e for e in entries if not e.startswith('.')]

        for entry in sorted(entries):
            full_path = os.path.join(path, entry)
            is_dir = os.path.isdir(full_path)
            is_exec = os.access(full_path, os.X_OK)

            if long_format:
                try:
                    stats = os.stat(full_path)
                except FileNotFoundError:
                    print(f"ls: cannot access '{entry}': No such file or directory")
                    continue

                mode = stat.filemode(stats.st_mode)
                n_links = stats.st_nlink
                size = stats.st_size
                mtime = time.strftime('%b %d %H:%M', time.localtime(stats.st_mtime))
                name = entry + ('/' if is_dir else '*' if is_exec else '')

                color = Fore.BLUE if is_dir else Fore.GREEN if is_exec else ''
                print(f"{mode} {n_links:2} user user {size:6} {mtime} {color}{name}{Style.RESET_ALL}")
            else:
                color = Fore.BLUE if is_dir else Fore.GREEN if is_exec else ''
                suffix = '/' if is_dir else '*' if is_exec else ''
                print(color + entry + suffix + Style.RESET_ALL)

    except PermissionError:
        print("ls: Permission denied (outside shell folder)")
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory")
    except NotADirectoryError:
        print(f"ls: cannot access '{path}': Not a directory")

def cat(args):
    if not args:
        if not sys.stdin.isatty():
            print(sys.stdin.read(), end='')
            return
        print("cat: missing file operand")
        return
    for filename in args:
        try:
            with open(safe_path(filename), 'r') as f:
                print(f.read(), end='')
        except PermissionError:
            print(f"cat: {filename}: Permission denied (outside shell folder)")
        except FileNotFoundError:
            print(f"cat: {filename}: No such file or directory")

def pwd(args):
    print(os.getcwd())

def cd(args):
    if not args:
        os.chdir(shell_root)
        return
    target = args[0]
    if target == '~':
        target_path = shell_root
    else:
        try:
            target_path = safe_path(target)
        except PermissionError:
            print(f"cd: {target}: Permission denied (outside shell folder)")
            return
    try:
        os.chdir(target_path)
    except FileNotFoundError:
        print(f"cd: {target}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {target}: Not a directory")

def echo(args):
    if '>>' in args:
        idx = args.index('>>')
        content = ' '.join(args[:idx])
        filename = args[idx + 1] if idx + 1 < len(args) else None
        if filename:
            try:
                target_path = safe_path(filename)
                with open(target_path, 'a') as f:
                    f.write(content + '\n')
            except PermissionError:
                print(f"echo: cannot append to '{filename}': Permission denied (outside shell folder)")
            except Exception as e:
                print(f"echo: cannot append to '{filename}': {e}")
        else:
            print("echo: syntax error near unexpected token `newline'")
    elif '>' in args:
        idx = args.index('>')
        content = ' '.join(args[:idx])
        filename = args[idx + 1] if idx + 1 < len(args) else None
        if filename:
            try:
                target_path = safe_path(filename)
                with open(target_path, 'w') as f:
                    f.write(content + '\n')
            except PermissionError:
                print(f"echo: cannot write to '{filename}': Permission denied (outside shell folder)")
            except Exception as e:
                print(f"echo: cannot write to '{filename}': {e}")
        else:
            print("echo: syntax error near unexpected token `newline'")
    else:
        print(' '.join(args))

def mkdir(args):
    if not args:
        print("mkdir: missing operand")
        return
    for directory in args:
        try:
            os.makedirs(safe_path(directory))
        except PermissionError:
            print(f"mkdir: cannot create directory '{directory}': Permission denied (outside shell folder)")
        except FileExistsError:
            print(f"mkdir: cannot create directory '{directory}': File exists")
        except FileNotFoundError:
            print(f"mkdir: cannot create directory '{directory}': No such file or directory")

def rmdir(args):
    if not args:
        print("rmdir: missing operand")
        return
    for directory in args:
        try:
            os.rmdir(safe_path(directory))
        except PermissionError:
            print(f"rmdir: failed to remove '{directory}': Permission denied (outside shell folder)")
        except FileNotFoundError:
            print(f"rmdir: failed to remove '{directory}': No such file or directory")
        except OSError:
            print(f"rmdir: failed to remove '{directory}': Directory not empty or other error")

def rm(args):
    if not args:
        print("rm: missing operand")
        return
    for filename in args:
        try:
            os.remove(safe_path(filename))
        except PermissionError:
            print(f"rm: cannot remove '{filename}': Permission denied (outside shell folder)")
        except FileNotFoundError:
            print(f"rm: cannot remove '{filename}': No such file or directory")
        except IsADirectoryError:
            print(f"rm: cannot remove '{filename}': Is a directory")

def touch(args):
    if not args:
        print("touch: missing file operand")
        return
    for filename in args:
        try:
            target_path = safe_path(filename)
            with open(target_path, 'a'):
                os.utime(target_path, None)
        except PermissionError:
            print(f"touch: cannot touch '{filename}': Permission denied (outside shell folder)")
        except Exception as e:
            print(f"touch: cannot touch '{filename}': {e}")

def cp(args):
    if len(args) < 2:
        print("cp: missing file operand")
        return
    src, dest = args[0], args[1]
    try:
        src_path = safe_path(src)
        dest_path = safe_path(dest)
    except PermissionError:
        print(f"cp: cannot stat '{src}': Permission denied (outside shell folder)")
        return
    try:
        with open(src_path, 'rb') as fsrc:
            with open(dest_path, 'wb') as fdest:
                fdest.write(fsrc.read())
    except FileNotFoundError:
        print(f"cp: cannot stat '{src}': No such file or directory")
    except IsADirectoryError:
        print(f"cp: omitting directory '{src}'")

def mv(args):
    if len(args) < 2:
        print("mv: missing file operand")
        return

    *sources, destination = args

    try:
        destination_path = safe_path(destination)
    except PermissionError:
        print(f"mv: target '{destination}' is outside the shell folder")
        return

    if len(sources) > 1:
        if not os.path.isdir(destination_path):
            print(f"mv: target '{destination}' is not a directory")
            return

    for src in sources:
        try:
            src_path = safe_path(src)
        except PermissionError:
            print(f"mv: cannot stat '{src}': Permission denied (outside shell folder)")
            continue

        if not os.path.exists(src_path):
            print(f"mv: cannot stat '{src}': No such file or directory")
            continue

        if os.path.isdir(destination_path):
            dest_path = os.path.join(destination_path, os.path.basename(src_path))
        else:
            dest_path = destination_path

        if os.path.exists(dest_path):
            response = input(f"mv: overwrite '{dest_path}'? [y/N] ").lower()
            if response != 'y':
                print(f"mv: not overwriting '{dest_path}'")
                continue

        try:
            shutil.move(src_path, dest_path)
            print(f"Moved '{src}' -> '{dest_path}'")
        except Exception as e:
            print(f"mv: error moving '{src}': {e}")

def head(args):
    if not args:
        if not sys.stdin.isatty():
            for i, line in enumerate(sys.stdin):
                if i >= 10:
                    break
                print(line, end='')
            return
        print("head: missing file operand")
        return
    for filename in args:
        try:
            with open(safe_path(filename)) as f:
                for i, line in enumerate(f):
                    if i >= 10:
                        break
                    print(line, end='')
        except PermissionError:
            print(f"head: cannot open '{filename}': Permission denied (outside shell folder)")
        except FileNotFoundError:
            print(f"head: cannot open '{filename}': No such file")

def tail(args):
    if not args:
        if not sys.stdin.isatty():
            lines = sys.stdin.readlines()
            for line in lines[-10:]:
                print(line, end='')
            return
        print("tail: missing file operand")
        return
    for filename in args:
        try:
            with open(safe_path(filename)) as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    print(line, end='')
        except PermissionError:
            print(f"tail: cannot open '{filename}': Permission denied (outside shell folder)")
        except FileNotFoundError:
            print(f"tail: cannot open '{filename}': No such file")

def uptime(args):
    fake_uptime = random.randint(1, 10000)
    hours = fake_uptime // 3600
    minutes = (fake_uptime % 3600) // 60
    print(f" {hours}:{minutes:02d},  1 user,  load average: 0.00, 0.01, 0.05")

def uname(args):
    print(f"{platform.system()} pyash-emul {platform.release()}")

def help_cmd(args):
    print(Fore.BLUE + "\nAvailable commands:")
    for cmd in sorted(commands.keys()):
        print(f"{Fore.WHITE}  {cmd}")
    print("")

def whoami(args):
    print(os.getenv("USER") or "user")

def date(args):
    now = datetime.now()
    print(now.strftime("%a %b %d %H:%M:%S %Y"))

def info(args):
    print(Fore.GREEN + "\n|| Pyash Emulator ||\n")
    print(f"{Fore.WHITE}Type 'help' for a list of commands.\n")

def man(args):
    man_pages = {
        'ls': "List directory contents.",
        'cat': "Concatenate and print files.",
        'cd': "Change directory.",
        'echo': "Display a line of text or redirect to a file.",
        'mkdir': "Create directories.",
        'rmdir': "Remove empty directories.",
        'rm': "Remove files.",
        'touch': "Create an empty file or update timestamp.",
        'whoami': "Print current user.",
        'date': "Display current date and time.",
        'clear': "Clear the screen.",
        'info': "Show emulator info.",
        'exit': "Exit the shell.",
        'man': "Show manual pages for commands.",
        'tree': "Display directory structure.",
        'fortune': "Print a random quote.",
        'history': "Show command history.",
        'cp': "Copy files.",
        'mv': "Move/rename files.",
        'head': "Display the first 10 lines of a file.",
        'tail': "Display the last 10 lines of a file.",
        'uptime': "Show system uptime.",
        'uname': "Show system information.",
        'extras': "Shows a list of third party commands.",
        'dd': "Convert and copy a file.",
        'run': "Run a command in the system shell. \n\n(WARNING: can run ANY command on your ACTUAL system/shell, even outside the shell folder)",
    }
    if not args:
        print("What manual page do you want?")
        return
    for cmd in args:
        print(Fore.YELLOW + f"{cmd}" + Style.RESET_ALL + " - " + man_pages.get(cmd, 'No manual entry for ' + cmd))

def history(args):
    if not args:
        for i, cmd in enumerate(command_history, 1):
            print(f"{i}  {cmd}")
        return

    for arg in args:
        try:
            index = int(arg)
            if index < 1 or index > len(command_history):
                print(f"history: {index}: history position out of range")
                continue
            print(f"{index}  {command_history[index - 1]}")
        except ValueError:
            print(f"history: {arg}: numeric argument required")


def tree(args, prefix=""):
    path = args[0] if args else "."
    try:
        path = safe_path(path)
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            colored_item = (Fore.BLUE + item + Style.RESET_ALL) if os.path.isdir(full_path) else item
            print(prefix + "|-- " + colored_item)
            if os.path.isdir(full_path):
                tree([full_path], prefix + "   ")
    except PermissionError:
        print(f"tree: {path}: Permission denied (outside shell folder)")
    except FileNotFoundError:
        print(f"tree: {path}: No such file or directory")

def dd(args):
    if_file = None
    of_file = None

    for arg in args:
        if arg.startswith('if='):
            if_file = arg[3:]
        elif arg.startswith('of='):
            of_file = arg[3:]

    if not if_file or not of_file:
        print("dd: missing operand")
        return

    if any(path.startswith(('/dev/', '/sys/')) for path in (if_file, of_file)):
        print("dd: Permission denied (access to system devices blocked in emulator)")
        return

    try:
        import shutil
        shutil.copyfile(safe_path(if_file), safe_path(of_file))
        print(f"dd: successfully copied '{if_file}' to '{of_file}'")
    except PermissionError:
        print("dd: Permission denied (outside shell folder)")
    except FileNotFoundError:
        print("dd: input or output file not found.")
    except Exception as e:
        print(f"dd: error: {e}")

def fortune(args):
    quotes = [
        "Unix is simple. It just takes a genius to understand its simplicity.",
        "Talk is cheap. Show me the code.",
        "There is no place like 127.0.0.1",
        "Beware of bugs in the above code.",
        "Shells are like onions, they have layers.",
        "Don't start Bash-ing stuff around.",
        "In a world without fences and walls, who needs Gates and Windows?",
        "The best way to predict the future is to invent it.",
        "To err is human, but to really foul things up you need a computer.",
        "Linux is free! (Free as in freedom, not free beer.)",
        "BSD is free! (Free as in free speech, not free beer.)",
        "Python is the best language for everything, except when it's not.",
        "when's the full rewrite of the code in pure Machine Code coming???"
    ]
    print(random.choice(quotes))

def chmod(args):
    if len(args) < 2:
        print("chmod: missing operand")
        return

    mode = args[0]
    filename = args[1]

    try:
        target_path = safe_path(filename)
    except PermissionError:
        print(f"chmod: cannot access '{filename}': Permission denied (outside shell folder)")
        return

    if not os.path.exists(target_path):
        print(f"chmod: cannot access '{filename}': No such file or directory")
        return

    try:
        mode_int = int(mode, 8)
        os.chmod(target_path, mode_int)
        return
    except ValueError:
        pass  # Not octal, try symbolic below

    try:
        current_mode = os.stat(target_path).st_mode

        if mode.startswith('+') or mode.startswith('-'):
            action = mode[0]
            perm = mode[1:]

            perms = {
                'x': stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                'r': stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH,
                'w': stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH,
            }

            if perm not in perms:
                print(f"chmod: invalid mode: '{mode}'")
                return

            if action == '+':
                new_mode = current_mode | perms[perm]
            elif action == '-':
                new_mode = current_mode & ~perms[perm]
            else:
                print(f"chmod: unsupported symbolic mode: '{mode}'")
                return

            os.chmod(target_path, new_mode)
            return

        print(f"chmod: invalid mode: '{mode}'")
    except Exception as e:
        print(f"chmod: error changing mode of '{filename}': {e}")

def missing_command(command_name, package_name=None):
    print(f"\n{command_name}: command not found.")
    print(f"Perhaps the package listed in .pyash_extras is missing/mistyped? Package: {package_name}\n")


def toggle_colorama(args):
    new_state = not COLORAMA_ENABLED
    if new_state and not _COLORAMA_AVAILABLE:
        print("toggle_colorama: Colorama is not available")
        return

    set_colorama_enabled(new_state)
    status = "enabled" if COLORAMA_ENABLED else "disabled"
    print(f"toggle_colorama: Colorama {status}")


def destroy_shell(args):
    if not shell_root:
        print("destroy_shell: no shell folder is currently active")
        return

    if not os.path.exists(shell_root):
        print(f"destroy_shell: shell folder not found: {shell_root}")
        return

    prompt = f"This will permanently delete the current shell folder and everything in it ({shell_root}). Continue? [y/N] "
    sys.__stdout__.write(prompt)
    sys.__stdout__.flush()
    confirmation = input().strip().lower()
    if confirmation not in {"y", "yes"}:
        print("destroy_shell: aborted")
        return

    try:
        parent_dir = os.path.dirname(shell_root) or os.path.expanduser("~")
        os.chdir(parent_dir)
        shutil.rmtree(shell_root)
        print(f"destroy_shell: removed {shell_root}")
        os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:])
    except OSError as exc:
        print(f"destroy_shell: failed to remove shell folder: {exc}")


def ensure_extras_file():
    extras_path = os.path.join(shell_root, ".pyash_extras")
    try:
        if not os.path.exists(extras_path):
            with open(extras_path, "a", encoding="utf-8") as handle:
                handle.write("# Add one custom command per line: <command_name> [package_name]\n")
                handle.write("# Example: vim vim\n")
    except OSError:
        pass
    return extras_path


def get_custom_extras():
    extras_path = ensure_extras_file()
    entries = {}
    try:
        with open(extras_path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = shlex.split(line)
                if not parts:
                    continue
                command_name = parts[0]
                package_name = parts[1] if len(parts) > 1 else command_name
                entries[command_name] = package_name
    except OSError:
        return {}
    return entries


def create_extra_command_runner(command_name, package_name):
    def runner(args):
        try:
            subprocess.run([command_name] + args, cwd=shell_root)
        except FileNotFoundError:
            missing_command(command_name, package_name)
    return runner


def reload_extra_commands():
    global extra_commands, custom_extra_commands
    extra_commands = dict(base_extra_commands)
    custom_extra_commands = get_custom_extras()
    for command_name, package_name in custom_extra_commands.items():
        if command_name in extra_commands:
            continue
        extra_commands[command_name] = create_extra_command_runner(command_name, package_name)


def extras(args):
    reload_extra_commands()
    print(Fore.BLUE + "\nExtra Commands:")
    for command_name in sorted(base_extra_commands):
        print(f"{Fore.WHITE}  {command_name}")
    for command_name, package_name in sorted(custom_extra_commands.items()):
        print(f"{Fore.WHITE}  {command_name} - custom command")
    print("")


commands = {
    'ls': ls,
    'cat': cat,
    'pwd': pwd,
    'cd': cd,
    'echo': echo,
    'mkdir': mkdir,
    'rmdir': rmdir,
    'rm': rm,
    'touch': touch,
    'cp': cp,
    'mv': mv,
    'head': head,
    'tail': tail,
    'uptime': uptime,
    'uname': uname,
    'help': help_cmd,
    'clear': clear_screen,
    'whoami': whoami,
    'date': date,
    'exit': lambda args: sys.exit(0),
    'info': info,
    'man': man,
    'history': history,
    'tree': tree,
    'fortune': fortune,
    'dd': dd,
    'extras': extras,
    'chmod': chmod,
}

base_extra_commands = {
    'destroy_shell': destroy_shell,
    'toggle_colorama': toggle_colorama,
    'pyim': pyim.pyim,
}
custom_extra_commands = {}
extra_commands = dict(base_extra_commands)
reload_extra_commands()


def run_command(cmd, args, input_data=None):
    reload_extra_commands()

    if cmd.startswith('./') and cmd.endswith('.sh'):
        script_path = os.path.abspath(cmd)
        if script_path.startswith(shell_root) and os.path.isfile(script_path):
            try:
                result = subprocess.run(["bash", script_path] + args, input=input_data, text=True, capture_output=True)
                if result.returncode != 0:
                    if result.stderr:
                        print(result.stderr, end='')
                    return None
                return result.stdout
            except FileNotFoundError:
                print("\nbash: command not found.")
                return None
        else:
            print(f"{cmd}: Permission denied or file not found.")
            return None

    original_stdin = sys.stdin
    try:
        if input_data is not None:
            sys.stdin = io.StringIO(input_data)

        if cmd in commands:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                commands[cmd](args)
            return buffer.getvalue()
        elif cmd in extra_commands:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                extra_commands[cmd](args)
            return buffer.getvalue()
        else:
            print(f"{cmd}: command not found")
            return None
    finally:
        sys.stdin = original_stdin


def main():
    while True:
        try:
            inp = input(get_prompt()).strip()
            if not inp:
                continue
            add_history_entry(inp)

            if '&&' in inp:
                commands_chain = [cmd.strip() for cmd in inp.split('&&')]
                for cmd_str in commands_chain:
                    parts = shlex.split(cmd_str)
                    if not parts:
                        continue
                    cmd, *args = parts

                    if cmd.startswith('./') and cmd.endswith('.sh'):
                        script_path = os.path.abspath(cmd)
                        if script_path.startswith(shell_root) and os.path.isfile(script_path):
                            try:
                                result = subprocess.run(["bash", script_path] + args)
                                if result.returncode != 0:
                                    break
                            except FileNotFoundError:
                                print("\nbash: command not found.")
                                break
                        else:
                            print(f"{cmd}: Permission denied or file not found.")
                            break

                    elif cmd in commands:
                        commands[cmd](args)
                    elif cmd in extra_commands:
                        extra_commands[cmd](args)

                    else:
                        print(f"{cmd}: Command not allowed.")
                        break
                continue

            elif '|' in inp:
                pipe_parts = [cmd.strip() for cmd in inp.split('|') if cmd.strip()]
                if len(pipe_parts) < 2:
                    print("Syntax error: incomplete pipe command.")
                    continue

                input_data = None
                for index, cmd_str in enumerate(pipe_parts):
                    parts = shlex.split(cmd_str)
                    if not parts:
                        continue
                    cmd, *args = parts

                    output = run_command(cmd, args, input_data=input_data)
                    if output is None:
                        break

                    if index == len(pipe_parts) - 1:
                        if output:
                            print(output, end='')
                    else:
                        input_data = output
                continue

            parts = shlex.split(inp)
            if not parts:
                continue
            cmd, *args = parts
            reload_extra_commands()

            if cmd.startswith('./') and cmd.endswith('.sh'):
                script_path = os.path.abspath(cmd)
                if script_path.startswith(shell_root) and os.path.isfile(script_path):
                    try:
                        subprocess.run(["bash", script_path] + args)
                    except FileNotFoundError:
                        print("\nbash: command not found.")
                else:
                    print(f"{cmd}: Permission denied or file not found.")
                continue

            if cmd in commands:
                output = run_command(cmd, args)
                if output:
                    print(output, end='')
            elif cmd in extra_commands:
                output = run_command(cmd, args)
                if output:
                    print(output, end='')
            else:
                print(f"{cmd}: command not found")

        except KeyboardInterrupt:
            print("\nExiting shell emulator.")
            break

if __name__ == "__main__":
    main()
