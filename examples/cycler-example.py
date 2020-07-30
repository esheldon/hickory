"""
Make a Plot with various markers and lines.  Use the
automatic cyclers for colors, lines, and markers
"""

import numpy as np
from hickory import Plot, Legend


n = 10
x = np.linspace(0, 1, n)

xlabel = r'$D ~[\mathrm{cm}]$'
ylabel = r'$\xi ~[\mathrm{kg}]$'
plt = Plot(
    xlabel=xlabel,
    ylabel=ylabel,
    legend=Legend(loc='upper left'),
)

# Colors and markers are automatically cycled in the plot
# and errorbar commands. Here we set linestyle to 'cycle'
# to also use automatic cycling

for p in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    dlab = r'$\mathrm{data%d}$' % p
    clab = r'$y = x^%d$' % p

    ytrue = x**p
    y = ytrue

    # the plot() command does not show line by default.  Setting to 'cycle'
    # tells it to use the specified cycler
    plt.plot(x, y, label=dlab, linestyle='cycle', markeredgecolor='black')

plt.axhline(0, color='black', linewidth=1)
plt.show(dpi=150)
