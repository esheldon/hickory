"""
Use explicit cyclers for colors, lines and markers
"""

import numpy as np
from hickory import Plot, Legend, MultiCycler


n = 10
x = np.linspace(-1, 1, n)

# cycling linesyles, markers, colors and also applying
# markeredgecolor and alpha for all
cycler = MultiCycler(
    linestyle=['solid', 'dashed', 'dotted'],
    marker=['o', 'd', '^'],
    color=['teal', 'red', 'orange'],
)

plt = Plot(
    xlabel='$x$',
    ylabel='$y$',
    cycler=cycler,
    legend=True,
)

for fac in [1, 2, 3]:
    label = r'$y = %d \times x$' % fac

    y = x*fac

    # the plot() command does not show line by default.  Setting to 'cycle'
    # tells it to use the specified cycler
    plt.plot(x, y, label=label, linestyle='cycle', markeredgecolor='black')

plt.show()
