import itertools

DEFAULT_MARKER_CYCLE = ('o', 'd', '+', '^', 's', 'v', 'h', 'p', '*', 'D', 'x')

EXTRA_LINESTYLES = {
    'loose dotted': (0, (1, 10)),
    'dense dotted': (0, (1, 1)),

    'loosely dashed': (0, (5, 5)),
    'very loosely dashed': (0, (5, 10)),
    'dense dashed': (0, (5, 1)),

    'dashdotdot': (0, (3, 5, 1, 5, 1, 5)),

    'dense dashdot': (0, (3, 1, 1, 1)),
    'dense dashdotdot': (0, (3, 1, 1, 1, 1, 1)),
}

DEFAULT_LINE_CYCLE = (
    'solid', 'dashed', 'dotted',
    EXTRA_LINESTYLES['dense dashdot'],
    EXTRA_LINESTYLES['loosely dashed'],
    EXTRA_LINESTYLES['dense dashdotdot'],
    EXTRA_LINESTYLES['dense dotted'],
    'dashdot',
    EXTRA_LINESTYLES['very loosely dashed'],
)
DEFAULT_COLOR_CYCLE = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
]

BROWNS = [
    '#ff7f00', '#fdbf6f', '#1f78b4', '#e31a1c', '#b15928',
    '#6a3d9a', '#fb9a99', '#cab2d6', '#a6cee3'
]


def get_marker_cycler(markers=DEFAULT_MARKER_CYCLE):
    return itertools.cycle(markers)


def get_line_cycler(lines=DEFAULT_LINE_CYCLE):
    return itertools.cycle(lines)


def get_color_cycler(colors=DEFAULT_COLOR_CYCLE):
    return itertools.cycle(colors)
