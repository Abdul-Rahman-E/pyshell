# PyShell – Custom Python Shell

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)

**PyShell** is a fully functional, Python-based command-line shell that emulates core Unix/Linux shell functionality. It is designed for learning, experimentation, and demonstrating systems programming concepts in Python.

---

## Features

- **Built-in commands**:
  - `cd` – change directories
  - `pwd` – display current directory
  - `echo` – print messages
  - `type` – show command type or path
  - `exit` – terminate the shell
- **External command execution**:
  - Execute system commands using Python’s `subprocess` module
  - Full support for PATH resolution and error handling
- **Advanced I/O redirection**:
  - Redirect stdout and stderr to files
  - Support for `>`, `>>`, `1>`, `1>>`, `2>`, `2>>`
- **Dynamic command parsing**:
  - Uses `shlex` to handle quoted arguments safely
- **Interactive shell prompt**:
  - Mimics real shell behavior with `$` prompt
- **Robust error handling**:
  - Gracefully handles invalid commands, missing files, and exceptions

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/pyshell.git
cd pyshell
```

Run the shell:

```bash
python pyshell.py
```

---

## Usage

```bash
$ echo Hello World
Hello World

$ pwd
/home/user

$ cd /tmp
$ pwd
/tmp

$ ls -l
total 0
-rw-r--r-- 1 user user 0 Jan 12 10:00 file.txt

$ echo "This is a test" > output.txt
$ type ls
ls is /bin/ls

$ exit
```

**Supports stdout and stderr redirection:**

```bash
$ echo "Hello" >> output.txt
$ ls non_existent_file 2> errors.txt
```

---

## Technical Highlights

- Implemented in **Python 3** using:

  - `os` – for directory and environment management
  - `subprocess` – for executing external commands
  - `shlex` – for parsing complex commands

- Demonstrates:

  - Systems programming concepts
  - Command parsing and dispatch
  - Process and file descriptor management

- Modular design allows easy extension of built-in commands and features

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
