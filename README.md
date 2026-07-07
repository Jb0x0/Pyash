
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

*  **Support for Extra Commands:** More commands can easily be added by modifying the ".pyash_extras" file that Pyash creates in its "shell" folder
  
*  **Battery-Included Utilities:** Native Python rewrites of classic coreutils:
  
    | Navigation & Files | Description |
    |---------|-------------|
    | `cd <directory>` | Change the current directory |
    | `pwd` | Display the current working directory |
    | `ls (-a, -l)` | List files in the current directory |
    | `mkdir` | Creates a new directory (folder) |
    | `rmdir <directory>` | Removes an empty directory |
    | `rm` | Deletes files or directories |
    | `touch` | Creates a new empty file or changes a file |
    | `cp` | Copies files or directories |
    | `mv` | Moves or renames files or directories |

    | Text Processing | Description |
    |---------|-------------|
    | `cat` | Displays the contents of a file |
    | `head` | Shows the first lines of a file |
    | `tail` | Shows the last lines of a file |
    | `echo (>, >>)` | Prints text to the terminal |

    | System & Info | Description |
    |---------|-------------|
    | `uname` | Displays system information |
    | `uptime` | Shows how long the system has been running |
    | `whoami` | Shows the current user |
    | `date` | Displays the current date and time |
    | `tree` | Displays files and directories in a tree |
    | `chmod` | Changes file permissions |
    | `history` | Show previously executed commands |
    | `exit` | Exit the shell |

    | Extras | Description |
    |---------|-------------|
    | `fortune` | Displays a random quote or message |
    | `dd` | Copies or transforms data at a low level |
    | `man` | A localized manual paging system |
   

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
