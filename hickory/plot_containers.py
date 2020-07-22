import math
import numpy as np
import matplotlib
import matplotlib.pyplot as mplt
from matplotlib.axes import (
    Axes,
    SubplotBase,
    subplot_class_factory,
)
from numbers import Integral

from .colors import COLORS
from .legend import Legend

DEFAULT_MARKER = 'o'


class _ScalarFormatter(matplotlib.ticker.ScalarFormatter):
    def _set_format(self):
        # set the format string to format all the ticklabels
        if len(self.locs) < 2:
            # Temporarily augment the locations with the axis end points.
            _locs = [*self.locs, *self.axis.get_view_interval()]
        else:
            _locs = self.locs
        locs = (np.asarray(_locs) - self.offset) / 10. ** self.orderOfMagnitude
        loc_range = np.ptp(locs)
        # Curvilinear coordinates can yield two identical points.
        if loc_range == 0:
            loc_range = np.max(np.abs(locs))
        # Both points might be zero.
        if loc_range == 0:
            loc_range = 1
        if len(self.locs) < 2:
            # We needed the end points only for the loc_range calculation.
            locs = locs[:-2]
        loc_range_oom = int(math.floor(math.log10(loc_range)))
        # first estimate:
        sigfigs = max(0, 3 - loc_range_oom)
        # refined estimate:
        thresh = 1e-3 * 10 ** loc_range_oom
        while sigfigs >= 0:
            if np.abs(locs - np.round(locs, decimals=sigfigs)).max() < thresh:
                sigfigs -= 1
            else:
                break
        sigfigs += 1
        self.format = '%1.' + str(sigfigs) + 'f'
        if self._usetex or self._useMathText:
            # self.format = r'$\mathdefault{%s}$' % self.format
            self.format = r'$%s$' % self.format


class _LogFormatter(matplotlib.ticker.LogFormatterSciNotation):
    def __call__(self, x, pos=None):
        s = super().__call__(x, pos=pos)

        if 'mathdefault' in s:
            s = s.replace(r'\mathdefault{', '')
            s = s[0:-2] + '$'
        return s


class _Axes(Axes):
    """
    This is the only way to override some of default for the plotting methods.
    For example, that points are drawn with a line between.  No way to do it in
    the config file, because it will affect all lines not just the plotting
    routines.
    """
    def plot(
        self,
        *args,
        marker=None,
        linestyle=None,
        **kw
    ):

        marker, linestyle = self._get_marker_and_linestyle(
            marker=marker,
            linestyle=linestyle,
        )

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().plot(
            *args,
            marker=marker,
            linestyle=linestyle,
            **kw
        )

    def errorbar(self, *args, marker=None, linestyle=None, **kw):

        marker, linestyle = self._get_marker_and_linestyle(
            marker=marker,
            linestyle=linestyle,
        )

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().errorbar(
            *args,
            marker=marker,
            linestyle=linestyle,
            **kw
        )

    def _get_marker_and_linestyle(self, *, marker, linestyle):

        if marker is None and linestyle is None:
            marker = DEFAULT_MARKER

        if linestyle is None:
            linestyle = 'none'

        return marker, linestyle

    def hist(
        self,
        *args,
        binsize=None,
        bins=None,
        range=None,
        min=None,
        max=None,
        **kw
    ):
        """
        make a histogram plot

        Parameters
        ----------
        x: array or sequences
            Array of x values
        binsize: float, optional
            Optional binsize, overrides bins= keyword
        bins: int or sequence
            Optional bins keywords.  Can be an integer number of bins or the
            bin edges.  See matplotlib ax.hist documentation
        range: 2-element sequence, optional
            The min/max range for binning the data.  Defaults to
            min and max of the input data.  Takes precedence over
            min= and max= keywords
        min: float
            Minimum value to use in data set. If range is not set, then
            the range will be [min, ?]
        max: float
            Maxiimum value to use in data set. If range is not set, then
            the range have this as max value

        Additional keywords for ax.hist command. See docs for matplotlib
        axes.hist command for details

        Returns
        -------
        Plot instance
        """

        # binsize takes precedence over bins
        if binsize is not None:
            if range is None:

                if len(args) == 0:
                    raise ValueError("send data in position 1")

                x = args[0]

                if min is None:
                    min = x.min()
                if max is None:
                    max = x.max()

                range = [min, max]

            bins = np.int64((range[1] - range[0]) / np.float64(binsize))
            if bins < 1:
                bins = 1

        return super().hist(
            *args,
            bins=bins,
            range=range,
            **kw
        )

    def set_yscale(self, value, **kwargs):
        ret = super().set_yscale(value, **kwargs)
        if value == 'log':
            self.yaxis.set_major_formatter(_LogFormatter())

        return ret


