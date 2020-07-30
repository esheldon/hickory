from .plot_containers import Plot
from .configuration import config


def plot(
    x, y, xerr=None, yerr=None,
    xlabel=None,
    ylabel=None,
    title=None,
    xlim=None,
    ylim=None,
    xlog=False,
    ylog=False,
    aratio=None,
    legend=None,
    plt=None,

    figsize=None,
    dpi=None,
    facecolor=None,
    edgecolor=None,
    linewidth=0.0,
    frameon=None,
    subplotpars=None,  # default to rc
    tight_layout=None,  # default to rc figure.autolayout
    constrained_layout=None,  # default to rc

    **kw
):
    """
    make a plot

    Parameters
    ----------
    x: array or sequences
        Array of x values
    y: array or sequences
        Array of y values
    xerr: array or sequence, optional
        Optional array of x errors
    yerr: array or sequence, optional
        Optional array of y errors

    xlabel: str, optional
        Label for x axis
    ylabel: str, optional
        Label for y axis
    title: str, optional
        Title string for plot
    xlim: 2-element sequence, optional
        Optional limits for the x axis
    ylim: 2-element sequence, optional
        Optional limits for the y axis
    xlog: bool, optional
        If True, use log x axis
    ylog: bool, optional
        If True, use log y axis
    aratio: float, optional
        Axis ratio of plot, ysize/xsize
    legend: bool or Legend instance
        If True, a legend is created. You can also send a Legend() instance.
        If None or False, no legend is created
    plt: Plot instance, optional
        If sent, a new Plot is not created, the input one
        is reused

    show: bool, optional
        If True, show the plot on the screen.  If the file= is
        not sent, this defaults to True.  If file= is sent
        this defaults to False
    file: str, optional
        Filename to write.

    Keywords for the Plot/matplotlib Figure.  See docs for
        the matplotlib Figure class

        figsize dpi facecolor edgecolor linewidth
        frameon subplotpars tight_layout constrained_layout

    Keywords for plot or errorbar, depending if xerr/yerr
    are sent.  See docs for matplotlib axes.plot and errorbar
    commands

    Returns
    -------
    Plot instance
    """
    file = kw.pop('file', None)
    if file is not None:
        show_default = False
    else:
        show_default = True

    show = kw.pop('show', config['show'])

    if plt is None:
        axis_kw = {
            'xlabel': xlabel,
            'ylabel': ylabel,
            'title': title,
        }
        if xlim is not None:
            axis_kw['xlim'] = xlim
        if ylim is not None:
            axis_kw['ylim'] = ylim
        if xlog:
            axis_kw['xscale'] = 'log'
        if ylog:
            axis_kw['yscale'] = 'log'

        plt = Plot(
            aratio=aratio,
            legend=legend,
            figsize=figsize,
            dpi=dpi,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            frameon=frameon,
            subplotpars=subplotpars,
            tight_layout=tight_layout,
            constrained_layout=constrained_layout,  # default to rc
            **axis_kw
        )

    if xerr is not None or yerr is not None:
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, **kw)
    else:
        plt.plot(x, y, **kw)

    if file is not None:
        plt.savefig(file)

    if show:
        plt.show()

    return plt


def plot_hist(
    x,
    binsize=None,
    bins=None,
    range=None,
    min=None,
    max=None,
    xlabel=None,
    ylabel=None,
    xlim=None,
    ylim=None,
    aratio=None,
    legend=None,
    figsize=None,
    dpi=None,
    facecolor=None,
    edgecolor=None,
    linewidth=0.0,
    frameon=None,
    subplotpars=None,  # default to rc
    tight_layout=None,  # default to rc figure.autolayout
    constrained_layout=None,  # default to rc
    plt=None,
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
        Optional bins keywords.  Can be an integer number of bins or the bin
        edges.  See matplotlib ax.hist documentation
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

    xlabel: str, optional
        Label for x axis
    ylabel: str, optional
        Label for y axis
    title: str, optional
        Title string for plot
    xlim: 2-element sequence, optional
        Optional limits for the x axis
    ylim: 2-element sequence, optional
        Optional limits for the y axis
    aratio: float, optional
        Axis ratio of plot, ysize/xsize
    legend: bool or Legend instance
        If True, create a legend, or you can send
        a Legend() instance.  If None or False, no legend
        is created
    plt: Plot instance, optional
        If sent, a new Plot is not created, the input one
        is reused

    show: bool, optional
        If True, show the plot on the screen.  If the file= is
        not sent, this defaults to True.  If file= is sent
        this defaults to False
    file: str, optional
        Filename to write.

    Keywords for the Plot/matplotlib Figure.  See docs for
        the matplotlib Figure class

        figsize dpi facecolor edgecolor linewidth
        frameon subplotpars tight_layout constrained_layout

    Additional keywords for ax.hist command. See docs for matplotlib axes.hist
    command for details

    Returns
    -------
    Plot instance
    """

    file = kw.pop('file', None)
    if file is not None:
        show_default = False
    else:
        show_default = True

    show = kw.pop('show', config['show'])

    if plt is None:
        plt = Plot(
            xlabel=xlabel,
            ylabel=ylabel,
            aratio=aratio,
            legend=legend,
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

    plt.hist(
        x,
        binsize=binsize,
        bins=bins,
        range=range,
        min=min,
        max=max,
        **kw)

    if file is not None:
        plt.savefig(file)

    if show:
        plt.show()

    return plt
