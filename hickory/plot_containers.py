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
    def show(self, dpi=None, fork=False):
        """
        Show the plot on the display.  Requires tkinter and pillow/PIL to be
        installed and able to connect to a display

        Parameters
        ----------
        dpi: float, optional
            Optional dpi for image file formats such as png
        fork: bool, optional
            If fork is set to True, the plot will "go in the background"
            in a separate thread.  This allows the program to continue,
            and users in interactive sessions to do other work, with
            the plot remaining visible.
        """

        if dpi is not None:
            # need to do it here or else bbox is wrong after savefig (does not
            # store it permanently)
            self.axes[0].set_dpi(dpi)

        if self._legend:
            self.legend(*self._legend.args, **self._legend.kw)

        self._set_aratio_maybe()

        self.fig.show()
        # input('hit enter')
        mplt.show()
        # _show_fig(self, fork=fork)

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

        self.fig.savefig(file, bbox_inches=bbox_inches, **kwargs)

    def set_aratio(self, aratio):
        self.ax.set_aspect(1.0/self.ax.get_data_ratio()*aratio)

    def _set_aratio_maybe(self):
        if hasattr(self, 'aratio') and self.aratio is not None:
            self.set_aratio(self.aratio)
            # self.set_aspect(
            #     1.0/self.get_data_ratio()*self.aratio
            # )

    def add_subplot(self, *args, **kwargs):

        cycler = kwargs.pop('cycler', None)

        if 'figure' in kwargs:
            # Axes itself allows for a 'figure' kwarg, but since we want to
            # bind the created Axes to self, it is not allowed here.
            raise TypeError(
                "add_subplot() got an unexpected keyword argument 'figure'")

        if len(args) == 1 and isinstance(args[0], SubplotBase):
            ax = args[0]
            key = ax._projection_init
            if ax.get_figure() is not self:
                raise ValueError("The Subplot must have been created in "
                                 "the present figure")
        else:
            if not args:
                args = (1, 1, 1)
            # Normalize correct ijk values to (i, j, k) here so that
            # add_subplot(211) == add_subplot(2, 1, 1).  Invalid values will
            # trigger errors later (via SubplotSpec._from_subplot_args).
            if (len(args) == 1 and isinstance(args[0], Integral)
                    and 100 <= args[0] <= 999):
                args = tuple(map(int, str(args[0])))
            projection_class, pkw = self._process_projection_requirements(
                *args, **kwargs)

            # ESS override class to use ours
            # ax = subplot_class_factory(projection_class)(self, *args, **pkw)
            ax = subplot_class_factory(HickoryAxes)(
                self,
                *args,
                cycler=cycler,
                **pkw,
            )

            key = (projection_class, pkw)
        return self._add_axes_internal(ax, key)

    def __iter__(self):
        self._ax_index = 0
        return self

    def __next__(self):
        if self._ax_index == len(self.axes):
            raise StopIteration
        plt = self.axes[self._ax_index]
        self._ax_index += 1
        return plt


