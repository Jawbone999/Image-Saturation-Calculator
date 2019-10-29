from PIL import Image, ImageTk
from tkinter import Tk, Message, ttk, Button, Canvas, W, LEFT, CENTER, PhotoImage, SUNKEN, RAISED, Scrollbar, RIGHT
from tkinter.filedialog import askopenfilename
from colorsys import rgb_to_hsv


"""
TODO:
Add image scrollbar.
Rewrite comments and README


"""

class GUI:
	"""
	A class to represent the gui for this program.
	"""
	def __init__(self):
		# There may be other compatible types I am not aware of
		self.image_types = ['png', 'jpg', 'gif', 'jpeg']

		# Create window
		self.window = Tk()
		self.window.title("Image Saturation Reader")

		# Set default variables
		self.current_image_name = "None Selected"
		self.current_image = None
		self.current_mode = 'area'
		self.corners = []
		self.sight_lines = []

		# Find screen height
		width = self.window.winfo_screenwidth()
		height = self.window.winfo_screenheight()
		self.width = width - (width // 2)
		self.height = height - (height // 2)

		# Populate window
		self._generate_window()

		# Bind events
		self.canvas.bind('<Motion>', self.motion)
		self.canvas.bind('<Leave>', self.leave)
		self.canvas.bind('<Button-1>', self.click)
		#self.canvas.config(yscrollcommand=self.y_bar.set)
		#self.canvas.config(xscrollcommand=self.x_bar.set)

		# Final stylizations
		self.area_mode_button.config(relief=SUNKEN)

	def _generate_window(self):
		"""
		Generate the components inside the window.
		"""
		# Left-side information panel
		info_panel = ttk.Frame(self.window)

		# Create components inside left panel
		choose_image = Button(info_panel, text='Choose Image', command=self.choose_image)
		image_label = Message(info_panel, text='Image:', width=40)
		self.image_name = Message(info_panel, text=self.current_image_name, width=100)
		self.image_width = Message(info_panel, text='W: ', width=50)
		self.image_height = Message(info_panel, text='H: ', width=50)
		self.separator = Message(info_panel, text='=======', width=75)
		self.x = Message(info_panel, text='x: ', width=40)
		self.y = Message(info_panel, text='y: ', width=40)
		self.r = Message(info_panel, text='r: ', width=40)
		self.g = Message(info_panel, text='g: ', width=40)
		self.b = Message(info_panel, text='b: ', width=40)
		self.num_pixels = Message(info_panel, text='# Pixels: ', width = 50)
		self.hue = Message(info_panel, text='Hue: ', width=75)
		self.saturation = Message(info_panel, text='Saturation: ', width=75)
		self.value = Message(info_panel, text='Value: ', width=75)
		self.pixel_mode_button = Button(info_panel, text='Pixel Mode', command=self.pixel_mode)
		self.area_mode_button = Button(info_panel, text='Area Mode', command=self.area_mode)

		# Place the components inside left panel
		choose_image.grid(padx=5, pady=5, sticky="N")
		image_label.grid(sticky=W)
		self.image_name.grid(sticky=W)
		self.image_width.grid(sticky=W)
		self.image_height.grid(sticky=W)
		self.separator.grid()
		self.x.grid(sticky=W)
		self.y.grid(sticky=W)
		self.r.grid(sticky=W)
		self.g.grid(sticky=W)
		self.b.grid(sticky=W)
		self.num_pixels.grid(sticky=W)
		self.hue.grid(sticky=W)
		self.saturation.grid(sticky=W)
		self.value.grid(sticky=W)
		self.area_mode_button.grid()
		self.pixel_mode_button.grid()

		# Create right panel components
		self.canvas = Canvas(self.window, width=self.width, height=self.height, bg='lightblue')
		self.x_bar = Scrollbar(self.canvas, orient="horizontal", command=self.canvas.xview)
		print()
		self.y_bar = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
		
		# Place components in right panel
		#self.x_bar.grid(row=1, column=0, sticky="ew")
		#self.y_bar.grid(row=0, column=1, sticky="ns")
		#self.x_bar.rowconfigure(1, weight=1)
		#self.y_bar.columnconfigure(1, weight=1)

		# Add two sides to final window
		info_panel.grid(column=1, row=1)
		self.canvas.grid(column=2, row=1)

		# Final Configurations
		# self.canvas.config(scrollregion=[0, 0, self.width, self.height])
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def choose_image(self):
		self.current_image_name = askopenfilename()
		if self.current_image_name.split('.')[-1] in self.image_types:
			self.image_name.configure(text=self.current_image_name.split('/')[-1])
			self.open_image()
			self.clear_drawing_data()

	def open_image(self):
		self.current_image = Image.open(self.current_image_name)
		current_image_tk = ImageTk.PhotoImage(self.current_image)
		width = current_image_tk.width()
		height = current_image_tk.height()
		self.image_width.config(text='W: ' + str(width))
		self.image_height.config(text='H: ' + str(height))
		self.canvas.config(width=width - 4, height=height - 4)
		self.canvas.create_image(round(width / 2), round(height / 2), anchor=CENTER, image=current_image_tk)
		self.canvas.image = current_image_tk

	def click(self, event):
		"""
		Clicking within the canvas.
		"""
		if self.current_image is not None:
			x, y = event.x, event.y
			if self.current_mode == 'area':
				if not self.corners:
					self.corners.append(self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='white'))
				elif len(self.corners) == 1:
					self.corners.append(self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='white'))
					x1, y1, *_ = self.canvas.coords(self.corners[0])
					x2, y2, *_ = self.canvas.coords(self.corners[1])
					self.get_pixel_data(x1, y1, x2, y2)
				else:
					self.clear_drawing_data()
					self.corners.append(self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='white'))
			elif self.current_mode == 'pixel':
				self.get_pixel_data(x, y, x, y)

	def get_pixel_data(self, x1, y1, x2, y2):
		x1 = round(x1)
		y1 = round(y1)
		x2 = round(x2)
		y2 = round(y2)
		if x2 < x1:
			x1, x2 = x2, x1
		if y2 < y1:
			y1, y2 = y2, y1
		total_hue = 0
		total_saturation = 0
		total_value = 0
		total_r = 0
		total_g = 0
		total_b = 0
		c = 0
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				r, g, b, *_ = self.current_image.getpixel((x, y))
				data = rgb_to_hsv(r, g, b)
				total_hue += data[0]
				total_saturation += data[1]
				total_value += data[2]
				total_r += r
				total_g += g
				total_b += b
				c += 1
		avg_hue = round((total_hue / c), 2)
		avg_saturation = round((total_saturation / c) * 100, 2)
		avg_value = round((total_value / c), 2)
		avg_r = round((total_r / c), 2)
		avg_g = round((total_g / c), 2)
		avg_b = round((total_b / c), 2)
		self.write_pixel_data(avg_hue, avg_saturation, avg_value, avg_r, avg_g, avg_b, c)

	def write_pixel_data(self, hue, sat, val, r, g, b, c):
		self.num_pixels.configure(text='# Pixels: ' + str(c))
		self.hue.configure(text='Hue: ' + str(hue))
		self.saturation.configure(text='Saturation: ' + str(sat) + '%')
		self.value.configure(text='Value: ' + str(val))
		self.r.configure(text='r: ' + str(r))
		self.g.configure(text='g: ' + str(g))
		self.b.configure(text='b: ' + str(b))

	def leave(self, event):
		self.x.configure(text='x: ')
		self.y.configure(text='y: ')

	def motion(self, event):
		if self.current_image is not None:
			x, y = event.x + 1, event.y + 1
			self.x.configure(text='x: ' + str(x))
			self.y.configure(text='y: ' + str(y))
			if len(self.corners) == 1:
				self.draw_sight_lines(x, y)
	
	def draw_sight_lines(self, x, y):
		for line in self.sight_lines:
				self.canvas.delete(line)
		lx, ly, *_ = self.canvas.coords(self.corners[0])
		lx += 2
		ly += 2
		self.sight_lines.append(self.canvas.create_line(lx, ly, x, ly, dash=(3, 3)))
		self.sight_lines.append(self.canvas.create_line(lx, ly, lx, y, dash=(3, 3)))
		self.sight_lines.append(self.canvas.create_line(x, ly, x, y, dash=(3, 3)))
		self.sight_lines.append(self.canvas.create_line(lx, y, x, y, dash=(3, 3)))

	def pixel_mode(self):
		self.clear_drawing_data()
		self.pixel_mode_button.config(relief=SUNKEN)
		self.area_mode_button.config(relief=RAISED)
		self.current_mode = 'pixel'
	
	def area_mode(self):
		self.clear_drawing_data()
		self.area_mode_button.config(relief=SUNKEN)
		self.pixel_mode_button.config(relief=RAISED)
		self.current_mode = 'area'

	def clear_drawing_data(self):
		self.clear_drawings()
		self.corners = []
		self.sight_lines = []

	def clear_drawings(self):
		for line in self.sight_lines:
			self.canvas.delete(line)
		for dot in self.corners:
			self.canvas.delete(dot)


if __name__ == '__main__':
	ui = GUI()
	ui.window.mainloop()