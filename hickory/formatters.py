import matplotlib


class HickoryScalarFormatter(matplotlib.ticker.ScalarFormatter):
    """
    tick formatter for linear axes

    Removes mathdefault from format strings
    """
    def _set_format(self):
        super()._set_format()

        if 'mathdefault' in self.format:
            self.format = _remove_mathdefault(self.format)


class HickoryLogFormatter(matplotlib.ticker.LogFormatterSciNotation):
    """
    tick formatter for log axes

    Removes mathdefault from format strings
    """

    def __call__(self, x, pos=None):
        s = super().__call__(x, pos=pos)

        if 'mathdefault' in s:
            s = self.format = _remove_mathdefault(s)

        return s


def _remove_mathdefault(s):
    s = s.replace(r'\mathdefault{', '')
    s = s[0:-2] + '$'
    return s
