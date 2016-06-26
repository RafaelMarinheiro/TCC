# the function to be plotted
import math
import numpy as np
import matplotlib.pyplot as plt

MY_PI = math.acos(-1)

def habs(x,y):
	f = 40
	dist = np.sqrt(x*x+y*y)
	return 1/(4*MY_PI*(dist + 0.001))

def hre(x,y):
	f = 40
	dist = np.sqrt(x*x+y*y)
	return np.cos(40*dist)/(4*MY_PI*(dist + 0.001))

x = np.linspace(-1,1,500)
y = np.linspace(-1,1,500)

X, Y = np.meshgrid(x, y)

def plot(f, vmin, vmax, name):
	Z = f(X, Y)
	fig = plt.figure(figsize=(6, 6), dpi=100) 
	ax = fig.add_subplot(1,1,1)

	ax.tick_params(
	    axis='x',          # changes apply to the x-axis
	    which='both',      # both major and minor ticks are affected
	    bottom='off',      # ticks along the bottom edge are off
	    top='off',         # ticks along the top edge are off
	    labelbottom='off') # labels along the bottom edge are off

	ax.tick_params(
	    axis='y',          # changes apply to the x-axis
	    which='both',      # both major and minor ticks are affected
	    left='off',      # ticks along the bottom edge are off
	    right='off',         # ticks along the top edge are off
	    labelleft='off') # labels along the bottom edge are off

	mappable = ax.pcolor(X, Y, Z/1.2, cmap="seismic", vmin=vmin, vmax=vmax)

	ax.axis([x.min(), x.max(), y.min(), y.max()])
	ax.set_aspect('equal')
	fig.colorbar(mappable, ax=ax, orientation='horizontal')
	fig.savefig(name, bbox_inches='tight')
	plt.close(fig)

plot(hre, -1, 1, "helmholtz_re")
plot(habs, 0, 1, "helmholtz_abs")

