import os
import shutil
import tempfile
from .data_containers import (
    Points,
    Function,
)

GOLDEN_RATIO = 1.618

HEAD = r"""\documentclass{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=newest}
\usepgfplotslibrary{groupplots}

\begin{document}

\begin{tikzpicture}

"""

TAIL = r"""
\end{tikzpicture}
\end{document}
"""

# forf filling
# \usepgfplotslibrary{fillbetween}


class Plot(object):
    """
    basic plot container

    Note all parameters that can be sent on construction can also be
    set on the plot itself.  e.g.

    plt = Plot(xmin=3)
    plt = Plot()
    plt.xmin = 3

    Parameters
    ----------
    xmin: number
        Minimum x range for plot
    xmax:
        Maximum x range for plot
    ymin:
        Minimum y range for plot
    ymax:
        Maximum y range for plot
    ratio: float
        Axis ratio ysize/xsize for plot, default 1/GOLDEN_RATIO.
        If both width and height are sent, ratio is not used
    width: number
        Width of plot.  Units are sent in the units keyword
    height: number
        Height of plot.  Units are sent in the units keyword.
        Default will be width*ratio
    nminor_ticks: int
        Number of minor ticks between major ticks
    xlabel: string
        A label for the x axis
    ylabel: string
        A label for the y axis
    units: string
        Units for sizes e.g. cm, in, mm
    legend_pos: string
        E.g. 'north west'
    legend_style: string or list
        E.g. 'draw=none' or ['draw=none']
    contents: list
        Optional list of contents, e.g.

        contents = [Points(x, y), Function('x^2')]

        This is an alternative to puting objects in in plot using plt.add()
    """
    def __init__(self,
                 xmin=None,
                 xmax=None,
                 ymin=None,
                 ymax=None,
                 ratio=GOLDEN_RATIO,
                 width=8,
                 height=None,
                 nminor_ticks=3,
                 xlabel=None,
                 ylabel=None,
                 units='cm',
                 legend_pos=None,
                 legend_style=None,
                 contents=None):

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.ratio = ratio
        self.width = width
        self.height = height
        self.nminor_ticks = nminor_ticks
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.units = units

        self.legend_pos = legend_pos
        self.legend_style = legend_style

        if contents is None:
            contents = []
        assert isinstance(contents, (tuple, list))

        self._contents = contents

    def add(self, *args):
        """
        add an object to the plot
        """
        for arg in args:
            self._contents.append(arg)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        assert units in [
            'cm', 'mm', 'in',
        ]
        self._units = units

    @property
    def height(self):
        height = self._height
        if height is None:
            if self.width is not None and self.ratio is not None:
                height = self.width/self.ratio

        return height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def legend_style(self):
        return self._legend_style

    @legend_style.setter
    def legend_style(self, legend_style):
        if isinstance(legend_style, (tuple, list)):
            legend_style = ', '.join(legend_style)
        self._legend_style = legend_style

    @property
    def axis_options(self):

        options = []
        options.append('axis on top')

        if self.nminor_ticks is not None:
            options.append('minor tick num=%d' % self.nminor_ticks)

        width = self.width
        if width is not None:
            widthstr = '%g%s' % (width, self.units)
            options.append('width=%s' % widthstr)

        height = self.height
        if height is not None:
            heightstr = '%g%s' % (height, self.units)
            options.append('height=%s' % heightstr)

        options.append('scale only axis')

        if self.xmin is not None:
            options.append('xmin=%g' % self.xmin)
        if self.xmax is not None:
            options.append('xmax=%g' % self.xmax)
        if self.ymin is not None:
            options.append('ymin=%g' % self.ymin)
        if self.ymax is not None:
            options.append('ymax=%g' % self.ymax)
        if self.xlabel is not None:
            options.append('xlabel={%s}' % self.xlabel)
        if self.ylabel is not None:
            options.append('ylabel={%s}' % self.ylabel)

        if self.legend_pos is not None:
            options.append('legend pos=%s' % self.legend_pos)
        if self.legend_style is not None:
            options.append('legend style={%s}' % self.legend_style)

        return ',\n      '.join(options)

    def write(self, fname, dpi=150):
        """
        write a file.

        If the file name has .tex extension, just the tex file is written.  If
        the file had .pdf extension, a temporary tex file is written and
        converted to pdf.  If the extension is .png it is converted from pdf at
        the requested resolution in dpi

        Parameters
        ----------
        fname: str
            The file name to write.
        dpi: int, optional
            Optional dpi for png writing
        """

        ext = fname[-4:]
        if ext == '.tex':
            self.write_tex(fname)
        elif ext == '.pdf':
            self.write_pdf(fname)
        elif ext == '.png':
            self.write_png(fname, dpi=dpi)

    def write_tex(self, tex_file):
        """
        write a tex that will produce the figure after it is run through
        pdflatex

        Parameters
        ----------
        tex_file: str
            The file name to write.
        """
        with open(tex_file, 'w') as fobj:
            self._write_tex(fobj)

    def write_pdf(self, pdf_file):
        """
        write the plot to a pdf file

        Parameters
        ----------
        pdf_file: str
            The file name to write.
        """

        if os.path.exists(pdf_file):
            os.remove(pdf_file)

        pdf_base = os.path.basename(pdf_file)

        with tempfile.TemporaryDirectory() as tdir:

            tfile = os.path.join(tdir, pdf_base)
            self._write_pdf(tfile)
            shutil.copy(tfile, pdf_file)

    def write_png(self, png_file, dpi=150):
        """
        write the plot to a png file

        Parameters
        ----------
        png_file: str
            The file name to write.
        dpi: int, optional
            Optional dpi for png writing
        """

        if os.path.exists(png_file):
            os.remove(png_file)

        assert png_file[-4:] == '.png'

        png_base = os.path.basename(png_file)

        pdf_base = png_base[:-4] + '.pdf'

        with tempfile.TemporaryDirectory() as tdir:

            pdf_file = os.path.join(tdir, pdf_base)
            self._write_pdf(pdf_file)

            _pdf_to_png(
                pdf_file=pdf_file,
                png_file=png_file,
                dpi=dpi,
            )

    def _write_pdf(self, fname):
        """
        write the plot to a pdf file

        Parameters
        ----------
        fname: str
            The file name to write.
        """

        if os.path.exists(fname):
            os.remove(fname)

        assert fname[-4:] == '.pdf'
        texfile = fname[:-4] + '.tex'

        if os.path.exists(texfile):
            raise RuntimeError('texfile already exists %s' % texfile)

        with open(texfile, 'w') as fobj:
            self._write_tex(fobj)

        command = ['pdflatex']
        fdir = os.path.dirname(fname)
        if fdir is not None:
            command.append('-output-directory %s' % fdir)

        command.append(texfile)
        command = ' '.join(command) + ' > /dev/null'

        ret_code = os.system(command)

        os.remove(texfile)

        if ret_code != 0:
            raise RuntimeError('pdflatex failed')

    def _write_tex(self, fobj):
        """
        write a tex that will produce the figure after run through
        pdflatex

        Parameters
        ----------
        fobj: file object
            The file object for writing
        """
        fobj.write(HEAD)
        _write_axis(fobj=fobj, options=self.axis_options)

        for obj in self._contents:
            fobj.write(obj.addplot)
            if obj.label is not None:
                fobj.write(obj.legend_entry)

            fobj.write('\n\n')

        end_axis(fobj=fobj)
        fobj.write(TAIL)


