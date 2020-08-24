# emu

Emu is a web-based terminal emulator designed to allow for educational interactions with command-line interfaces and POSIX shell commands in a safe environment (i.e. zero risk of deleting `/bin/`). This repo demonstrates its functions with a core set of Hadoop File System (HDFS) commands, allowing the user to practice executing them without the lag that comes with running HDFS on a personal computer.

## Requirements

* Python v3.6 or higher (for f-strings and type hints)
* An up-to-date browser, eg Firefox 79.0 or Chrome 84.0

## Local set-up

`*`Commands provided here presume a POSIX shell like bash or zshell, but alternative systems (eg Powershell) can substitute their own commands.

Create a local clone of the repository and navigate to its root folder:

```shell
git clone https://github.com/jsstevenson/emu.git
cd emu
```

Create and start a new virtual environment, and install requirements from `requirements.txt` (venv and PIP commands shown here)

```shell
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Initialize Flask environmental variable(s) and database

```shell
export FLASK_APP=emu
flask init-db

# optional: turn on reload on internal changes
export FLASK_ENV=development
```

Start the Flask server process

```shell
flask run
```

Finally, navigate to 127.0.0.1:5000/app in a web browser.

## Functionality

At present, available commands are limited. The user can enter `help` at the in-app shell prompt to see a full list.

In addition to shell commands, users can press the up- and down-arrow keys, as in a bash or zshell terminal, to traverse their command history.
