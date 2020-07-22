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
from .constants import GOLDEN_ARATIO

DEFAULT_MARKER = 'o'


class _ScalarFormatter(matplotlib.ticker.ScalarFormatter):
    """
    tick formatter for linear axes

    Removes mathdefault from format strings
    """
    def _set_format(self):
        super()._set_format()

        if 'mathdefault' in self.format:
            self.format = _remove_mathdefault(self.format)


class _LogFormatter(matplotlib.ticker.LogFormatterSciNotation):
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

    def set_aratio(self, aratio):
        self.set_aspect(1.0/self.get_data_ratio()*aratio)

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

    def set(self, margin=None, **kw):
        if margin is not None:
            kw['xmargin'] = margin
            kw['ymargin'] = margin
        super().set(**kw)


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

        self._set_aratio_maybe()

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

        self._set_aratio_maybe()

        super().savefig(file, bbox_inches=bbox_inches, **kwargs)

    def _set_aratio_maybe(self):
        if hasattr(self, 'aratio') and self.aratio is not None:
            self.set_aratio(self.aratio)
            # self.set_aspect(
            #     1.0/self.get_data_ratio()*self.aratio
            # )

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

    def __iter__(self):
        self._ax_index = 0
        return self

    def __next__(self):
        if self._ax_index == len(self.axes):
            raise StopIteration
        plt = self.axes[self._ax_index]
        self._ax_index += 1
        return plt


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
        aratio=GOLDEN_ARATIO,
        legend=None,
        **axis_kw
    ):

        if figsize is None:
            width = 6.4
            figsize = [width, width*GOLDEN_ARATIO]

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
        figsize=None,
        **kw,
    ):

        # if figsize is None:
        #     width = 6.4
        #     figsize = [width, width*nrows/ncols]

        super().__init__(figsize=figsize, **kw)

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
