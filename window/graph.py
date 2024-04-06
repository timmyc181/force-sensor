from matplotlib import pyplot as plt

from file_manager import Logger

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph:
	x = []
	y = []

	x_width = 200
	y_min = 0
	y_max = 10
	x_min = 0
	x_max = x_width
	margins = 0.01

	frame = 0

	def __init__(self, window):
		print('inited')
		self.fig, self.ax = plt.subplots()

		self.ax.axhline(y=8, color="red", linestyle="--", linewidth=3)
		self.line, = self.ax.plot(self.x, self.y, color='green', linewidth=2, animated=True)
		# plt.show(block=False)

		self.set_x_lim()
		self.set_y_lim()

		# get copy of entire figure (everything inside fig.bbox) sans animated artist
		self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
		# draw the animated artist, this uses a cached renderer
		self.ax.draw_artist(self.line)
		# show the result to the screen, this pushes the updated RGBA buffer from the
		# renderer to the GUI framework so you can see it

		self.canvas = FigureCanvasTkAgg(self.fig,
		                                master=window)
		self.canvas.draw()

		# self.canvas.blit(self.fig.bbox)

		self.canvas.get_tk_widget().pack()

	def set_x_lim(self):
		self.ax.set_xlim(
			left=self.x_min - self.margins * (self.x_max - self.x_min),
			right=self.x_max + self.margins * (self.x_max - self.x_min)
		)

	def set_y_lim(self):
		self.ax.set_ylim(
			bottom=self.y_min - self.margins * (self.y_max - self.y_min),
			top=self.y_max + self.margins * (self.y_max - self.y_min)
		)

	def add(self, x_val, y_val):
		# self.fig.canvas.restore_region(self.bg)
		self.x.append(x_val)
		self.y.append(y_val)

		self.manage_scale(x_val, y_val)

		self.line.set_data(self.x, self.y)
		self.ax.draw_artist(self.line)
		self.canvas.blit(self.fig.bbox)
		self.canvas.flush_events()

	def manage_scale(self, x_val, y_val):
		if y_val > self.y_max:
			# Resize y scale
			self.y_max = y_val
			self.set_y_lim()
			self.fig.canvas.draw()
		# self.fig.canvas.copy_from_bbox(self.fig.bbox)

		if x_val > self.x_max:
			# Resize x scale
			shift_by = self.x_width / 4
			self.x_max += shift_by
			self.x_min += shift_by
			self.set_x_lim()
			self.fig.canvas.draw()
