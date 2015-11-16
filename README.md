prompt.bash: a simple but powerful prompt for Bash
======================================

prompt.bash is a flavored **prompt** for [Bash](http://en.wikipedia.org/wiki/Bash_(Unix_shell))
which provides info about the running **system** and **environment** in a fancy **colored** output.
It works under **Mac OS X** and **Linux**.

This project is very heavily inspired by [Promptastic](https://github.com/nimiq/promptastic) which
was in turn heavily inspired by [Powerline](https://github.com/Lokaltog/powerline)
and [Powerline-shell](https://github.com/milkbikis/powerline-shell/). After dealing with nagging issue
after issue with Powerline and it's bloated, messy setup, I went looking for alternatives. I then found
[vim-airline](https://github.com/bling/vim-airline) which perfectly fits the bill for my Vim needs, but still needed something for Bash.
Promptastic was a very close fit and quite fast, but I wanted something even more simple, so this project was born.
It cuts out the multi-line and left/right side prompt functionality and adds a few nice features from Powerline.
It also improves upon Promptastic/Powerline's git functionality making it significantly easier (in the case of Powerline) to follow the code
and it also is faster / more stable to boot.

Features
--------
- shows the name of the logged user, the current directory path (intelligently truncated similar to Powerline);
- provides a feedback if the current directory is read-only or is not a valid path;
- warns if the last command exited with a failure code and includes the exit code;
- displays the number of active jobs;
- reveals the name of the active Python [virtualenv](https://github.com/pypa/virtualenv)
environment;
- presents details about the current Git branch and the status of the staging area and commit;
- adds a special label in case of SSH connection with the hostname;
- colored output: there are a bunch of themes to choose from and new themes can be easily created;
- simple and automatic [installation procedure](https://github.com/nimiq/promptastic/blob/master/INSTALL.md);
- written in Python.

Requirements
------------
Python `pygit2` package installed

Installation
------------
See [INSTALL.md](https://github.com/nimiq/promptastic/blob/master/INSTALL.md).
