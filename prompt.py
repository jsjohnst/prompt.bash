#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

import segments as segs

# Python 2 and 3 compatibility: FileNotFoundError in Python 3, IOError in Python 2.
FileNotFoundError = getattr(__builtins__, 'FileNotFoundError', IOError)


# Python 2 and 3 compatibility: `sys.stdout.buffer.write` in Python 3, `sys.stdout.write`
# in Python 2.
try:
    write = sys.stdout.buffer.write
except AttributeError:
    write = sys.stdout.write


class Prompt:
    def __init__(self):
        self.cwd = os.getenv('PWD')

        self.first_line_left = []

    def render(self):
        """
        Render the prompt with the appropriate syntax.
        """
        # Remove inactive segments and duplicated Dividers.
        self._clean_segments()

        # Render first line.
        first_line = self._render_first_line()

        # Return the entire prompt.
        return first_line.encode('utf-8')

    def _render_first_line(self):
        # List of segments for the first line (left part, padding, right part).
        # Add left part segments.
        segments = self.first_line_left

        # Color the dividers.
        segments = self._color_dividers(segments)

        # Render the resulting segments.
        output = ''
        for segment in segments:
            output += segment.render()
        return output

    def _clean_segments(self):
        """
        Remove inactive segments.
        F.i. the job segment is inactive when there is no job.
        """
        def remove_inactive(segments):
            return [x for x in segments if x.active]

        def remove_duplicated_dividers(segments):
            # Collect in a list all indexes of elements in `segments` which must be removed ('cause
            # they are duplicated dividers).
            to_remove = []
            for i in range(len(segments)-1):
                if isinstance(segments[i], segs.Divider) and isinstance(segments[i+1], segs.Divider):
                    to_remove.append(i)

            # Remove from segments the collected indexes.
            for counter, i in enumerate(to_remove):
                segments.pop(i - counter)
            return segments

        def strip():
            # Remove initial Divider, if any.
            if self.first_line_left and isinstance(self.first_line_left[0], segs.Divider):
                self.first_line_left.pop(0)

        self.first_line_left = remove_duplicated_dividers(remove_inactive(self.first_line_left))
        strip()

    @staticmethod
    def _get_total_segments_length(segments):
        return sum([x.length() for x in segments])

    @staticmethod
    def _color_dividers(segments):
        for i, segment in enumerate(segments):
            # We need to color a divider based on the colors of the previous and next segments.
            if isinstance(segment, segs.Divider):
                prev = segments[i-1] if i > 0 else None
                next_ = segments[i+1] if i+1 < len(segments) else None
                segment.set_colors(prev, next_)
        return segments


if __name__ == '__main__':
    prompt = Prompt()

    # First line left (order: left to right).
    prompt.first_line_left.append(segs.Ssh())
    prompt.first_line_left.append(segs.Divider())
    prompt.first_line_left.append(segs.UserAtHost())
    prompt.first_line_left.append(segs.Divider())
    prompt.first_line_left.append(segs.Git())
    prompt.first_line_left.append(segs.Divider())
    prompt.first_line_left.append(segs.Venv())
    prompt.first_line_left.append(segs.Divider())
    prompt.first_line_left.append(segs.CurrentDir(prompt.cwd))
    prompt.first_line_left.append(segs.Divider())
    prompt.first_line_left.append(segs.ReadOnly(prompt.cwd))
    prompt.first_line_left.append(segs.Divider())
    prompt.first_line_left.append(segs.ExitCode())
    prompt.first_line_left.append(segs.Divider())
    prompt.first_line_left.append(segs.Root())

    write(prompt.render())

