# flake8: noqa

from .convenience import plot, plot_hist

from . import plot_containers
from .plot_containers import Plot, Table

# from .data_containers import Points, Curve, HLine, VLine
# from . import data_containers

from .legend import Legend

from . import colors
from .colors import (
    get_color,
    get_random_colors,
    COLORS,
    COLOR_VALS,
)

from . import cyclers
from .cyclers import (
    get_marker_cycler,
    get_line_cycler,
    get_color_cycler,
    DEFAULT_MARKER_CYCLE,
    DEFAULT_LINE_CYCLE,
    DEFAULT_COLOR_CYCLE,
)
