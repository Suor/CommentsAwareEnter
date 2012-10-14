import re
import sublime, sublime_plugin

def parse(desc):
    rules = [map(str.strip, line.split('=>')) for line in desc.strip().splitlines()]
    return dict((lang, delim) for langs, delim in rules
                              for lang in langs.split())

# Add your languages here
LINE_COMMENTS = parse("""
    python perl ruby bash coffescript => #
    javascript json c c++ java php    => //
    clojure                           => ;
    sql                               => --
""")

class CommentsAwareEnterCommand(sublime_plugin.TextCommand):
    """
    Context aware Enter handler.

    Preserves line comments scope (by adding escaping chars as needed)
    and auto indents in comments.
    """
    def run(self, edit):
        if self.source() in LINE_COMMENTS:
            delim = LINE_COMMENTS[self.source()]
            line = self.line_str()

            start, _, end = line.partition(delim)
            start = re.sub(r'\S', ' ', start)
            end = re.search(r'^\s*', end).group()

            self.view.insert(edit, self.cursor_pos(), '\n' + start + delim + end)
        else:
            self.view.run_command('insert', {'characters': "\n"})

    def cursor_pos(self):
        return self.view.sel()[0].begin()

    def scope_name(self):
        return self.view.scope_name(self.cursor_pos())

    def parsed_scope(self):
        return parse_scope(self.scope_name())

    def source(self):
        return first(vec[1] for vec in self.parsed_scope() if vec[0] == 'source')

    def line_str(self):
        return self.view.substr(self.view.line(self.cursor_pos()))


def parse_scope(scope_name):
    return [name.split('.') for name in scope_name.split()]

def first(coll):
    return next(coll, None)
