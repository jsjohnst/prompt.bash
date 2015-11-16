from __future__ import print_function
# Python 2 and 3 compatibility: FileNotFoundError in Python 3, IOError in Python 2.
FileNotFoundError = getattr(__builtins__, 'FileNotFoundError', IOError)
input = getattr(__builtins__, 'raw_input', input)

from segment import Segment, theme
import colors, glyphs

try:
    import pygit2
except ImportError:
    pygit2 = None


import socket, os, sys, re, subprocess, getpass, time

class Jobs(Segment):
    bg = colors.background(theme.JOBS_BG)
    fg = colors.foreground(theme.JOBS_FG)

    def init(self):
        pppid = subprocess.Popen(['ps', '-p', str(os.getppid()), '-oppid='],
                                 stdout=subprocess.PIPE).communicate()[0].strip()
        output = subprocess.Popen(['ps', '-a', '-o', 'ppid'],
                                  stdout=subprocess.PIPE).communicate()[0]
        num_jobs = len(re.findall(bytes(pppid), output)) - 1

        self.text = glyphs.HOURGLASS + ' ' + str(num_jobs)

        if not num_jobs:
            self.active = False


class Time(Segment):
    bg = colors.background(theme.TIME_BG)
    fg = colors.foreground(theme.TIME_FG)

    def init(self):
        self.text = glyphs.TIME + ' ' + str(time.strftime("%H:%M:%S"))


class UserAtHost(Segment):
    bg = colors.background(theme.USERATHOST_BG)
    fg = colors.foreground(theme.USERATHOST_FG)

    def init(self):
        self.text = getpass.getuser()

class NewLine(Segment):
    text = '\r\n'


class Root(Segment):
    text = ' '


class Divider(Segment):
    text = glyphs.DIVIDER

    def set_colors(self, prev, next):
        self.bg = next.bg if next and next.bg else Padding.bg
        self.fg = prev.bg if prev and prev.bg else Padding.bg
        self.fg = self.fg.replace('setab', 'setaf')


class ExitCode(Segment):
    bg = colors.background(theme.EXITCODE_BG)
    fg = colors.foreground(theme.EXITCODE_FG)

    def init(self):
        self.text = str(sys.argv[1])

        if sys.argv[1] == '0':
            self.active = False


class Padding(Segment):
    bg = colors.background(theme.PADDING_BG)

    def init(self, amount):
        self.text = ''.ljust(amount)


class CurrentDir(Segment):
    bg = colors.background(theme.CURRENTDIR_BG)
    fg = colors.foreground(theme.CURRENTDIR_FG)

    def init(self, cwd):
        home = os.path.expanduser('~')
        self.text = self.shorten(cwd.replace(home, '~'))

    def shorten(self, cwd, ellipsis='...', dir_shorten_len=3, dir_limit_depth=4):
        cwd_split = cwd.split(os.sep)
        cwd_split_len = len(cwd_split)

        cwd = [i[0:dir_shorten_len] if dir_shorten_len and i else i for i in cwd_split[:-1]] + [cwd_split[-1]]

        if dir_limit_depth and cwd_split_len > dir_limit_depth + 1:
            del(cwd[0:-dir_limit_depth])
            if ellipsis is not None:
                cwd.insert(0, ellipsis)

        return os.sep.join(cwd)


class ReadOnly(Segment):
    bg = colors.background(theme.READONLY_BG)
    fg = colors.foreground(theme.READONLY_FG)

    def init(self, cwd):
        self.text = glyphs.WRITE_ONLY

        if os.access(cwd, os.W_OK):
            self.active = False


class Venv(Segment):
    bg = colors.background(theme.VENV_BG)
    fg = colors.foreground(theme.VENV_FG)

    def init(self):
        env = os.getenv('VIRTUAL_ENV')
        if env is None:
            self.active = False
            return

        env_name = os.path.basename(env)
        self.text = glyphs.VIRTUAL_ENV + ' ' + env_name

class Ssh(Segment):
    bg = colors.background(theme.SSH_BG)
    fg = colors.foreground(theme.SSH_FG) + colors.bold()

    def init(self):
        self.text = 'SSH: ' + socket.gethostname().replace('.local', '')

        if not os.getenv('SSH_CLIENT'):
            self.active = False

