from .plot_containers import Plot
from .data_containers import Points


def plot(x, y, xerr=None, yerr=None,
         marker='o',
         linestyle=None,
         linewidth=None,
         color=None,
         edgecolor=None,
         edgewidth=None,
         size=None,
         alpha=None,
         capsize=2,
         xlabel=None, ylabel=None,
         plt=None, show=False, dpi=None):

    if plt is None:
        plt = Plot(
            xlabel=xlabel,
            ylabel=ylabel,
        )
    assert isinstance(plt, Plot)

    pts = Points(
        x, y, xerr=xerr, yerr=yerr,
        marker=marker,
        size=size,
        linestyle=linestyle,
        linewidth=linewidth,
        color=color,
        edgecolor=edgecolor,
        alpha=alpha,
        capsize=capsize,
    )
    plt.add(pts)

    if show:
        plt.show(dpi=dpi)

    return plt
