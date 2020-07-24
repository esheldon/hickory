# flake8: noqa

from .convenience import plot, plot_hist

from .plot_containers import Plot, Table
from .legend import Legend

from .colors import (
    get_color,
    get_random_colors,
    COLORS,
    COLOR_VALS,
)

from .cyclers import (
    get_marker_cycler,
    get_linestyle_cycler,
    get_color_cycler,
    DEFAULT_MARKER_CYCLE,
    DEFAULT_LINE_CYCLE,
    DEFAULT_COLOR_CYCLE,
)

from .constants import GOLDEN_ARATIO

from . import axes
from . import formatters
