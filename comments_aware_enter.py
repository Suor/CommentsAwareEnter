import re
import sublime, sublime_plugin


COMMENT_STYLES = {
    'number-sign'  : '#',
    'double-slash' : '//',
    'double-dash'  : '--',
    'semicolon'    : ';',
    'percentage'   : '%',
    'erlang'       : '%',
}


class CommentsAwareEnterCommand(sublime_plugin.TextCommand):
    """
    Context aware Enter handler.

    Preserves line comments scope (by adding escaping chars as needed)
    and auto indents in comments.
    """
    def run(self, edit):
        for region in reversed(self.view.sel()):
            pos = region.end()
            delim = COMMENT_STYLES.get(comment_style(self.view, pos))
            line = line_start_str(self.view, pos)

            if delim and delim in line:
                start, delim, end = re.split(r'(%s+)' % re.escape(delim), line, 1)
                start = re.sub(r'\S', ' ', start)
                end = re.search(r'^\s*([A-Z]+:|-)?\s*', end).group()
                if '-' not in end:
                    end = ' ' * len(end)
                replacement = "\n" + start + delim + end
            else:
                replacement = "\n"

            self.view.erase(edit, region)
            self.view.insert(edit, region.begin(), replacement)


class CommentsAwareJoinLinesCommand(sublime_plugin.TextCommand):
    """
    Context aware join lines.

    Removes comment marker and extraneous space.
    """
    def run(self, edit):
        for region in reversed(self.view.sel()):
            pos = region.end()
            delim = COMMENT_STYLES.get(comment_style(self.view, pos))
            next_line = line_f(self.view, pos)
            next_line_str = self.view.substr(next_line)

            if delim and delim in next_line_str:
                start, _, end = re.split(r'(%s+)' % re.escape(delim), next_line_str, 1)
                if not start or start.isspace():
                    next_line = sublime.Region(next_line.a - 1, next_line.b)
                    end = re.sub(r'^\s+', ' ', end)
                    self.view.replace(edit, next_line, end)
                    return

            self.view.run_command('join_lines')


### View tools

def line_start(view, pos):
    line = view.line(pos)
    return sublime.Region(line.begin(), pos)

def line_start_str(view, pos):
    return view.substr(line_start(view, pos))

def line_f(view, pos):
    return view.line(newline_f(view, pos))

if sublime.version() >= '3000':
    def newline_f(view, pos):
        return view.find_by_class(pos, True, sublime.CLASS_LINE_START)
else:
    def newline_f(view, pos):
        region = view.find(r'^', pos + 1)
        return region.end()


### Scopes

def comment_style(view, pos):
    parsed_scope = parse_scope(scope_name(view, pos))
    return first(vec[2] for vec in parsed_scope if vec[:2] == ['comment', 'line'])

def scope_name(view, pos):
    return view.scope_name(pos)

def parse_scope(scope_name):
    return [name.split('.') for name in scope_name.split()]


### funcy

def first(seq):
    return next(iter(seq), None)

def isa(*types):
    return lambda x: isinstance(x, types)

from collections import Iterable
iterable = isa(Iterable)