def _write_axis(*, fobj, options):
    text = r"""\begin{axis}[
    %s
    ]""" % options
    fobj.write(text)
    fobj.write('\n')


def end_axis(*, fobj):
    fobj.write('\n\\end{axis}\n')


def _pdf_to_png(*, png_file, pdf_file, dpi):
    # for jpg, use device jpg
    command = [
        'gs',
        '-dTextAlphaBits=4',
        '-dGraphicsAlphaBits=4',
        '-dSAFER',
        '-dBATCH',
        '-dNOPAUSE',
        '-r%d' % dpi,
        '-sDEVICE=png16m',
        '-sOutputFile=%s' % png_file,
        '%s' % pdf_file,
    ]
    command = ' '.join(command) + ' > /dev/null'
    os.system(command)


def test():
    import numpy as np
    rng = np.random.RandomState(5)

    plt = Plot(
        legend_pos='north west',
        legend_style='draw=none',
    )
    num = 10

    x = np.arange(num)

    err = 5
    y = x**2 + rng.normal(size=num, scale=err)
    yerr = y*0 + err
    pts1 = Points(
        x, y, yerr=yerr, style='only marks',
        label='data',
    )
    fun = Function('x^2', domain=[x.min(), x.max()],
                   label=r'$x^2$')
    pts2 = Points(
        x,
        x**2 + 30,
        label=r'$x^2 + 30$',
    )

    plt.add(pts1, fun, pts2)

    plt.write('test-gen.png')


if __name__ == '__main__':
    test()
