import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import matplotlib.font_manager as font_manager
import time
import field
from tqdm import tqdm

history = 100 * field.slow_factor #This tracks how many frames the graphs show.

start = time.time()

def simulate(input_field, iterations, output):
	"""
	We're given a playing field, and a number of iterations to let the playing field do its thing.
	We simulate the game and we capture the relevant data at each time frame.
	Then we take this information and we create an animation using Matplotlib.
	"""
	#Initialise the datasets.
	data = np.copy(input_field.inhabitants) #Field on first frame
	data_updates = [] #This will contain the playing field info at every timeframe
	population_count = [] #Keeps track of the population sizes of every empire
	messages = [] #Holds the messages that need to be displayed

	#Run the simulation.
	print("Starting simulation...")
	for i in tqdm(range(iterations), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'): #tqdm() generates a progress bar
		input_field.iterate()
		data_updates.append(input_field.update.copy()) #We keep track of the updates of the field.
		census = [empire.count for empire in input_field.empires] #Notice that this list becomes longer as we go on
		population_count.append(census)
		messages.append(input_field.messages)

	print("Post-processing data...")
	#Post-processing population_count: make the list equally long and add a history of trailing zeros.
	empire_count = len(population_count[-1])
	processed_count = [[0 for _ in range(empire_count)] for _ in range(history)]
	for census in population_count:
		length = len(census)
		census = census + [0] * (empire_count - length)
		processed_count.append(census)
	#Post-processing messages.
	processed_messages = [[] for _ in range(iterations)]
	for i in range(iterations):
		for message in messages[i]:
			if message[1] == 0:
				p = random.choice(range(2))
				if p == 0:
					processed_messages[i].append([message[0], input_field.empires[message[0]].name + ' has perished!'])
				else:
					processed_messages[i].append([message[0], input_field.empires[message[0]].name + ' has collapsed!'])
			elif message[1] == 1:
				p = random.choice(range(2))
				if p == 0:
					processed_messages[i].append([message[0], input_field.empires[message[0]].name + ' was established!'])
				else:
					processed_messages[i].append([message[0], input_field.empires[message[0]].name + ' was founded!'])
			elif message[1] == 2:
				processed_messages[i].append([message[0], input_field.empires[message[0]].name + ' reached the age of ' + str(input_field.milestone) +'.'])
			elif message[1] == 3 and i > 50 * field.slow_factor and message not in messages[i - 1]:
					processed_messages[i].append([message[0], input_field.empires[message[0]].name + ' is dominating the world!'])

	#We now initiate figure to draw on.
	print("Preparing animation...")
	font = font_manager.FontEntry(fname = 'df.ttf', name = 'Dwarven MS') #Font file lives in same directory
	font_manager.fontManager.ttflist.insert(0, font)
	plt.rcParams['font.family'] = font.name
	fig = plt.figure(figsize = (20, 10), dpi = 144)
	fig.set_facecolor('black')
	ax1 = plt.subplot(2, 2, (1, 3)) #This will be the playing field
	ax2 = plt.subplot(2, 2, 2) #This will plot the population sizes
	ax3 = plt.subplot(2, 2, 4) #This will contain all messages
	ax1.axis('off')
	ax2.axis('off')
	ax3.axis('off')
	max_y = max([max(processed_count[i][1 : ]) for i in range(history + iterations)]) #Determine range of population size plot (would be wrongly determined on frame 0 otherwise)
	ax2.set_ylim([0, max_y + 1])
	ax3.axis([0, 1, 0, 21]) #Ten lines for news messages; ten lines for the populations of the ten largest empires; one empty line in between
	plt.tight_layout()

	#Create colour map.
	colour_list = [empire.colour for empire in input_field.empires] #Every empire has its own colour which we now import
	cmap = colors.ListedColormap(colour_list)
	boundaries = [n - 1/2 for n in range(empire_count + 1)] #Half-integer value to prevent rounding problems
	norm = colors.BoundaryNorm(boundaries, cmap.N, clip = True)

	#Create first frame.
	print("Drawing initial frame...")
	if input_field.real_mode:
		im1 = ax1.imshow(input_field.heights, cmap = 'terrain')
	im1 = ax1.imshow(data, cmap = cmap, norm = norm, alpha = 0.85)

	im2s = {}
	for n in range(1, empire_count):
		im2, = ax2.plot([processed_count[i][n] for i in range(history)], color = colour_list[n]) #Matplotlib will kill you if you remove the ,
		im2s[n] = im2

	im3s = {}
	news_log = [[0, ""] for i in range(10)]
	for i in range(10):
		im3 = ax3.text(0, i, news_log[i], color = 'white', fontsize = 16)
		im3s[i] = im3
	
	im4s = {}
	for i in range(10):
		im4s[i] = ax3.text(0, 20 - i, "", color = 'white', fontsize = 16)
	
	def updatefig(frame):
		"""This function specifies how the animation should progress."""
		save_progress_bar.update(1)

		for x in data_updates[frame]:
			data[x] = data_updates[frame][x]
		im1.set_array(data)
		update = (im1,)

		for n in range(1, empire_count):
			im2s[n].set_data(range(history), [processed_count[i + frame][n] for i in range(history)])
			update += (im2s[n],)

		for message in processed_messages[frame]:
			news_log.append(message)
			del news_log[0]
		for i in range(10):
			im3s[i].set_text(news_log[i][1])
			im3s[i].set_color(colour_list[news_log[i][0]])
			update += (im3s[i],)
		
		top10 = sorted(range(1, empire_count), key = lambda i : processed_count[history + frame][i], reverse = True)[ : 10]
		for i in range(len(top10)): #The length might be <10 if there were < 10 empires overall which is why we don't write range(10)
			value = processed_count[history + frame][top10[i]]
			if value > 0:
				im4s[i].set_text(input_field.empires[top10[i]].name + ": " + str(value))
				im4s[i].set_color(colour_list[top10[i]])
				update += (im4s[i],)
			else: #Don't display empires with population 0
				break

		return update

	#Create animation
	print("Creating animation...")
	ani = animation.FuncAnimation(fig, updatefig, frames = iterations, init_func = lambda : None, save_count = None) #The init_func prevents updatefig(0) from being evaluated twice; the save_count = 0 should (I think) prevent memory issues.

	#Save the animation
	FFWriter = animation.FFMpegWriter(fps = 15, extra_args = ['-vcodec', 'libx265']) #libx265 > libx264
	with tqdm(total = iterations, bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}') as save_progress_bar:
		ani.save(output + '.mp4', writer = FFWriter)
	print("Done!")

	end = time.time()

	print("Time elapsed:", end - start, "seconds.")
