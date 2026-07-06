
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

git clone [https://github.com/YOUR-USERNAME/pyash.git](https://github.com/YOUR-USERNAME/pyash.git)
cd pyash
python pyash.py

```

##  📄 License
Distributed under the MIT License. See LICENSE for more information. This grants you full rights to use, modify, study, and distribute this codebase in both private and commercial environments.
