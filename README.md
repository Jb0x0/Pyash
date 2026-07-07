
# 🐍🐚 Pyash (Unix Shell Emulator)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Pyash** is a feature-rich, highly portable, and deeply customizable Unix shell emulator coded entirely in clean modular Python. Designed primarily as a secure sandbox environment, Pyash restricts file operations strictly to a designated "shell" folder, preventing directory traversal and protecting your host machine. 

Whether you are looking for an educational tool to study shell or Python mechanics, a safe terminal environment for a Capture The Flag (CTF) game, or just a fun text-based interface to play with, Pyash delivers a native-feeling terminal experience right in your Python runtime.

---

##  Features

*  **Secure Sandbox Environment:** Pyash operates fully in a sandboxed "shell" folder, Pyash specifically leverages `os.path.commonpath` to ensure users absolutely cannot read, write, or navigate to files outside the designated "shell" root folder.
  
*  **Command Chaining (`&&`):** Supports sequential execution and if a command fails, the chain safely halts.
  
*  **Stream Piping (`|`):** Custom text-stream pipeline architecture allows you to seamlessly pass data across utilities (e.g., `cat file.txt | head`).
  
*  **Colored Output and Output History:** Built-in persistent history (.pyash_history) and crisp terminal color coding powered by `colorama`.

*  **Support for Extra Commands:** More commands can easily be added by modifying the .pyash_extras file that Pyash creates in its "shell" folder
  
*  **Battery-Included Utilities:** Native Python rewrites of classic coreutils:
   * *Navigation & Files:* `cd`, `pwd`, `ls (-a, -l)`, `mkdir`, `rmdir`, `rm`, `touch`, `cp`, `mv`
   * *Text Processing:* `cat`, `head`, `tail`, `echo` (with `>` and `>>` redirection support)
   * *System & Info:* `uname`, `uptime`, `whoami`, `date`, `tree`, `chmod`
   * *Extras:* `fortune`, `dd`, and a localized `man` paging system.


Read INSTRUCTIONS.txt for more info.

---

##  Prerequisites

Pyash only works on Unix based Operating Systems (so Linux, BSD, MacOS, etc).

Pyash relies primarily on the Python Standard Library. You only need to install `colorama` for terminal colors:

```bash
pip install colorama
```
```bash
git clone https://github.com/Jb0x0/Pyash.git
cd Pyash/pyash
python3 Pyash.py

```
---

##   License
Distributed under the MIT License. See LICENSE for more information. This grants you full rights to use, modify, study, and distribute this codebase in both private and commercial environments.
