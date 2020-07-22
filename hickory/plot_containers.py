import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.axes import (
    SubplotBase,
    subplot_class_factory,
)
from numbers import Integral

from .legend import Legend
from .constants import GOLDEN_ARATIO
from .formatters import HickoryScalarFormatter
from .axes import HickoryAxes


class _PlotContainer(object):
    """
    over-ride the show and savefig methods.

    Showing does does not use one of the toolkit backends from matplotlib, but
    rather Tkinter, and thus hickory can be imported with and without a
    display, yet can still provide a plot display, unlike matplotlib which will
    crash if you have set a toolkit backend but no display is present.
    """
    def show(self, dpi=None):
        """
        Show the plot on the display.  Requires tkinter and pillow/PIL to be
        installed and able to connect to a display

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
        **kw see savefig docs for additional keywords
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
            a = subplot_class_factory(HickoryAxes)(
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
    A plot container.  This class provides an interface to both
    the Figure and axis functionality in one.

    Parameters
    ----------
    aratio: float, optional
        Axis ratio of plot, ysize/xsize. Default is the
        1/(golden ratio) ~ 0.618
    legend: bool or Legend instance
        If True, a legend is created. You can also send a Legend() instance.
        If None or False, no legend is created

    Additional Keywords for the Plot/matplotlib Figure.  See docs for
        the matplotlib Figure class

        figsize dpi facecolor edgecolor linewidth
        frameon subplotpars tight_layout constrained_layout

    Additional Keywords for setting axis parameters such as
        xlabel, xlim, margin (or xmargin/ymargin), etc.
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
        ax.xaxis.set_major_formatter(HickoryScalarFormatter())
        ax.yaxis.set_major_formatter(HickoryScalarFormatter())

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
    """
    A plot container for a table of subplots.  Provides
    access to the Figure and subplot grid in one interface.

    e.g.

    tab = Table(nrows=2, ncols=3, ...)
    tab[1, 0].plot(x, y)
    tab[0, 1].set(xlabel='x', ylabel='y')
    etc.

    Parameters
    ----------
    **figure_kw: keywords for the Figure class
    **subplots_kw: keywords for the subplots command
    """
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
            ax.xaxis.set_major_formatter(HickoryScalarFormatter())
            ax.yaxis.set_major_formatter(HickoryScalarFormatter())

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
    """
    requires pillow/PIL
    """
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

    try:
        _ = _TkinterWindowFromArray(img_array)
    except KeyboardInterrupt:
        pass
