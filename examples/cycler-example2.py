"""
Use explicit cyclers for colors, lines and markers
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
x = np.linspace(-1, 1, n)

plt = Plot(
    xlabel='$x$',
    ylabel='$y$',
    legend=Legend(loc='upper left'),
)

lcycler = get_line_cycler(lines=['-', 'dashed', 'dotted'])
mcycler = get_marker_cycler(markers=['o', 'd', '^'])
ccycler = get_color_cycler(colors=['blue', 'red', 'orange'])

for fac in [1, 2, 3]:
    label = r'$y = %d \times x$' % fac

    y = x*fac

    plt.plot(
        x, y, label=label,
        marker=next(mcycler),
        linestyle=next(lcycler),
        color=next(ccycler),
        markeredgecolor='black',
        alpha=0.5,
    )

plt.show()
