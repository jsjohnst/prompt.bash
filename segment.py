import importlib
import colors
from prompt import CURRENT_THEME

theme = importlib.import_module('themes.{}'.format(CURRENT_THEME))

class Segment(object):
    bg = ''  # Default: no color.
    fg = ''  # Default: no color.

    def __init__(self, *args, **kwargs):
        self.active = True
        class_name = type(self).__name__.lower()
        if class_name in ['newline', 'root', 'divider', 'padding']:
            self.pad_text = False
        else:
            self.pad_text = True

        if self.active:
            self.init(*args, **kwargs)

    def init(self):
        pass

    def get_text(self):
        return ' ' + self.text + ' ' if self.pad_text else self.text

    def render(self):
        output = list()
        output.append(self.bg)
        output.append(self.fg)
        output.append(self.get_text())
        output.append(colors.reset() if self.bg or self.fg else '')
        return ''.join(output)

    def length(self):
        return len(self.get_text())
