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


class Plot(object):
    """
    A plot container

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
    def __init__(self, xlabel=None, ylabel=None, aratio=None, legend=None):

        self._xlabel = xlabel
        self._ylabel = ylabel
        self._aratio = aratio
        self._set_legend(legend)
        self.objlist = []
        self._reset_fig()

    def add(self, *args):
        self.objlist += args
        self._reset_fig()

    def write(self, fname, dpi=None):
        fig, ax = self.get_fig()
        if dpi is not None:
            fig.set_dpi(dpi)

        self.fig.savefig(fname, bbox_inches='tight')

    def show(self, dpi=None):
        import io

        fig, ax = self.get_fig()

        if dpi is not None:
            # need to do it here or else bbox is wrong after
            # savefig (does not store it permanently)
            fig.set_dpi(dpi)

        # fig.canvas.draw()
        # renderer = fig.canvas.get_renderer()
        # # bbox = ax.get_tightbbox(renderer)
        # bbox = ax.figure.get_tightbbox(renderer)
        # bbox = bbox.padded(None)

        # fig.set_tight_layout(True)
        # print(fig.bbox.bounds)

        io_buf = io.BytesIO()

        # hmm... the bounds end up wrong if I do bbox_inches here,
        # because in fig.canvas.print_figure it does not
        # store the bbox permanently it resets it to what it was
        # before the call
        # fig.savefig(io_buf, format='raw',  bbox_inches='tight')
        # fig.savefig(io_buf, format='raw', bbox_inches=bbox)
        fig.savefig(io_buf, format='raw')
        io_buf.seek(0)

        shape = (int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1)
        # shape = (int(bbox.bounds[3]), int(bbox.bounds[2]), -1)

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

    def _show_from_file(self, dpi=None):
        with tempfile.TemporaryDirectory() as dir:
            fname = tempfile.mktemp(dir=dir, suffix='.png')
            self.write(fname, dpi=dpi)

            _show_file_tkinter(fname)

    def get_fig(self):
        if self.fig is None or self.ax is None:
            self._render_fig()
        return self.fig, self.ax

    def _render_fig(self):
        self.fig, self.ax = plt.subplots()
        # self.fig, self.ax = plt.subplots(tight_layout=True)
        # self.fig, self.ax = plt.subplots(constrained_layout=True)

        if self._xlabel is not None:
            self.ax.set_xlabel(self._xlabel)

        if self._ylabel is not None:
            self.ax.set_ylabel(self._ylabel)

        for obj in self.objlist:
            obj._add_to_axes(self.ax)

        legend = self.legend
        if legend is not None:
            self.ax.legend(
                loc=legend.loc,
                frameon=legend.frame,
                borderaxespad=legend.borderaxespad,
                framealpha=legend.framealpha,
            )

        # needs to come after plotting
        if self._aratio is not None:
            self.ax.set_aspect(
                1.0/self.ax.get_data_ratio()*self._aratio
            )


    def _set_legend(self, legend):
        if legend is True:
            self.legend = Legend()
        elif legend:
            # we got something that wasn't False, we'll let
            # duck typing do its thing
            self.legend = legend
        else:
            self.legend = None

    def _reset_fig(self):
        self.fig = None
        self.ax = None


def _show_viewer(fname, viewer='feh'):
    import subprocess
    command = [viewer, fname]
    subprocess.check_call(command)


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
