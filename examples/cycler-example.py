"""
Make a Plot with various markers and lines.  Use cyclers
to choose colors, lines, and markers
"""

import numpy as np
from hickory import (
    Plot,
    Legend,
    get_marker_cycler,
    get_line_cycler,
    get_color_cycler,
)


err = 0.03
n = 10
x = np.linspace(0, 1, n)
yerr = x*0 + err

xlabel = r'$r ~[h^{-1}~\mathrm{Mpc}]$'
ylabel = r'$\Delta\Sigma ~[h~\mathrm{M}_\odot]$'
plt = Plot(
    xlabel=xlabel,
    ylabel=ylabel,
    legend=Legend(loc='upper left'),
)

lcycler = get_line_cycler()
mcycler = get_marker_cycler()
ccycler = get_color_cycler()

for p in [1, 2, 3, 4]:
    dlab = r'$\mathrm{data%d}$' % p
    clab = r'$y = x^%d$' % p

    ytrue = x**p
    y = ytrue

    plt.errorbar(
        x, y, yerr=yerr, label=dlab,
        marker=next(mcycler),
        color=next(ccycler),
        alpha=0.8,
    )
    plt.plot(
        x, ytrue,
        label=clab,
        linestyle=next(lcycler),
        color=next(ccycler),
    )
plt.axhline(0, color='black', linewidth=1)
plt.show()
