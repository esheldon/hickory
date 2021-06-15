# hickory

Python plotting library, wrapping matplotlib to provide a simple and robust
user experience.

Features

- Plot class provides the functionality of matplotlib Figure but with a simpler interface.
    - The plotting commands, as well as figure saving and viewing are available directly from the Plot object.
    - No need to deal with Figure and Axes separately
- Table class represents subplots in a simpler way.
    - Access to the array of subplots is available directly from the Table
    - No need to carry around both fig and axes separately.
- Plots can be shown on the screen without using one of the matplotlib viewer toolkits as the backend (e.g. GTK).
    - This is an improvement over matplotlib where the library will fail to import if a display is not found, *even if no plot is ever made*.
    - Hickory can import fine with and without a display, no need for altering backends depending on the environment.

- 
## examples 

```python
import hickory

# convenience function for plotting x/y.

# show plot on the screen
hickory.plot(x, y)
hickory.errorbar(x, y, yerr=yerr)

# write a file with no plot on screen
hickory.errorbar(x, y, yerr=yerr, file='test.png')

# write a file and show on the screen
hickory.errorbar(x, y, yerr=yerr, show=True, file='test.png')

# convenience function for plotting histograms
hickory.plot_hist(data, binsize=0.1)
hickory.plot_hist(data, bins=20)


# object oriented tools
# make a Plot object

plt = hickory.Plot()

# any matplotlib axis plotting methods are available directly
# plot and errorbar default to markers only

plt.errorbar(x, y, yerr=yerr)
plt.show(dpi=150)
plt.savefig('test.png')

# New method curve defaults to lines only
plt.curve(x, ytrue)

# New method function can plot a function represented as
# a string or callable. Defaults to lines only
plt.function('x**2', range=[x.min(), x.max()])

# set axis parameters in the constructor
plt = hickory.Plot(
    xlabel=r'$x ~[\mathrm{cm}]$',
    ylabel=r'$\Sigma$',
    xlim=(-1, 1),
)


# table of plots, 2x2
tab = hickory.Table(nrows=2, ncols=2)

# call plotting routines direclty on the table using indexing
tab[0, 0].plot(x, y)
tab[0, 1].scatter(xp, yp)
tab[1, 0].errorbar(x, x**3, yerr=yerr)
tab[1, 1].plot(x, y**4)
tab[1, 1].set(xlim=(1, 5), xlabel='x', ylabel='y')

# iterate over plots
for i, plt in enumerate(tab):
    pindex = i+1
    plt.curve(x, x**pindex)

tab.show(dpi=100)
tab.savefig('table-plot.png', dpi=150)
```

## requirements

- numpy
- matplotlib >=3.4
- Optional dependency: pillow and Tkinter for viewing plots on screen
