"""
Simple example using the plot convenience function
"""

import numpy as np
from hickory import plot

x = np.linspace(0, 1, 10)
y = x**2

plot(x, y, xlabel='distance', ylabel='value')
