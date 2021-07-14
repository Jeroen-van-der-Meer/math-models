import perlin
import random
import numpy as np
from itertools import product
import csv

slow_factor = 2

with open('language.txt', 'r', encoding = 'CP437') as f:
	names = [row[0] for row in csv.reader(f, delimiter = '\n')]

class Empire():
	def __init__(self, strength = 2, count = 0, empty = False):
		"""Initialise attributes."""
		self.count = count
		self.empty = empty
		
		if not empty:
			rands = random.choices(range(255), k = 3)

			self.colour = "#%02X%02X%02X" %(rands[0], rands[1], rands[2])

			self.strength = 2.5 + 0.25 * strength
			self.decrease = 0.01 * (4 - strength) / slow_factor
		else:
			self.colour = "black"
			self.strength = 1
		
		#Give empire a name
		name1 = random.choice(names)
		name2 = random.choice(names)
		self.name = (name1 + name2).capitalize()
	
	def nerf(self):
		if not self.empty and self.strength > 1:
			factor = random.choice([-1, -1, 1])
			#Might want to add a randomness factor to this, with some bias.
			self.strength += factor * self.decrease

class Field():
	"""The playing field for our Game of Life."""

	def __init__(self, real_mode = True, size = 1, granularity = 2, spawn_rate = 1, strength = 2):
		"""Initialise attributes."""
		#Initiate some parameters
		print("Initialising field...")
		self.size_param = size
		self.size = 128 * 2**size
		self.spawn_rate = 2**(4 - spawn_rate) * slow_factor
		self.strength = strength
		self.real_mode = real_mode
		self.time = 0

		#Initiate map if set to real mode
		if self.real_mode:
			self.heights = perlin.grid(size = self.size_param, granularity = granularity)
			self.habitability = np.zeros((self.size, self.size))
			for x in range(self.size):
				for y in range(self.size):
					self.habitability[x, y] = -abs(2 * self.heights[x, y] - 1) + 1
			self.habitable_blocks = [x for x in product(range(1, self.size - 1), repeat = 2) if self.habitability[x] > 0] #This is all we need to iterate over when updating the playing field.
			self.spawnable_blocks = [x for x in product(range(3, self.size - 3), repeat = 2) if self.habitability[x] > 0.3] #Where a new empire might spawn.
		else:
			self.habitable_blocks = [x for x in product(range(1, self.size - 1), repeat = 2)]
			self.spawnable_blocks = self.habitable_blocks

		#We partition the habitable blocks into pieces which get sampled separately during each timeframe. We do this to slow down the development of the animation.
		random.shuffle(self.habitable_blocks)
		self.partition = [self.habitable_blocks[i :: slow_factor] for i in range(slow_factor)]

		#Declare attributes related to the playing field
		self.empires = [Empire(count = self.size**2, empty = True)] #Holds all empire data.
		self.living = [] #Collection of indices of living empires.
		self.inhabitants = np.zeros((self.size, self.size), dtype = int) #Keeps track of who lives on a given square
		
		self.update = {} #Reset the update dictionary.
		self.messages = [] #Reset the messages

	def neighbourhood(self, x):
		"""Given a point x in our grid, return the points around it that we consider a 'neighbourhood' of the point."""
		x0 = x[0]
		y0 = x[1]
		return [(x0, y0),
				(x0 - 1, y0 - 1), (x0 + 1, y0 - 1), (x0 - 1, y0 + 1), (x0 + 1, y0 + 1),
				(x0 - 1, y0), (x0, y0 - 1), (x0, y0 + 1), (x0 + 1, y0)]
	
	def spawn(self, x):
		"""Introduce new empire around coordinate x."""
		#self.species_count += 1
		n = len(self.empires)
		new_empire = Empire(strength = self.strength) #Fill in stuff.
		self.empires.append(new_empire)
		self.living.append(n)
		for y in self.neighbourhood(x):
			self.inhabitants[y] = n
			new_empire.count += 1
		self.messages.append([n, new_empire.name + " has been established."])

	def survival_rate(self, n, x):
		if n == 0:
			return 1
		elif not self.real_mode:
			return self.empires[n].strength
		else:
			return self.empires[n].strength * self.habitability[x]

	def iterate(self):
		"""Simulate the passage of time and every bit of misery that comes with it."""
		self.update = {} #Reset the update dictionary.
		self.messages = [] #Reset the messages
		self.time += 1

		#Procedure will be slightly different depending on whether we're using a map or not.
		for x in self.partition[self.time % slow_factor]:
			surroundings = [self.inhabitants[n] for n in self.neighbourhood(x)]
			if len(set(surroundings)) == 1: #Optimisation procedure --- ignores blocks whose neighbourhood is uniform.
				continue
			else:
				prob = [self.survival_rate(n, x) for n in surroundings]
				self.update[x] = random.choices(surroundings, weights = prob, k = 1)[0] #Appears to be significantly faster than numpy's weighted random choice

		#New species?
		p = random.choice(range(self.spawn_rate))
		if p == 0:
			x = random.choice(self.spawnable_blocks)
			self.spawn(x)

		#Finally, invoke the updates.
		for x in self.update:
			self.empires[self.inhabitants[x]].count -= 1
			self.inhabitants[x] = self.update[x]
			self.empires[self.inhabitants[x]].count += 1

		#To do! Implement deaths.
		for n in self.living[:]:
			if self.empires[n].count == 0:
				self.living.remove(n)
				self.messages.append([n, self.empires[n].name + " has perished."])

		#Implement nerf.
		for n in self.living:
			self.empires[n].nerf()
