# hickory

Python plotting library, wrapping matplotlib to provide a simpler and robust
user experience.

## examples 

```python
import hickory

# convenience function for plotting x/y.  Shown on the screen
# by default (show=True)
hickory.plot(x, y)
hickory.plot(x, y, yerr=yerr)
hickory.plot(x, y, yerr=yerr, file='test.png')

# convenience function for plotting histograms
hickory.plot_hist(data, binsize=0.1)
hickory.plot_hist(data, bins=20)

# object oriented tools
plt = hickory.Plot()
plt.plot(x, y, yerr=yerr)

plt = hickory.Plot(
    xlabel=r'$x ~[\mathrm{cm}]$',
    ylabel=r'$\Sigma$',
)
plt.plot(x, y, yerr=yerr, marker='d', linestyle='-')
plt.show()

# table of plots, 2x2
tab = hickory.Table(nrows=2, ncols=2)
tab[0, 0].plot(x, y)
tab[0, 1].plot(x, y**2)
tab[1, 0].plot(x, y**3)
tab[1, 1].plot(x, y**4)
tab.show(dpi=100)
tab.savefig('test.png', dpi=150)
```

## requirements

- numpy
- matplotlib
- Optional dependency: pillow and Tkinter for viewing plots on screen
