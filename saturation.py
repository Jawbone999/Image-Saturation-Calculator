"""
Pixels are defined with 0, 0 being the top left pixel.
"""

from PIL import Image, ImageColor
from colorsys import rgb_to_hsv
import os

samplesPath = os.getcwd() + '/samples/'

images = {}

for filename in os.listdir(samplesPath):
	images[filename] = Image.open(samplesPath + filename)

for filename, img in images.items():
	img = img.convert('RGB')
	print('=' * 30 + ' ' + filename.upper() + ' ' + '=' * 30)
	print('Please define the rectangle of pixels to evaluate for ' + filename)
	x1, y1 = [int(v) for v in input('Enter the x y position of the top left pixel: ').strip().split()]
	x2, y2 = [int(v) for v in input('Enter the x y position of the bottom right pixel: ').strip().split()]
	
	assert(x1 <= x2 and y1 <= y2)
	totalSaturation = 0
	c = 0
	for y in range(y1, y2 + 1):
		for x in range(x1, x2 + 1):
			r, g, b = img.getpixel((x, y))
			totalSaturation += rgb_to_hsv(r, g, b)[1]
			c += 1
	avg = round((totalSaturation / c) * 100, 2)
	print('Average Saturation for ' + str(c) + ' pixel(s): ' + str(avg) + '%\n\n')
	

	
