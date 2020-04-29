import numpy as np


class _PlotEntryContainer(object):
    """
    generic container base class

    Parameters
    ----------
    style: string or sequence of strings

        e.g. these would both produce a red triangle mark with
        a thick dotted string in between

            style='mark=triangle, red, thick, dotted'
            style=['mark=triangle', 'red', 'thick', 'dotted']

        See the pgfplots manual for all style options

    label: string
        A label for the legend
    """

    def __init__(self, style=None, label=None):

        self.style = style
        self.label = label

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        if isinstance(style, (tuple, list)):
            style = ", ".join(style)
        self._style = style

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def addplot_options(self):
        style = self.style
        if style is not None and style != "":
            style_options = "+[%s]" % style
        else:
            style_options = ""

        return style_options

    @property
    def legend_entry(self):
        label = self.label
        if label is None:
            return ""
        else:
            return r"\addlegendentry{%s}" % label


class Points(_PlotEntryContainer):
    """
    represent a set of points

    Parameters
    ----------
    x: scalar or sequence
        x values to plot
    y: scalar or sequence
        y values to plot
    xerr: scalar or sequence
        symmetric x error bars to plot
    yerr: scalar or sequence
        symmetric y error bars to plot
    style: string or sequence of strings
        Because in pgfplots some options are keyword value pairs and some are
        not, there is no uniform way to represent style.  For this reason most
        style options need to be sent as strings.  The style can be set as
        either one long string or a sequence of strings:

        e.g. these would both produce a red triangle mark with
        a thick dashed string in between

            style='mark=triangle, red, thick, dashed'
            style=['mark=triangle', 'red', 'thick', 'dashed']

        See the pgfplots manual for all style options

    label: string
        A label for the legend
    """

    def __init__(self, x, y, xerr=None, yerr=None, style=None, label=None):

        self._x = _make_array(x)
        self._y = _make_array(y)
        assert self._x.size == self._y.size, "x and y must be same size"

        self._xerr = xerr
        if self._xerr is not None:
            self._xerr = _make_array(self._xerr)
            assert (
                self._xerr.size == self._x.size
            ), "values and x errors must be same size"

        self._yerr = yerr
        if self._yerr is not None:
            self._yerr = _make_array(self._yerr)
            assert (
                self._yerr.size == self._x.size
            ), "values and y errors must be same size"

        super().__init__(style=style, label=label)

    @property
    def style(self):
        style = super().style

        if style is None:
            style = []
        else:
            style = [style]

        if self._yerr is not None or self._xerr is not None:
            style.append("error bars")

        if self._yerr is not None:
            style.append("y dir=both, y explicit")
        if self._xerr is not None:
            style.append("x dir=both, x explicit")

        return ", ".join(style)

    # we are forced to redefine the setter
    @style.setter
    def style(self, style):
        super(Points, self.__class__).style.fset(self, style)
        # super().style.fset(style)

    @property
    def addplot(self):
        options = self.addplot_options
        table = self.table

        addplot = r"""    \addplot%(options)s
%(table)s""" % {
            "options": options,
            "table": table,
        }
        return addplot

    @property
    def table(self):
        data = []

        table_declare = ["x=x", "y=y"]

        hdr = ["x", "y"]

        if self._xerr is not None:
            table_declare.append("x error=xerr")
            hdr.append("xerr")
        if self._yerr is not None:
            table_declare.append("y error=yerr")
            hdr.append("yerr")

        table_declare = "    table[%s]" % ", ".join(table_declare)
        data.append(table_declare)
        data.append("    {")

        hdr = "      %s" % " ".join(hdr)
        data.append(hdr)

        for i in range(self._x.size):
            v = []

            v.append("%g" % self._x[i])
            v.append("%g" % self._y[i])

            if self._xerr is not None:
                v.append("%g" % self._xerr[i])

            if self._yerr is not None:
                v.append("%g" % self._yerr[i])

            v = "      %s" % " ".join(v)

            data.append(v)

        data.append("    };")

        return "\n".join(data)


class Function(_PlotEntryContainer):
    """
    represent a function for plotting

    Parameters
    ----------
    function: string
        String with function to plot
    domain: sequence
        (xmin, xmax) sequence.  Note you can also send this as a
        style parameter 'domain=xmin:xmax'
    style: string or sequence of strings

        e.g. these would both produce a red triangle mark with
        a thick dotted string in between

            style='mark=triangle, red, thick, dotted, domain=5:10'
            style=['mark=triangle', 'red', 'thick', 'dotted', 'domain=5:10']

        See the pgfplots manual for all style options
        Note for functions the style 'mark=none' is set automatically

    label: string
        A label for the legend
    """

    def __init__(self, function, domain=None, style=None, label=None):

        self.function = function
        self.domain = domain

        super().__init__(style=style, label=label)

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, domain):

        self._domain = domain

        if domain is not None:
            assert isinstance(
                domain, (tuple, list)
            ), "domain must be a tuple or list of length 2"
            assert len(domain) == 2, "domain must be a tuple or list of length 2"

    @property
    def style(self):
        style = super().style

        if style is None:
            style = []
        else:
            style = [style]

        style = ["mark=none"] + style
        domain = self.domain
        if domain is not None and "domain" not in style:
            style.append("domain=%g:%g" % tuple(domain))

        return ", ".join(style)

    # we are forced to redefine the setter
    @style.setter
    def style(self, style):
        super(Function, self.__class__).style.fset(self, style)
        # super().style.fset(style)

    @property
    def addplot(self):
        options = self.addplot_options

        addplot = r"""    \addplot%(options)s {%(function)s};""" % {
            "options": options,
            "function": self.function,
        }
        return addplot


def _make_array(data):
    return np.array(data, ndmin=1, copy=False)