class Plot(_PlotContainer):
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
        cycler=None,
        subplot_kw=None,
        **axis_kw
    ):

        if figsize is None:
            width = 6.4
            figsize = [width, width*aratio]

        self.fig = mplt.figure(
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

        # if subplot_kw is None:
        #     subplot_kw = {}
        # subplot_kw['cycler'] = cycler

        self.fig.subplots(subplot_kw=subplot_kw)
        self.axes = self.fig.axes
        self.ax = self.fig.axes[0]

        # default formatters
        self.ax.xaxis.set_major_formatter(HickoryScalarFormatter())
        self.ax.yaxis.set_major_formatter(HickoryScalarFormatter())

        self.ax.set(**axis_kw)

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
        return getattr(self.ax, name)


class _PlotContainerOld(object):
    """
    over-ride the show and savefig methods.

    Showing does does not use one of the toolkit backends from matplotlib, but
    rather Tkinter, and thus hickory can be imported with and without a
    display, yet can still provide a plot display, unlike matplotlib which will
    crash if you have set a toolkit backend but no display is present.
    """
    def show(self, dpi=None, fork=False):
        """
        Show the plot on the display.  Requires tkinter and pillow/PIL to be
        installed and able to connect to a display

        Parameters
        ----------
        dpi: float, optional
            Optional dpi for image file formats such as png
        fork: bool, optional
            If fork is set to True, the plot will "go in the background"
            in a separate thread.  This allows the program to continue,
            and users in interactive sessions to do other work, with
            the plot remaining visible.
        """

        if dpi is not None:
            # need to do it here or else bbox is wrong after savefig (does not
            # store it permanently)
            self.axes[0].set_dpi(dpi)

        if self._legend:
            self.legend(*self._legend.args, **self._legend.kw)

        self._set_aratio_maybe()

        _show_fig(self, fork=fork)

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

        cycler = kwargs.pop('cycler', None)

        if 'figure' in kwargs:
            # Axes itself allows for a 'figure' kwarg, but since we want to
            # bind the created Axes to self, it is not allowed here.
            raise TypeError(
                "add_subplot() got an unexpected keyword argument 'figure'")

        if len(args) == 1 and isinstance(args[0], SubplotBase):
            ax = args[0]
            key = ax._projection_init
            if ax.get_figure() is not self:
                raise ValueError("The Subplot must have been created in "
                                 "the present figure")
        else:
            if not args:
                args = (1, 1, 1)
            # Normalize correct ijk values to (i, j, k) here so that
            # add_subplot(211) == add_subplot(2, 1, 1).  Invalid values will
            # trigger errors later (via SubplotSpec._from_subplot_args).
            if (len(args) == 1 and isinstance(args[0], Integral)
                    and 100 <= args[0] <= 999):
                args = tuple(map(int, str(args[0])))
            projection_class, pkw = self._process_projection_requirements(
                *args, **kwargs)

            # ESS override class to use ours
            # ax = subplot_class_factory(projection_class)(self, *args, **pkw)
            ax = subplot_class_factory(HickoryAxes)(
                self,
                *args,
                cycler=cycler,
                **pkw,
            )

            key = (projection_class, pkw)
        return self._add_axes_internal(ax, key)

    def __iter__(self):
        self._ax_index = 0
        return self

    def __next__(self):
        if self._ax_index == len(self.axes):
            raise StopIteration
        plt = self.axes[self._ax_index]
        self._ax_index += 1
        return plt


class PlotOld(_PlotContainer, mplt.Figure):
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
        cycler=None,
        subplot_kw=None,
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

        if subplot_kw is None:
            subplot_kw = {}
        subplot_kw['cycler'] = cycler

        self.subplots(subplot_kw=subplot_kw)

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
    cycler: Cycler, optional
        A cycler to use for marker/line properties

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
        cycler=None,
        **kw,
    ):

        # if figsize is None:
        #     width = 6.4
        #     figsize = [width, width*nrows/ncols]

        super().__init__(figsize=figsize, **kw)

        if subplot_kw is None:
            subplot_kw = {}
        if cycler is not None:
            subplot_kw['cycler'] = cycler

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


def _show_fig(fig, fork=False):
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

    if fork:
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
        from tkinter import Tk, Canvas, NW, TclError
        from PIL import ImageTk, Image

        try:
            img = Image.fromarray(img_array)
            w, h = img.size

            self.root = Tk()
            self.root.bind('q', self.destroy)

            canvas = Canvas(self.root, width=w, height=h)
            canvas.pack()

            self.imgtk = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor=NW, image=self.imgtk)
            self.root.mainloop()
        except TclError:
            raise KeyboardInterrupt

    def destroy(self, even):
        self.root.destroy()


def _show_array_tkinter(img_array):
    _ = _TkinterWindowFromArray(img_array)
