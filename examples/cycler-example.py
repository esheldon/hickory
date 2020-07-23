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

xlabel = r'$D ~[\mathrm{cm}]$'
ylabel = r'$\xi ~[\mathrm{kg}]$'
plt = Plot(
    xlabel=xlabel,
    ylabel=ylabel,
    legend=Legend(loc='upper left'),
)

# Colors and markers are automatically cycled.  Let's cycle
# both markers and linestyles
lcycler = get_line_cycler()
mcycler = get_marker_cycler()
ccycler = get_color_cycler()

for p in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    dlab = r'$\mathrm{data%d}$' % p
    clab = r'$y = x^%d$' % p

    ytrue = x**p
    y = ytrue

    plt.plot(
        x, y, label=dlab,
        marker=next(mcycler),
        linestyle=next(lcycler),
        color=next(ccycler),
        # markeredgecolor='black',
    )

plt.axhline(0, color='black', linewidth=1)
plt.show(dpi=150)
