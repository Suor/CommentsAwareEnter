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
                end = re.search(r'^\s*([A-Z]+:)?\s*', end).group()
                end = ' ' * len(end)
                replacement = "\n" + start + delim + end
            else:
                replacement = "\n"

            self.view.erase(edit, region)
            self.view.insert(edit, region.begin(), replacement)


### View tools

def line_start(view, pos):
    line = view.line(pos)
    return sublime.Region(line.begin(), pos)

def line_start_str(view, pos):
    return view.substr(line_start(view, pos))


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
