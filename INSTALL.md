Installation
============

Requirements
------------
- **Mac OS X** or **Linux**.
prompt.bash is mainly developed for Mac OS X but it works smoothly under Linux too.
- **Python 2.7+**
- A terminal emulator with support for
[**ANSI colors**](http://en.wikipedia.org/wiki/ANSI_escape_code).
Most terminal emulators works out of the box, in particular:
    - [*Terminal*](http://en.wikipedia.org/wiki/Terminal_\(OS_X\)), the default terminal emulator
    in Mac OS X;
    - [*iTerm2*](http://iterm2.com), the app for Mac OS X;
    - [*GNOME Terminal*](http://en.wikipedia.org/wiki/GNOME_Terminal), the default terminal emulator
    in Ubuntu.

  For others, like [*Konsole*](http://en.wikipedia.org/wiki/Konsole) the default terminal emulator
for KDE, the right `TERM` type might be required in order to activate colors. If this is the case,
check the `TERM` type with `echo $TERM` and if the output differs from `xterm-256color`, then
add the following line to `~/.bashrc`:

  `export TERM='xterm-256color'`
- `pygit2` for better native python git support
- **Patched fonts** for better-looking glyphs.
Install patched [powerline-fonts](https://github.com/Lokaltog/powerline-fonts) and set the
terminal to use them. My favorite is
[DejaVu Sans Mono for Powerline](https://github.com/powerline/fonts/tree/master/DejaVuSansMono).

Steps
-----
1. Clone this repository:

        git clone https://github.com/jsjohnst/prompt.bash.git
2. Run:

        ./install.py
3. *Optional* - Edit the file `prompt.py`, in particular:
    - set `CURRENT_THEME` to your favorite theme or create a new one copying one of the existent themes;
4. Logout and login again in the shell to see the new prompt!
