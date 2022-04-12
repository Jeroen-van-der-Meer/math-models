import numpy as np
import math
from itertools import product

def random_gradient():
	"""Create a random 2-dimensional unit gradient vector."""
	random_x = np.random.normal() #Gaussian coordinate sampling yields uniform distribution on unit circle
	random_y = np.random.normal()
	norm = math.sqrt(random_x**2 + random_y**2)
	return (random_x / norm, random_y / norm)

def nearby_grid_points(point, stepsize):
	"""Given a point in 2-dimesnional space, return the 4 closest grid points on which the gradients are to be placed."""
	left = point[0] - point[0] % stepsize
	right = left + stepsize
	up = point[1] - point[1] % stepsize
	down = up + stepsize
	return [(left, up), (left, down), (right, up), (right, down)]

def dot(v, w):
	return (v[0] * w[0] + v[1] * w[1])

def lerp(a, b, t):
    """Linear interpolation function between a and b."""
    return a + t * (b - a)

def fade(t):
    """Smooth curve with vanishing derivative at 0 and 1."""
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def perlin_noise(size = 100, stepsize = 5):
	"""This function creates a 2-dimensional square of dimensions given by size, with a value on each coordinate determined by Perlin noise. To do so, we create a grid, whose size is specified by stepsize, and we attach a random unit vector to each grid point. We then compute the influence at each point in our space, in terms  of dot products with the gradients. This we output."""
	# Let's begin by creating a random gradient field
	gradient_field = {x : random_gradient() for x in product(range(0, size + stepsize, stepsize), repeat = 2)}

	# Next, we create our output field
	output = np.zeros((size, size))

	for x in range(size):
		for y in range(size):
			# At each point in our coordinate field, we calculate the influences at the four neighbouring grid points, and then we interpolate, first horizontally, then vertically
			dx = x % stepsize
			left = x - dx
			right = left + stepsize

			dy = y % stepsize
			down = y - dy
			up = down + stepsize

			influence_1 = dot(gradient_field[(left, down)], (dx, dy))
			influence_2 = dot(gradient_field[(left, up)], (dx, dy - stepsize))
			influence_3 = dot(gradient_field[(right, down)], (dx - stepsize, dy))
			influence_4 = dot(gradient_field[(right, up)], (dx - stepsize, dy - stepsize))
			
			ratio_x = fade(dx / stepsize)
			ratio_y = fade(dy / stepsize)
			
			h_interpolate_1 = lerp(influence_1, influence_3, ratio_x)
			h_interpolate_2 = lerp(influence_2, influence_4, ratio_x)

			v_interpolate = lerp(h_interpolate_1, h_interpolate_2, ratio_y)

			output[x, y] = v_interpolate
	
	return output
 
"""
The final function will require only two inputs from the user: a size parameter between 0 and 3, and a 'granularity' parameter between 0 and 3. The latter controls the step size of the Perlin functions invoked.

Although we use Perlin noise as the main mathematical tool for producing the landscape, we want to manually tweak some things to make things according to our wishes. For instance, we want to force the land to become ocean as we're nearing the border, and we want to normalise the values to lie between 0 and 1. The precise normalisation constant, however, depends on the step sizes of the Perlin noise functions, and since these in turn depend on the user's chosen parameter, it is best to just determine the appropriate constants heuristically.

In the dictionary below, the first output yields the true map size; the second output yields the smallest step size of the Perlin noise functions; and the third output is the normalisation factor.
"""
parameter_guide = {(0, 0): [128, 15, 20], (0, 1): [128, 10, 20], (0, 2): [128, 5, 12], (0, 3): [128, 2, 10],
		(1, 0): [256, 30, 40], (1, 1): [256, 20, 35], (1, 2): [256, 10, 20], (1, 3): [256, 5, 12],
		(2, 0): [512, 60, 70], (2, 1): [512, 40, 50], (2, 2): [512, 20, 30], (2, 3): [512, 10, 20],
		(3, 0): [1024, 120, 140], (3, 1): [1024, 80, 80], (3, 2): [1024, 40, 50], (3, 3): [1024, 20, 30]}

def grid(size = 1, granularity = 1):
	"""Produces a height grid based on Perlin noise function."""
	s = parameter_guide[(size, granularity)][0]
	st = parameter_guide[(size, granularity)][1]
	factor = parameter_guide[(size, granularity)][2]
	
	f1 = perlin_noise(size = s, stepsize = st)
	f2 = perlin_noise(size = s, stepsize = st + 5)
	f3 = perlin_noise(size = s, stepsize = st + 9)
	output = np.zeros((s, s))
	
	h = s // 2
	for x in range(s):
		for y in range(s):
			perlin_output = f1[x, y] + f2[x, y] + f3[x, y]
			perlin_output /= factor
			perlin_output += 0.5
			border_correction = ((x - h)**2 + (y - h)**2) / h**2
			total = perlin_output - border_correction
			if total > 1:
				output[x, y] = 1
			elif total < 0:
				output[x, y] = 0
			else:
				output[x, y] = total
	return output

