import copy
import itertools

DEFAULT_MARKERS = ('o', 'd', '^', 's', 'v', 'h', 'p', 'P', 'H', 'X')

EXTRA_LINESTYLES = {
    'loose dotted': (0, (1, 10)),
    'dense dotted': (0, (1, 1)),

    'loose dashed': (0, (5, 5)),
    'very loose dashed': (0, (5, 10)),
    'dense dashed': (0, (5, 1)),

    'dashdotdot': (0, (3, 5, 1, 5, 1, 5)),

    'dense dashdot': (0, (3, 1, 1, 1)),
    'dense dashdotdot': (0, (3, 1, 1, 1, 1, 1)),
}

DEFAULT_LINESTYLES = (
    'solid', 'dashed', 'dotted',
    EXTRA_LINESTYLES['dense dashdot'],
    EXTRA_LINESTYLES['loose dashed'],
    EXTRA_LINESTYLES['dense dashdotdot'],
    EXTRA_LINESTYLES['dense dotted'],
    'dashdot',
    EXTRA_LINESTYLES['very loose dashed'],
    EXTRA_LINESTYLES['dense dashed'],
)
DEFAULT_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
]

BROWNS = [
    '#ff7f00', '#fdbf6f', '#1f78b4', '#e31a1c', '#b15928',
    '#6a3d9a', '#fb9a99', '#cab2d6', '#a6cee3'
]


class MultiCycler(object):
    def __init__(self, **kw):
        self._cycles = {}

        for key, cyc in kw.items():
            if hasattr(cyc, '__next__'):
                self._cycles[key] = cyc
            else:
                self._cycles[key] = itertools.cycle(cyc)

    def next(self, type):
        if type not in self._cycles:
            raise ValueError("unknown cycle: '%s'" % type)

        return next(self._cycles[type])


def get_default_multi_cycler():
    return MultiCycler(
        marker=get_marker_cycler(),
        linestyle=get_linestyle_cycler(),
        color=get_color_cycler(),
    )


def get_marker_cycler(markers=DEFAULT_MARKERS):
    return itertools.cycle(markers)


def get_linestyle_cycler(linestyles=DEFAULT_LINESTYLES):
    return itertools.cycle(linestyles)


def get_color_cycler(colors=DEFAULT_COLORS):
    return itertools.cycle(colors)
