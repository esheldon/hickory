# hickory

Python plotting library, wrapping matplotlib to provide a simpler and robust
user experience.

## examples 

```python
import hickory

# convenience function for plotting x/y.

# show plot on the screen
hickory.plot(x, y)
hickory.plot(x, y, yerr=yerr)

# write a file with no plot on screen
hickory.plot(x, y, yerr=yerr, file='test.png')

# write a file and show on the screen
hickory.plot(x, y, yerr=yerr, show=True, file='test.png')

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

# any matplotlib axis plotting methods are available directly
# from the Plot
plt.plot(x, y, marker='d', linestyle='-')
plt.errorbar(x, y2, yerr=yerr)
plt.show()
plt.savefig('test.png')

# table of plots, 2x2
tab = hickory.Table(nrows=2, ncols=2)

# call plotting routines direclty on the table using indexing
tab[0, 0].plot(x, y)
tab[0, 1].scatter(xp, yp)
tab[1, 0].errorbar(x, x**3, yerr=yerr)
tab[1, 1].plot(x, y**4)
tab[1, 1].set(xlim=(1, 5), xlabel='x', ylabel='y')

tab.show(dpi=100)
tab.savefig('test.png', dpi=150)
```

## requirements

- numpy
- matplotlib
- Optional dependency: pillow and Tkinter for viewing plots on screen