class Git(Segment):
    def init(self):
        if pygit2 is None:
            self.text = glyphs.BRANCH + ' ' + glyphs.WRITE_ONLY
            self.bg = colors.background(colors.RED)
            self.fg = colors.foreground(colors.WHITE)
            return

        try:
            repo_path = pygit2.discover_repository(os.getcwd())
            self.repo = pygit2.Repository(repo_path)
        except Exception:
            self.active = False
            return

        branch_name = self.get_branch_name()

        if not branch_name:
            self.active = False
            return

        git_colors = self.get_working_dir_status_decorations()
        self.bg = colors.background(git_colors[0])
        self.fg = colors.foreground(git_colors[1])

        current_commit_text = self.get_current_commit_decoration_text()
        self.text = (glyphs.BRANCH + ' ' + branch_name + ' ' + current_commit_text).strip()

    def get_branch_name(self):
        try:
            if self.repo.head_is_detached:
                return '(Detached: %s)' % (str(self.repo.head.target)[:8] + '...')
            else:
                return self.repo.head.shorthand.strip()

        except Exception:
            return None

    def get_working_dir_status_decorations(self):
        # Working directory statuses:
        UNTRACKED_FILES = 0
        CHANGES_NOT_STAGED = 1
        ALL_CHANGES_STAGED = 2
        CLEAN = 3
        CONFLICT = 4
        UNKNOWN = 5

        # Statuses vs colors:
        STATUSES_COLORS = {
            #STATUS: (bg_col, fg_col),
            UNTRACKED_FILES: (theme.GIT_UNTRACKED_FILES_BG, theme.GIT_UNTRACKED_FILES_FG),
            CHANGES_NOT_STAGED: (theme.GIT_CHANGES_NOT_STAGED_BG, theme.GIT_CHANGES_NOT_STAGED_FG),
            ALL_CHANGES_STAGED: (theme.GIT_ALL_CHANGES_STAGED_BG, theme.GIT_ALL_CHANGES_STAGED_FG),
            CLEAN: (theme.GIT_CLEAN_BG, theme.GIT_CLEAN_FG),
            CONFLICT: (theme.GIT_CONFLICT_BG, theme.GIT_CONFLICT_FG),
            UNKNOWN: (colors.RED, colors.WHITE),
        }

        is_clean = True
        has_conflicted = False
        has_untracked = False
        has_unstaged = False
        has_staged = False

        try:
            for file_name, status in self.repo.status().items():
                if status & pygit2.GIT_STATUS_IGNORED:
                    continue

                elif status & pygit2.GIT_STATUS_CONFLICTED:
                    has_conflicted = True
                    is_clean = False

                elif status & pygit2.GIT_STATUS_WT_NEW:
                    has_untracked = True
                    is_clean = False

                elif status & pygit2.GIT_STATUS_WT_MODIFIED or status & pygit2.GIT_STATUS_WT_DELETED:
                    has_unstaged = True
                    is_clean = False

                elif status & pygit2.GIT_STATUS_INDEX_DELETED or \
                     status & pygit2.GIT_STATUS_INDEX_NEW or \
                     status & pygit2.GIT_STATUS_INDEX_MODIFIED:
                    has_staged = True
                    is_clean = False

        except Exception:
            return STATUSES_COLORS[UNKNOWN]

        if has_conflicted:
            return STATUSES_COLORS[CONFLICT]

        if has_untracked:
            return STATUSES_COLORS[UNTRACKED_FILES]

        if has_unstaged:
            return STATUSES_COLORS[CHANGES_NOT_STAGED]

        if has_staged:
            return STATUSES_COLORS[ALL_CHANGES_STAGED]

        if is_clean:
            return STATUSES_COLORS[CLEAN]

        return STATUSES_COLORS[UNKNOWN]

    def get_current_commit_decoration_text(self):
        try:
            ret = ''

            branch = self.repo.lookup_branch(self.repo.head.shorthand)

            if not branch.upstream:
                return ret

            ahead, behind = self.repo.ahead_behind(branch.target, branch.upstream.target)

            if ahead:
                amount_ahead = getattr(glyphs, 'N{}'.format(ahead)) if int(ahead) <= 10 else ahead
                ret = amount_ahead + glyphs.RIGHT_ARROW

            if behind:
                amount_behind = getattr(glyphs, 'N{}'.format(behind)) if int(behind) <= 10 else behind
                ret += ' ' + glyphs.LEFT_ARROW + amount_behind

            return ret.strip()

        except Exception:
            return ''

