"""
TODO:
    - plotting 2d arrays as images
    - 2d histograms, e.g. using hexbin under the hood
    - non-symmetric error bars
    - fill between curves etc.
    - plotting functions
    - figure size: maybe have it in write/show and force a rerender
      when that is sent?
"""
import numpy as np
import tempfile
import matplotlib.pyplot as plt

from .legend import Legend


class _PlotContainer(object):
    def write(self, fname, dpi=None):
        """
        write the plot to a file

        Parameters
        ----------
        fname: str
            Filename to write
        dpi: float, optional
            Optional dpi for image file formats such as png
        """
        fig = self._render()
        if dpi is not None:
            fig.set_dpi(dpi)

        fig.savefig(fname, bbox_inches='tight')

    def show(self, dpi=None):
        """
        show the plot on the display.  Requires tkinter
        to be installed and able to connect to a display

        Parameters
        ----------
        dpi: float, optional
            Optional dpi for image file formats such as png
        """
        fig = self._render()
        _show_fig(fig, dpi=dpi)

    def _render(self):
        raise NotImplementedError('implement _render()')


class Plot(_PlotContainer):
    """
    A plot container base class

    Parameters
    ----------
    xlabel: str
        Label for the x axis
    ylabel: str
        Label for the y axis
    aratio: float
        Axis ratio of output plot, ysize/xsize
    legend: Legend or bool
        If a boolean True, the legend is auto-generated.  For more control send
        a Legend instance.
    """
    def __init__(
        self,
        *,
        xlabel=None,
        ylabel=None,
        aratio=None,
        legend=None,
    ):

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.aratio = aratio
        self.legend = legend
        self.reset()

    def reset(self):
        """
        reset the object list and rendering
        """
        self.objlist = []

    def add(self, *args):
        """
        add a new object to be plotted.  This resets the
        rendered state

        Parameters
        ----------
        *args: objects
            A set of objects to be rendered, e.g. Points.
        """
        self.objlist += args

    def render_axis(self, ax):
        """
        render into the specified axis

        Parameters
        -----------
        ax: e.g. Axis
            An axis object
        """
        ax.clear()

        if self.xlabel is not None:
            ax.set_xlabel(self.xlabel)

        if self.ylabel is not None:
            ax.set_ylabel(self.ylabel)

        for obj in self.objlist:
            obj._add_to_axes(ax)

        legend = self.legend
        if legend is not None:
            ax.legend(
                loc=legend.loc,
                frameon=legend.frame,
                borderaxespad=legend.borderaxespad,
                framealpha=legend.framealpha,
            )

        # needs to come after plotting
        if self.aratio is not None:
            ax.set_aspect(
                1.0/ax.get_data_ratio()*self.aratio
            )

    @property
    def xlabel(self):
        """
        get the x label
        """
        return self._xlabel

    @xlabel.setter
    def xlabel(self, xlabel):
        """
        get the x label
        """
        self._xlabel = xlabel

    @property
    def ylabel(self):
        """
        get the y label
        """
        return self._ylabel

    @ylabel.setter
    def ylabel(self, ylabel):
        """
        get the y label
        """
        self._ylabel = ylabel

    @property
    def aratio(self):
        """
        get the y label
        """
        return self._aratio

    @aratio.setter
    def aratio(self, aratio):
        """
        get the y label
        """
        self._aratio = aratio

    @property
    def legend(self):
        """
        get the legend instance
        """
        return self._legend

    @legend.setter
    def legend(self, legend):
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

    def _show_from_file(self, dpi=None):
        with tempfile.TemporaryDirectory() as dir:
            fname = tempfile.mktemp(dir=dir, suffix='.png')
            self.write(fname, dpi=dpi)

            _show_file_tkinter(fname)

    def _render(self):
        self.fig, self.ax = plt.subplots()
        self.render_axis(self.ax)

        return self.fig


class Table(_PlotContainer):
    """
    Represent a table of plots

    Parameters
    ----------
    nrows: int
        Number of rows in table
    ncols: int
        Number of columns in the table
    """
    def __init__(self, *, nrows, ncols):
        self.nrows = int(nrows)
        self.ncols = int(ncols)
        if self.nrows < 1:
            raise ValueError("got nrows %d < 1" % self.nrows)
        if self.ncols < 1:
            raise ValueError("got ncols %d < 1" % self.ncols)

        self.reset()

    def reset(self):
        """
        Completely reset the table.  All plots are set to None
        """
        self.fig, self.axes = plt.subplots(nrows=self.nrows, ncols=self.ncols)
        self._plots = []
        for row in range(self.nrows):
            col_plots = []
            for col in range(self.ncols):
                col_plots.append(None)
            self._plots.append(col_plots)

    def _render(self):
        """
        render the table if needed

        Each plot is checked to see if it has been rendred
        """
        for row in range(self.nrows):
            for col in range(self.ncols):

                ax = self.axes[row, col]

                plot = self[row, col]
                if plot is not None:
                    print('rendering:', row, col)
                    plot.render_axis(ax)
                else:
                    ax.axis('off')

        return self.fig

    def __getitem__(self, indices):
        row, col = self._get_row_col(indices)
        return self._plots[row][col]

    def __setitem__(self, indices, plot):
        """
        set a plot

        Parameters
        ----------
        row, col: int
            row and column indices
        plot: plot container or None
            If None, the plot is set to invisible
        """

        row, col = self._get_row_col(indices)

        self._plots[row][col] = plot

    def _get_row_col(self, indices):
        if len(indices) != 2:
            raise ValueError(
                "to set a plot use table[row, col] = plot"
            )

        row, col = indices

        if row < 0 or row > self.nrows-1:
            raise ValueError(
                "row %d out of range [%d, %d]" % (row, self.nrows, self.ncols)
            )
        if col < 0 or col > self.ncols-1:
            raise ValueError(
                "col %d out of range [%d, %d]" % (col, self.ncols, self.ncols)
            )

        return row, col

def _show_viewer(fname, viewer='feh'):
    import subprocess
    command = [viewer, fname]
    subprocess.check_call(command)


def _show_fig(fig, dpi=None):
    import io

    if dpi is not None:
        # need to do it here or else bbox is wrong after savefig (does not
        # store it permanently)
        fig.set_dpi(dpi)

    io_buf = io.BytesIO()

    # cannot set bbox_inches tight here because in fig.canvas.print_figure
    # it does not store the bbox permanently it resets it to what it was
    # before the call

    fig.savefig(io_buf, format='raw')
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

    # from multiprocessing import Process
    # p = Process(target=_show_array_tkinter, args=(img_array, ))
    # p.start()

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


class _TkinterWindowFromFile(object):
    def __init__(self, fname):
        from tkinter import Tk, Canvas, NW
        from PIL import ImageTk, Image

        img = Image.open(fname)
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


def _show_file_tkinter(fname):
    """
    requires pillow
    """

    try:
        _ = _TkinterWindowFromFile(fname)
    except KeyboardInterrupt:
        pass