class _PlotContainer(object):
    def show(self, dpi=None):
        """
        show the plot on the display.  Requires tkinter
        to be installed and able to connect to a display

        Parameters
        ----------
        dpi: float, optional
            Optional dpi for image file formats such as png
        """

        if dpi is not None:
            # need to do it here or else bbox is wrong after savefig (does not
            # store it permanently)
            self.set_dpi(dpi)

        if self._legend:
            self.legend(*self._legend.args, **self._legend.kw)

        if self.aratio is not None:
            self.set_aspect(
                1.0/self.get_data_ratio()*self.aratio
            )

        _show_fig(self)

    def savefig(
        self,
        file,
        *,
        bbox_inches='tight',
        **kwargs
    ):
        """
        write the plot to a file

        Parameters
        ----------
        file: str
            Filename to write
        **kw see savefig docs
        """

        if self._legend:
            self.legend(*self._legend.args, **self._legend.kw)

        if self.aratio is not None:
            self.set_aspect(
                1.0/self.get_data_ratio()*self.aratio
            )

        super().savefig(file, bbox_inches=bbox_inches, **kwargs)

    def add_subplot(self, *args, **kwargs):
        if not len(args):
            args = (1, 1, 1)

        if len(args) == 1 and isinstance(args[0], Integral):
            if not 100 <= args[0] <= 999:
                raise ValueError("Integer subplot specification must be a "
                                 "three-digit number, not {}".format(args[0]))
            args = tuple(map(int, str(args[0])))

        if 'figure' in kwargs:
            # Axes itself allows for a 'figure' kwarg, but since we want to
            # bind the created Axes to self, it is not allowed here.
            raise TypeError(
                "add_subplot() got an unexpected keyword argument 'figure'")

        if isinstance(args[0], SubplotBase):

            a = args[0]
            if a.get_figure() is not self:
                raise ValueError(
                    "The Subplot must have been created in the present figure")
            # make a key for the subplot (which includes the axes object id
            # in the hash)
            key = self._make_key(*args, **kwargs)
        else:
            projection_class, kwargs, key = \
                self._process_projection_requirements(*args, **kwargs)

            # try to find the axes with this key in the stack
            ax = self._axstack.get(key)

            if ax is not None:
                if isinstance(ax, projection_class):
                    # the axes already existed, so set it as active & return
                    self.sca(ax)
                    return ax
                else:
                    # Undocumented convenience behavior:
                    # subplot(111); subplot(111, projection='polar')
                    # will replace the first with the second.
                    # Without this, add_subplot would be simpler and
                    # more similar to add_axes.
                    self._axstack.remove(ax)

            # a = subplot_class_factory(projection_class)(
            #     self, *args, **kwargs,
            # )
            # ESS override class to use ours
            a = subplot_class_factory(_Axes)(
                self,
                *args,
                **kwargs
            )

        return self._add_axes_internal(key, a)


