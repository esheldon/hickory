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
    legend: Legend or bool
        If a boolean True, the legend is auto-generated.  For more control send
        a Legend instance.
    """
    def __init__(self, xlabel=None, ylabel=None, legend=None):

        self._xlabel = xlabel
        self._ylabel = ylabel
        self._set_legend(legend)
        self.objlist = []
        self._reset_fig()

    def add(self, *args):
        self.objlist += args
        self._reset_fig()

    def write(self, fname, dpi=None):
        fig, ax = self.get_fig()
        self.fig.savefig(fname, dpi=dpi)

    def show(self, dpi=None):
        with tempfile.TemporaryDirectory() as dir:
            fname = tempfile.mktemp(dir=dir, suffix='.png')
            self.write(fname, dpi=dpi)

            _show_tkinter(fname)

    def get_fig(self):
        if self.fig is None or self.ax is None:
            self._render_fig()
        return self.fig, self.ax

    def _render_fig(self):
        self.fig, self.ax = plt.subplots()

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


class _TkinterWindow(object):
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


def _show_tkinter(fname):
    """
    requires pillow
    """

    try:
        _ = _TkinterWindow(fname)
    except KeyboardInterrupt:
        pass
