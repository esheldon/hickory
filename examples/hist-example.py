import numpy as np
from hickory import Plot

seed = 1253
rng = np.random.RandomState(seed)
vals1 = rng.normal(size=10000, scale=0.3)
vals2 = rng.normal(size=15000, loc=0.9)

plt = Plot(xlabel=r'$\Sigma ~[\mathrm{cm}]$', ylabel='Number')

binsize = 0.1
alpha = 0.5
plt.hist(
    vals1,
    binsize=binsize,
    alpha=alpha,
)
plt.hist(
    vals2,
    binsize=binsize,
    alpha=alpha,
)

plt.show()

