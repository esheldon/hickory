"""
Use explicit cyclers for colors, lines and markers
"""

from cycler import cycler

import numpy as np
from hickory import Plot, Legend


err = 0.03
n = 10
x = np.linspace(-1, 1, n)

# cycling linesyles, markers, colors and also applying
# markeredgecolor and alpha for all
cyc = cycler(
    linestyle=['solid', 'dashed', 'dotted'],
    marker=['o', 'd', '^'],
    color=['teal', 'red', 'orange'],
) * cycler(markeredgecolor=['black']) * cycler(alpha=[0.5])

plt = Plot(
    xlabel='$x$',
    ylabel='$y$',
    cycler=cyc,
    legend=True,
)

for fac in [1, 2, 3]:
    label = r'$y = %d \times x$' % fac

    y = x*fac

    # the plot() command does not show line by default.  Setting to 'cycle'
    # tells it to use the specified cycler
    plt.plot(x, y, label=label, linestyle='cycle')

plt.show()
