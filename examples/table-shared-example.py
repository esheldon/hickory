import numpy as np
from hickory import Table

seed = 5
rng = np.random.RandomState(seed)

n = 40
x = np.linspace(-2, 2, n)
err = 0.5
y1 = x**3 + rng.normal(scale=err, size=x.size)
y1err = y1*0 + err
y2 = y1 - x**3
y2err = y1err

tab = Table(
    figsize=[5, 5.5],
    nrows=2, ncols=1,
    sharex=True,
    gridspec_kw={'height_ratios': [0.8, 0.2]},
)

tab[0].errorbar(x, y1, yerr=y1err, markeredgecolor='black')
tab[0].plot(x, x**3, marker=None, linestyle='-')
tab[0].set(ylabel=r'$\Sigma$')

tab[1].errorbar(x, y2, yerr=y2err, markeredgecolor='black')
tab[1].axhline(0)
tab[1].set(
    ylim=(-2.1, 2.1),
    xlabel=r'$x [\mathrm{cm}]$',
    ylabel=r'$\Delta$',
)
tab.show()