class Plot(_PlotContainer, mplt.Figure):
    """
    This object combines the figure and single axis so
    we don't need to carry around both
    """
    def __init__(
        self,
        figsize=None,
        dpi=None,
        facecolor=None,
        edgecolor=None,
        linewidth=0.0,
        frameon=None,
        subplotpars=None,  # default to rc
        tight_layout=None,  # default to rc figure.autolayout
        constrained_layout=None,  # default to rc
        aratio=None,
        legend=None,
        **axis_kw
    ):

        super().__init__(
            figsize=figsize,
            dpi=dpi,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            frameon=frameon,
            subplotpars=subplotpars,
            tight_layout=tight_layout,
            constrained_layout=constrained_layout,  # default to rc
        )

        self.subplots()

        ax = self.axes[0]

        # default formatters
        ax.xaxis.set_major_formatter(_ScalarFormatter())
        ax.yaxis.set_major_formatter(_ScalarFormatter())

        self.set(**axis_kw)

        self.aratio = aratio
        self._set_legend(legend)

    def _set_legend(self, legend):
        """
        set the legend

        Parameters
        ----------
        legend: Legend or bool
            If a boolean True, the legend is auto-generated.  For more control
            send a Legend instance.
        """
        if legend is True:
            self._legend = Legend()
        elif legend:
            # we got something that wasn't False, we'll let
            # duck typing do its thing
            self._legend = legend
        else:
            self._legend = None

    def legend(self, *args, **kw):
        self.axes[0].legend(*args, **kw)

    def __getattr__(self, name):
        """
        pass on calls to the axis, e.g. making a plot
        """
        return getattr(self.axes[0], name)


class Table(_PlotContainer, mplt.Figure):
    def __init__(
        self,
        nrows=1,
        ncols=1,
        sharex=False,
        sharey=False,
        squeeze=True,
        subplot_kw=None,
        gridspec_kw=None,
        # aratio=None,
        **kw,
    ):

        super().__init__(**kw)

        self._axs = self.subplots(
            nrows=nrows,
            ncols=ncols,
            sharex=sharex,
            sharey=sharey,
            squeeze=squeeze,
            subplot_kw=subplot_kw,
            gridspec_kw=gridspec_kw,
        )

        for ax in self.axes:
            ax.xaxis.set_major_formatter(_ScalarFormatter())
            ax.yaxis.set_major_formatter(_ScalarFormatter())

        # self.aratio = aratio
        self.aratio = None
        self._legend = None

    def __getitem__(self, indices):
        """
        pass on calls to the axis, e.g. making a plot
        """

        return self._axs[indices]


def _show_fig(fig, background=False):
    import io

    io_buf = io.BytesIO()

    # cannot set bbox_inches tight here because in fig.canvas.print_figure it
    # does not store the bbox permanently, it resets it to what it was before
    # the call

    fig.savefig(io_buf, bbox_inches=None, format='raw')
    io_buf.seek(0)

    shape = (
        int(fig.bbox.bounds[3]),
        int(fig.bbox.bounds[2]),
        -1,
    )

    data = np.frombuffer(io_buf.getvalue(), dtype=np.uint8)
    img_array = np.reshape(
        data,
        newshape=shape,
    )

    io_buf.close()

    if background:
        from multiprocessing import Process
        p = Process(target=_show_array_tkinter, args=(img_array, ))
        p.start()
    else:
        _show_array_tkinter(img_array)


class _TkinterWindowFromArray(object):
    def __init__(self, img_array):
        from tkinter import Tk, Canvas, NW
        from PIL import ImageTk, Image

        img = Image.fromarray(img_array)
        w, h = img.size

        self.root = Tk()
        self.root.bind('q', self.destroy)

        canvas = Canvas(self.root, width=w, height=h)
        canvas.pack()

        self.imgtk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=NW, image=self.imgtk)
        self.root.mainloop()

    def destroy(self, even):
        self.root.destroy()


def _show_array_tkinter(img_array):
    """
    requires pillow
    """

    try:
        _ = _TkinterWindowFromArray(img_array)
    except KeyboardInterrupt:
        pass
