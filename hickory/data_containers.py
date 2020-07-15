import numpy as np
from .colors import get_color


class Points(object):
    def __init__(
        self,
        x, y, xerr=None, yerr=None,
        marker='o',
        size=None,
        linestyle=None,
        linewidth=None,
        color=None,
        edgecolor=None,
        edgewidth=None,
        alpha=None,
        capsize=2,
    ):

        self._set_points(x, y, xerr, yerr)
        self.marker = marker
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.color = color
        self.edgecolor = edgecolor
        self.edgewidth = edgewidth
        self.size = size
        self.alpha = alpha

        self.capsize = capsize

    def _set_points(self, x, y, xerr, yerr):
        self.x = _make_array_maybe(x)
        self.y = _make_array_maybe(y)
        self.xerr = _make_array_maybe(xerr)
        self.yerr = _make_array_maybe(yerr)

        if self.x.size != self.y.size:
            raise ValueError(
                "x and y must be same "
                "size, got %d and %d" % (self.x.size, self.y.size)
            )

        if self.xerr is not None and self.x.size != self.xerr.size:
            raise ValueError(
                "x and xerr must be same "
                "size, got %d and %d" % (self.x.size, self.xerr.size)
            )
        if self.yerr is not None and self.y.size != self.yerr.size:
            raise ValueError(
                "y and yerr must be same "
                "size, got %d and %d" % (self.y.size, self.yerr.size)
            )

    def _add_to_axes(self, ax):

        color = None if self.color is None else get_color(self.color)

        linestyle = 'none' if self.linestyle is None else self.linestyle
        ax.errorbar(
            self.x, self.y,
            xerr=self.xerr,
            yerr=self.yerr,
            marker=self.marker,
            markersize=self.size,
            linestyle=linestyle,
            linewidth=self.linewidth,
            color=color,
            capsize=self.capsize,
            ecolor=color,
            elinewidth=self.linewidth,
            alpha=self.alpha,
            # zorder=3,
            # barsabove=True,
        )


class Curve(Points):
    """
    Same as Points but defaults to marker None and now support for
    error bars
    """
    def __init__(
        self, x, y,
        linestyle='-',
        linewidth=None,
        color=None,
        alpha=None,
        marker=None,
        size=None,
        edgecolor=None,
        edgewidth=None,
    ):

        super().__init__(
            x, y,
            linestyle=linestyle,
            linewidth=linewidth,
            color=color,
            alpha=alpha,

            marker=marker,
            size=size,
            edgecolor=edgecolor,
            edgewidth=edgewidth,
        )


class HLine(object):
    def __init__(self,
                 y=0,
                 xmin=0, xmax=1,
                 linestyle='-', linewidth=None,
                 color=None,
                 alpha=None):
        self.y = y
        self.xmin = xmin
        self.xmax = xmax
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.color = color
        self.alpha = alpha

    def _add_to_axes(self, ax):
        color = None if self.color is None else get_color(self.color)
        linestyle = 'none' if self.linestyle is None else self.linestyle
        ax.axhline(
            y=self.y,
            xmin=self.xmin,
            xmax=self.xmax,
            linestyle=linestyle,
            linewidth=self.linewidth,
            color=color,
            alpha=self.alpha,
        )


class VLine(object):
    def __init__(self,
                 x=0,
                 ymin=0, ymax=1,
                 linestyle='-', linewidth=None,
                 color=None,
                 alpha=None):
        self.x = x
        self.ymin = ymin
        self.ymax = ymax
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.color = color
        self.alpha = alpha

    def _add_to_axes(self, ax):
        color = None if self.color is None else get_color(self.color)
        linestyle = 'none' if self.linestyle is None else self.linestyle
        ax.axvline(
            x=self.x,
            ymin=self.ymin,
            ymax=self.ymax,
            linestyle=linestyle,
            linewidth=self.linewidth,
            color=color,
            alpha=self.alpha,
        )


def _make_array_maybe(data):
    if data is None:
        return None
    else:
        return np.array(data, ndmin=1, copy=False)
