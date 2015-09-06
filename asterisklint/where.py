# vim: set ts=8 sw=4 sts=4 et ai:


class Where(object):
    def __init__(self, filename, lineno, line):
        self.filename = filename  # shared constant in CPython, so cheap
        self.lineno = lineno
        self.line = line
        self.last_line = False

    def __str__(self):
        return '%s:%d' % (self.filename, self.lineno)