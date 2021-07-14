import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import matplotlib.font_manager as font_manager
import time
import field
from tqdm import tqdm

history = 100 * field.slow_factor #This tracks how many frames the graphs show.

start = time.time()

def simulate(field, iterations, output):
	"""
	Create an animation based on the following data:
		- A list of numpy arrays forming the field at any given timeframe.
		- Counts of the population at a given timeframe.
		- Messages that we must display at a given timeframe.
	"""
	print("Starting simulation...")
	data = []
	population_count = []
	messages = []

	for i in tqdm(range(iterations)):
		field.iterate()
		data.append(np.copy(field.inhabitants))
		census = [empire.count for empire in field.empires] #Notice that this list becomes longer as we go on.
		population_count.append(census)
		messages.append(field.messages)
	
	print("Post-processing data...")
	#Post-processing population_count: make the list equally long and add a history of trailing zeros.
	empire_count = len(population_count[-1])
	processed_count = [[0 for _ in range(empire_count)] for _ in range(history)]
	for census in population_count:
		length = len(census)
		census = census + [0] * (empire_count - length)
		processed_count.append(census)

	print("Preparing animation...")
	#Initiate figure to draw on
	font = font_manager.FontEntry(fname = 'df.ttf', name = 'Dwarven MS')
	font_manager.fontManager.ttflist.insert(0, font)
	plt.rcParams['font.family'] = font.name
	fig = plt.figure(figsize = (20, 10))
	fig.set_facecolor('black')
	ax1 = plt.subplot(2, 2, (1, 3))
	ax2 = plt.subplot(2, 2, 2)
	ax3 = plt.subplot(2, 2, 4)
	ax1.axis('off')
	ax2.axis('off')
	ax3.axis('off')
	max_y = max([max(processed_count[i][1 : ]) for i in range(history + iterations)])
	ax2.set_ylim([0, max_y + 1])
	ax3.axis([0, 1, 0, 21])
	plt.tight_layout()

	#Create colour map
	colour_list = [empire.colour for empire in field.empires]
	cmap = colors.ListedColormap(colour_list)
	boundaries = [n - 1/2 for n in range(empire_count + 1)]
	norm = colors.BoundaryNorm(boundaries, cmap.N, clip = True) #cmap.N?

	#Create first frame
	print("Drawing initial frame...")
	if field.real_mode:
		im1 = ax1.imshow(field.heights, cmap = 'terrain')
	im1 = ax1.imshow(data[0], cmap = cmap, norm = norm, alpha = 0.85)

	im2s = {}
	for n in range(1, empire_count):
		im2, = ax2.plot([processed_count[i][n] for i in range(history)], color = colour_list[n])
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
		save_progress_bar.update(1)
		im1.set_array(data[frame])
		update = (im1,)

		for n in range(1, empire_count):
			im2s[n].set_data(range(history), [processed_count[i + frame][n] for i in range(history)])
			update += (im2s[n],)

		for message in messages[frame]:
			news_log.append(message)
			del news_log[0]
		for i in range(10):
			im3s[i].set_text(news_log[i][1])
			im3s[i].set_color(colour_list[news_log[i][0]])
			update += (im3s[i],)
		
		top10 = sorted(range(1, empire_count), key = lambda i : processed_count[history + frame][i], reverse = True)[ : 10]
		for i in range(len(top10)): #The length might be <10 if there were < 10 empires overall
			value = processed_count[history + frame][top10[i]]
			if value > 0:
				im4s[i].set_text(field.empires[top10[i]].name + ": " + str(value))
				im4s[i].set_color(colour_list[top10[i]])
				update += (im4s[i],)
			else:
				break

		return update

	#Create animation
	print("Creating animation...")
	ani = animation.FuncAnimation(fig, updatefig, frames = iterations, save_count = 0) #Additional things?

	#Save the animation
	with tqdm(total = iterations + 1) as save_progress_bar:
		ani.save(output + '.mp4', fps = 15) #Additional things?
	print("Done!")

	end = time.time()

	print("Time elapsed:", end - start, "seconds.")
