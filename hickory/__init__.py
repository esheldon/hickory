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
    MultiCycler,
    get_default_multi_cycler,
    get_marker_cycler,
    get_linestyle_cycler,
    get_color_cycler,
    DEFAULT_MARKERS,
    DEFAULT_LINESTYLES,
    DEFAULT_COLORS,
)

from .constants import GOLDEN_ARATIO

from . import axes
from . import formatters
