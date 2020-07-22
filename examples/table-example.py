import numpy as np
from hickory import Table, get_color_cycler


def main():
    seed = 8312
    rng = np.random.RandomState(seed)

    tab = Table(
        figsize=[6.4, 6.4],
        nrows=2, ncols=2,
    )

    ccycler = get_color_cycler()

    n = 40
    x = np.linspace(-1, 1, n)
    err = 0.3

    # row, col, power law index
    indexes = [
        (0, 0, 1),
        (0, 1, 2),
        (1, 0, 3),
        (1, 1, 4),
    ]

    for ti in indexes:
        row, col, pindex = ti

        ytrue = x**pindex
        y = ytrue + rng.normal(scale=err, size=n)
        yerr = ytrue*0 + err

        plt = tab[row, col]
        plt.errorbar(x, y, yerr=yerr, color=next(ccycler))
        plt.plot(
            x, ytrue, marker=None, linestyle='-',
            color=next(ccycler),
        )
        plt.set(
            xlabel=r'$x [\mathrm{cm}]$',
            ylabel=r'$x^%d$' % pindex,
        )
        plt.set_aratio(1.0)

    tab.show()


if __name__ == '__main__':
    main()
