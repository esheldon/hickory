from .plot_containers import Plot
from .data_containers import (
    Points,
    Function,
)


def plot(
    x,
    y=None,
    xerr=None,
    yerr=None,
    plt=None,
    show=True,
    viewer='feh',
    file=None,
    dpi=150,
):
    """
    plot data or a function

    TODO docs
    """
    if plt is None:
        plt = Plot()

    if isinstance(x, str):
        obj = Function(x)
    else:
        assert y is not None
        obj = Points(x, y, xerr=xerr, yerr=yerr)

    plt.add(obj)

    if file is not None:
        plt.write(file, dpi=dpi)

    if show:
        plt.show(dpi=dpi, viewer=viewer)

    return plt
