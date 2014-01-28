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
        delim = COMMENT_STYLES.get(self.comment_style())
        line = self.line_start_str()

        if delim and delim in line:
            start, delim, end = re.split(r'(%s+)' % re.escape(delim), line, 1)
            start = re.sub(r'\S', ' ', start)
            end = re.search(r'^\s*([A-Z]+:)?\s*', end).group()
            end = ' ' * len(end)

            self.view.insert(edit, self.cursor_pos(), '\n' + start + delim + end)
        else:
            self.view.run_command('insert', {'characters': "\n"})

    def cursor_pos(self):
        return self.view.sel()[0].begin()

    def scope_name(self):
        return self.view.scope_name(self.cursor_pos())

    def parsed_scope(self):
        return parse_scope(self.scope_name())

    def comment_style(self):
        return first(vec[2] for vec in self.parsed_scope() if vec[:2] == ['comment', 'line'])

    def line_start(self):
        line = self.view.line(self.cursor_pos())
        return sublime.Region(line.begin(), self.cursor_pos())

    def line_start_str(self):
        return self.view.substr(self.line_start())


def parse_scope(scope_name):
    return [name.split('.') for name in scope_name.split()]

def first(seq):
    return next(iter(seq), None)
