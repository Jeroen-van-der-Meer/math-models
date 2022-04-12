#!/usr/bin/env python

import field
import simulate

"""
To do:
- Possible memory problems? Might be that save_count = None fixes it? No! In fact, it's more than just FuncAnimation: the simulation is also capable of crashing.
	Solution: One major point would be to not save each frame's grid but to save the update (as a dictionary...) and reconstruct the simulation when running the animation.
	Alternative approach: Save things in temporary data files. Why I want this: I would like a very long simulation to illustrate on YT. But this is a pain to pull off.
- Add other messages. (X is dominant)
"""

while True:
	mode = input("Would you like to simulate on a map? [y/n]\nWithout a map, the simulation will proceed on a blank field.\n")
	if mode in ['y', 'n', 'Y', 'N', 'yes', 'no', 'true', 'false', 'True', 'False']:
		break
	else:
		print("Invalid input; please try again.")

if mode in ['y', 'Y', 'yes', 'Yes', 'true', 'True']:
	real_mode = True
elif mode in ['n', 'N', 'no', 'No', 'false', 'False']:
	real_mode = False

while True:
	size = input("Enter field size. [0--3]\nLarger field takes longer to compute.\n")
	if size in ['0', '1', '2', '3']:
		size = int(size)
		break
	else:
		print("Invalid input; please try again.")

if real_mode:
	while True:
		granularity = input("Enter granularity of the map. [0--3]\nLarger granularity means more features on the map.\n")
		if granularity in ['0', '1', '2', '3']:
			granularity = int(granularity)
			break
		else:
			print("Invalid input; please try again.")
else:
	granularity = 2 #Just set it to a random value

while True:
	spawn_rate = input("Enter the rate of empire creation. [0--3]\nA higher rate has little impact on simulation speed.\n")
	if spawn_rate in ['0', '1', '2', '3']:
		spawn_rate = int(spawn_rate)
		break
	else:
		print("Invalid input; please try again.")

while True:
	strength = input("Enter strength of the empires. [0--3]\nGreater strength means bigger and longer-lasting empires.\n")
	if strength in ['0', '1', '2', '3']:
		strength = int(strength)
		break
	else:
		print("Invalid input; please try again.")

playing_field = field.Field(real_mode = real_mode, size = size, granularity = granularity, spawn_rate = spawn_rate, strength = strength)

iterations = int(input("Enter the amount of iterations you want to simulate.\nRecommended input within range [100--1000].\n"))

output = input("Give a name to the output video.\nMake sure not to choose an existing file name, lest it be overwritten.\n")

simulate.simulate(input_field = playing_field, iterations = iterations, output = output)
