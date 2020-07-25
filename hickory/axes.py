import numpy as np
from matplotlib.axes import Axes
from .formatters import HickoryScalarFormatter, HickoryLogFormatter
from .colors import COLORS
from .cyclers import get_default_multi_cycler

DEFAULT_MARKER = 'o'


class HickoryAxes(Axes):
    """
    Axes class to over ride defaults in matplotlib Axes

    This is the only way to override some of default for the plotting
    methods.  For example, that points are drawn with a line between.  There
    is no way to do it in the config file, because it will affect all lines
    not just the plotting routines.

    We override the tick formatters here on calls to set_xscale or
    set_yscale

    We provide the ability to set the axis ratio using set_aratio

    We provide binsize= functionality for the hist command, as well
    as more fine grained control over the range

    Provide margin= option for set() which sets both x and y
    margins
    """

    def __init__(self, *args, **kw):

        cycler = kw.pop('cycler', None)
        if cycler is None:
            cycler = get_default_multi_cycler()

        self.cycler = cycler

        res = super().__init__(*args, **kw)

        return res

    def set_aratio(self, aratio):
        self.set_aspect(1.0/self.get_data_ratio()*aratio)

    def plot(self, *args, **kw):

        self._set_color(kw)
        self._set_props_default_noline(kw)

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().plot(*args, **kw)

    def errorbar(self, *args, **kw):

        self._set_color(kw)
        self._set_props_default_noline(kw)

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().errorbar(*args, **kw)

    def curve(self, *args, **kw):

        self._set_color(kw)
        self._set_props_default_line(kw)

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().plot(*args, **kw)

    def function(
        self,
        func,
        range=None,
        npts=100,
        **kw
    ):

        if range is None:
            range = self._viewLim.intervalx

        x = np.linspace(range[0], range[1], npts)

        if callable(func):
            y = func(x)
        else:
            y = eval(func)

        return self.curve(x, y, **kw)

    def _set_color(self, kw):
        if 'color' not in kw:
            kw['color'] = self.cycler.next('color')

    def _set_props_default_noline(self, kw):
        """
        defaulting to no line
        """

        has_marker = 'marker' in kw
        if (not has_marker) or (has_marker and kw['marker'] == 'cycle'):
            kw['marker'] = self.cycler.next('marker')

        linestyle = kw.get('linestyle', None)
        if linestyle is None:
            kw['linestyle'] = 'none'
        elif linestyle == 'cycle':
            kw['linestyle'] = self.cycler.next('linestyle')

    def _set_props_default_line(self, kw):
        """
        defaulting to a line
        """

        has_line = 'linestyle' in kw

        if (not has_line) or (has_line and kw['linestyle'] == 'cycle'):
            kw['linestyle'] = self.cycler.next('linestyle')
        elif has_line and kw['linestyle'] is None:
            kw['linestyle'] = 'none'

        if 'marker' in kw and kw['marker'] == 'cycle':
            kw['marker'] = self.cycler.next('marker')
        else:
            kw['marker'] = None

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

            bins = int(round((range[1] - range[0]) / binsize))
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
            self.yaxis.set_major_formatter(HickoryLogFormatter())
        elif value == 'linear':
            self.yaxis.set_major_formatter(HickoryScalarFormatter())

        return ret

    def set_xscale(self, value, **kwargs):
        ret = super().set_xscale(value, **kwargs)
        if value == 'log':
            self.xaxis.set_major_formatter(HickoryLogFormatter())
        elif value == 'linear':
            self.xaxis.set_major_formatter(HickoryScalarFormatter())

        return ret

    def set(self, margin=None, **kw):
        if margin is not None:
            kw['xmargin'] = margin
            kw['ymargin'] = margin
        super().set(**kw)


class HickoryAxesOld(Axes):
    """
    Axes class to over ride defaults in matplotlib Axes

    This is the only way to override some of default for the plotting
    methods.  For example, that points are drawn with a line between.  There
    is no way to do it in the config file, because it will affect all lines
    not just the plotting routines.

    We override the tick formatters here on calls to set_xscale or
    set_yscale

    We provide the ability to set the axis ratio using set_aratio

    We provide binsize= functionality for the hist command, as well
    as more fine grained control over the range

    Provide margin= option for set() which sets both x and y
    margins
    """

    def __init__(self, *args, **kw):

        if 'cycler' in kw:
            cycler = kw.pop('cycler')
            if cycler is False or cycler is None:
                cycler = None
            elif cycler is True:
                cycler = get_default_cycler()
            else:
                cycler = cycler
        else:
            cycler = get_default_cycler()

        res = super().__init__(*args, **kw)
        self.set_prop_cycle(cycler)

        return res

    def set_aratio(self, aratio):
        self.set_aspect(1.0/self.get_data_ratio()*aratio)

    def plot(self, *args, **kw):

        if 'marker' in kw and kw['marker'] == 'cycle':
            kw.pop('marker')

        # if linestyle not sent, set it to 'none' for no line
        if 'linestyle' in kw:
            linestyle = kw['linestyle']
            if linestyle is None:
                kw['linestyle'] = 'none'
            elif 'cycle' in linestyle:
                kw.pop('linestyle')
        else:
            kw['linestyle'] = 'none'

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().plot(*args, **kw)

    def errorbar(self, *args, **kw):

        if 'marker' in kw and kw['marker'] == 'cycle':
            kw.pop('marker')

        # if linestyle not sent, set it to 'none' for no line
        if 'linestyle' in kw:
            linestyle = kw['linestyle']
            if linestyle is None:
                kw['linestyle'] = 'none'
            elif 'cycle' in linestyle:
                kw.pop('linestyle')
        else:
            kw['linestyle'] = 'none'

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().errorbar(*args, **kw)

    def curve(self, *args, **kw):

        if 'linestyle' in kw and kw['linestyle'] == 'cycle':
            kw.pop('linestyle')

        # if linestyle not sent, set it to 'none' for no line
        if 'marker' in kw:
            marker = kw['marker']
            if marker is None:
                kw['marker'] = None
            elif 'cycle' in marker:
                kw.pop('marker')
        else:
            kw['marker'] = None

        kw['marker'] = None

        if 'color' in kw:
            if kw['color'] in COLORS:
                kw['color'] = COLORS[kw['color']]

        return super().plot(*args, **kw)

    def function(
        self,
        func,
        range=None,
        npts=100,
        **kw
    ):

        if range is None:
            range = self._viewLim.intervalx

        x = np.linspace(range[0], range[1], npts)

        if callable(func):
            y = func(x)
        else:
            y = eval(func)

        return self.curve(x, y, **kw)

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

            bins = int(round((range[1] - range[0]) / binsize))
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
            self.yaxis.set_major_formatter(HickoryLogFormatter())
        elif value == 'linear':
            self.yaxis.set_major_formatter(HickoryScalarFormatter())

        return ret

    def set_xscale(self, value, **kwargs):
        ret = super().set_xscale(value, **kwargs)
        if value == 'log':
            self.xaxis.set_major_formatter(HickoryLogFormatter())
        elif value == 'linear':
            self.xaxis.set_major_formatter(HickoryScalarFormatter())

        return ret

    def set(self, margin=None, **kw):
        if margin is not None:
            kw['xmargin'] = margin
            kw['ymargin'] = margin
        super().set(**kw)
