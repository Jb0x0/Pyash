
# 🐚 Pyash (Shell Emulator)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Pyash** is a feature-rich, highly portable, and deeply customized Unix shell emulator coded entirely in Python. Designed primarily as a secure sandbox environment, Pyash restricts file operations strictly to a designated "shell folder," preventing directory traversal and protecting your host machine. 

Whether you are looking for an educational tool to study shell mechanics, a safe terminal environment for a Capture The Flag (CTF) game, or just a fun text-based interface to play with, Pyash delivers a native-feeling terminal experience right in your Python runtime.

---

##  Features

*  **Secure Sandbox Environment:** Leverages `os.path.commonpath` to ensure users absolutely cannot read, write, or navigate to files outside the designated shell root folder.
*  **Command Chaining (`&&`):** Supports sequential execution—if a command fails, the chain safely halts.
*  **Stream Piping (`|`):** Custom text-stream pipeline architecture allows you to seamlessly pass data across utilities (e.g., `cat file.txt | head`).
*  **Beautiful UI & History:** Built-in persistent history (with cross-platform GNU readline fallbacks) and crisp terminal color coding powered by `colorama`.
*  **Battery-Included Utilities:** Native Python rewrites of classic coreutils:
  * *Navigation & Files:* `cd`, `pwd`, `ls (-a, -l)`, `mkdir`, `rmdir`, `rm`, `touch`, `cp`, `mv`
  * *Text Processing:* `cat`, `head`, `tail`, `echo` (with `>` and `>>` redirection support)
  * *System & Info:* `uname`, `uptime`, `whoami`, `date`, `tree`, `chmod`
  * *Extras:* `fortune`, `dd`, and a localized `man` paging system.

---

##  Getting Started

### Prerequisites

Pyash relies primarily on the Python Standard Library. You only need to install `colorama` for terminal colors:

```bash
pip install colorama
Running the Shell
Simply clone this repository and run the Python script:

Bash
git clone [https://github.com/YOUR-USERNAME/pyash.git](https://github.com/YOUR-USERNAME/pyash.git)
cd pyash
python pyash.py
On your first launch, the interactive Setup Wizard will ask you to select or create a dedicated workspace folder. This folder will act as the root (~) for your sandboxed session.

🛠️ System Architecture
Pyash processes strings in memory to simulate low-level OS behaviors safely:

[ User Input ] ──> [ shlex Tokenizer ] ──> [ Chaining/Piping Parser ]
                                                       │
                                            ┌──────────┴──────────┐
                                            ▼                     ▼
                                    [ Built-in Logic ]     [ safe_path Check ]
                                   (cat, ls, echo...)      (Strict Jail Validation)
The safe_path Sandbox Shield
Our path validation routine guarantees that even if a user tries to use directory traversal loops like cd ../../../../, the shell dynamically catches it and throws a permission denial:

Python
# Core sandboxing mechanism used in Pyash
candidate = os.path.abspath(os.path.join(os.getcwd(), os.path.expanduser(target_str)))
root_real = os.path.realpath(shell_root)
resolved_target = os.path.realpath(candidate)

if os.path.commonpath([root_real, resolved_target]) != root_real:
    raise PermissionError("Access denied: Outside sandbox.")
🎛️ Advanced Usage & Testing
The run Debugging Utility
For debugging purposes, an un-sandboxed run command is packed into the engine. It allows execution of raw host shell commands.

⚠️ Security Warning: The run command is explicitly locked by default to maintain the sandbox integrity. To unlock it for localized testing, you must explicitly read its documentation by executing man run inside the emulator.

Extending Commands (.pyash_extras)
You can append custom host binaries directly into the shell interface by listing them in the .pyash_extras configuration file generated inside your shell root.

🤝 Contributing
Pyash is fully open-source and highly modular! If you want to study how it works or add your own custom features, contributions are completely welcome.

Ideas for contributions:

Building a native grep string matching utility.

Implementing environment variable tracking (export KEY=VALUE).

Creating a tiny, sandboxed Python text editor (like a mini nano or vi).

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information. This grants you full rights to use, modify, study, and distribute this codebase in both private and commercial environments.
