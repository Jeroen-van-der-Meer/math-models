import perlin
import random
import numpy as np
from itertools import product
import csv

slow_factor = 2 #Global term slowing down the simulation; used in simulation.py as well

with open('language.txt', 'r', encoding = 'CP437') as f:
	names = [row[0] for row in csv.reader(f, delimiter = '\n')] #We will be sampling from these names whenever an empire gets created

class Empire():
	"""Captures all attributes of a specific empire."""

	def __init__(self, strength = 2, count = 0, empty = False):
		"""Initialise attributes."""
		self.count = count
		self.empty = empty
		
		if not empty:
			#Attach a colour to the mpire; to ensure brightness, the colour hex value isn't picked arbitrarily
			rgb = [0, 0, 0] #initial rgb
			main, secondary = random.sample([0, 1, 2], 2)
			rgb[main] = 255
			secondary_value = random.choice(range(255))
			rgb[secondary] = secondary_value
			self.colour = "#%02X%02X%02X" %(rgb[0], rgb[1], rgb[2])

			self.strength = 2.5 + 0.25 * strength #Strength is used when determining with what probability blocks take on a certain value
			self.decrease = 0.01 * (4 - strength) / slow_factor
		else: #We treat an empty field as an empire as well, though it behaves differently
			self.colour = "black"
			self.strength = 1
		
		#Give empire a name
		name1 = random.choice(names)
		name2 = random.choice(names)
		self.name = (name1 + name2).capitalize()
		self.age = 0
	
	def nerf(self):
		if not self.empty and self.strength > 1:
			factor = random.choice([-1, -1, 1]) #There's some randomness involved in the nerf function, just to make the development a bit more interesting
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
		self.milestone = 100 * 2**self.size_param * slow_factor #If an empire reaches this age, it qualifies as impressive

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
		n = len(self.empires)
		new_empire = Empire(strength = self.strength) #Fill in stuff.
		self.empires.append(new_empire)
		self.living.append(n)
		for y in self.neighbourhood(x):
			self.inhabitants[y] = n
			new_empire.count += 1
		self.messages.append([n, 1]) #[n, 1] means message of type 1 concerning empire n

	def survival_rate(self, n, x):
		if n == 0:
			return 1
		elif not self.real_mode:
			return self.empires[n].strength #Case distinction is somewhat irrelevant but it slightly speeds up the real_mode=False simulation
		else:
			return self.empires[n].strength * self.habitability[x]

	def iterate(self):
		"""Simulate the passage of time and every bit of misery that comes with it."""
		self.update = {} #Reset the update dictionary.
		self.messages = [] #Reset the messages
		self.time += 1

		#Procedure will be slightly different depending on whether we're using a map or not.
		for x in self.partition[self.time % slow_factor]: #Only probe part of the field
			surroundings = [self.inhabitants[n] for n in self.neighbourhood(x)]
			if len(set(surroundings)) == 1: #Optimisation procedure --- ignores blocks whose neighbourhood is uniform.
				continue
			else:
				prob = [self.survival_rate(n, x) for n in surroundings]
				self.update[x] = random.choices(surroundings, weights = prob, k = 1)[0] #Appears to be significantly faster than numpy's weighted random choice

		#New empire?
		p = random.choice(range(self.spawn_rate)) #Only with some minor probability will we introduce a new empire
		if p == 0:
			x = random.choice(self.spawnable_blocks)
			self.spawn(x)

		#Finally, invoke the updates.
		for x in self.update:
			self.empires[self.inhabitants[x]].count -= 1
			self.inhabitants[x] = self.update[x]
			self.empires[self.inhabitants[x]].count += 1

		#Register deaths.
		for n in self.living[:]:
			if self.empires[n].count == 0:
				self.living.remove(n)
				self.messages.append([n, 0]) #[n, 0] means message of type 0 concerning empire n

		#Update age.
		for n in self.living:
			self.empires[n].age += 1
			if self.empires[n].age == self.milestone:
				self.messages.append([n, 2])

		#Implement nerf.
		for n in self.living:
			self.empires[n].nerf()
