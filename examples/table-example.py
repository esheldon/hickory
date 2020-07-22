"""
basic table example
"""
import numpy as np
from hickory import Table, get_color_cycler, get_marker_cycler


seed = 8312
rng = np.random.RandomState(seed)

tab = Table(
    figsize=[6.4, 6.4],
    nrows=2, ncols=2,
)

ccycler = get_color_cycler()
mcycler = get_marker_cycler()

n = 20
x = np.linspace(-1, 1, n)
err = 0.3

# iterate over subplots
for i, plt in enumerate(tab):
    pindex = i+1

    ytrue = x**pindex
    y = ytrue + rng.normal(scale=err, size=n)
    yerr = ytrue*0 + err

    plt.errorbar(
        x, y, yerr=yerr,
        marker=next(mcycler),
        color=next(ccycler),
        markeredgecolor='black',
    )
    plt.plot(
        x, ytrue, marker=None, linestyle='-',
        color=next(ccycler),
    )
    plt.set(
        xlabel=r'$x [\mathrm{cm}]$',
        ylabel=r'$x^%d$' % pindex,
        margin=0.2,
    )
    plt.set_aratio(1.0)

tab.show()
tab.savefig('table-example.pdf')
