import cv2
import numpy as np
import sys
import random

def get_neighbours(blank_image, x, y, vertical_length, horizontal_length):
	neighbours = []

	if x != 0:
		top = blank_image[x-1][y]
		if top != 0:
			neighbours.append(top)
	if y != 0:
		left = blank_image[x][y-1]
		if left != 0:
			neighbours.append(left)
	if x != vertical_length-1:
		bottom = blank_image[x+1][y]
		if bottom != 0:
			neighbours.append(bottom)
	if y != horizontal_length-1:
		right = blank_image[x][y+1]
		if right != 0:
			neighbours.append(right)
	if x != 0 and y != 0:
		top_left = blank_image[x-1][y-1]
		if top_left != 0:
			neighbours.append(top_left)
	if x != 0 and y != horizontal_length-1:
		top_right = blank_image[x-1][y+1]
		if top_right != 0:
			neighbours.append(top_right)
	if x != vertical_length-1 and y != 0:
		bottom_left = blank_image[x+1][y-1]
		if bottom_left != 0:
			neighbours.append(bottom_left)
	if x != vertical_length-1 and y != horizontal_length-1:
		bottom_right = blank_image[x+1][y+1]
		if bottom_right != 0:
			neighbours.append(bottom_right)
	return neighbours

def get_lowest_adjacent(blank_image, x, y, vertical_length, horizontal_length):
	neighbours = get_neighbours(blank_image, x, y, vertical_length, horizontal_length)
	if neighbours:
		return min(neighbours)
	else:
		return None

input_file = sys.argv[2]
min_nodule = int(sys.argv[4])

input_image=cv2.imread(input_file, 0)
input_image[input_image >= 128] = 255
input_image[input_image < 128] = 0

vertical_length = input_image.shape[0]
horizontal_length = input_image.shape[1]
blank_image = np.zeros((vertical_length, horizontal_length))

count = 0
connected_nodules = {}

for x in range(vertical_length):
	for y in range(horizontal_length):
		if input_image[x][y] == 0:
			lowest_adjacent = get_lowest_adjacent(blank_image, x, y, vertical_length, horizontal_length)
			if lowest_adjacent:
				blank_image[x][y] = lowest_adjacent
			else:
				count += 1
				blank_image[x][y] = count
				connected_nodules[count] = set()
				connected_nodules[count].add(count)
			neighbours = get_neighbours(blank_image, x, y, vertical_length, horizontal_length)
			for neighbour in neighbours:
				for number in connected_nodules[neighbour]:
					connected_nodules[blank_image[x][y]] = connected_nodules[blank_image[x][y]].union(connected_nodules[number])
					connected_nodules[number] = connected_nodules[number].union(connected_nodules[blank_image[x][y]])

unique_counter = 0
unique_identifiers = set()
nodule_size = {}

for x in range(vertical_length):
	for y in range(horizontal_length):
		identifier = blank_image[x][y]
		if identifier != 0:
			min_association = min(list(connected_nodules[identifier]))
			blank_image[x][y] = min_association
			if min_association not in nodule_size:
				nodule_size[min_association] = 0
			nodule_size[min_association] += 1
			if min_association not in unique_identifiers:
				unique_counter += 1
				unique_identifiers.add(min_association)

color_image = np.zeros((vertical_length, horizontal_length,3), np.uint8)
color_image[:, :] = (255, 255, 255)

nodule_colour = {}

significant_nodules = 0
for nodule in nodule_size:
	if nodule_size[nodule] >= min_nodule:
		nodule_colour[nodule] = (random.randint(50,200), random.randint(50,200), random.randint(50,200))
		significant_nodules += 1

print(significant_nodules)

if len(sys.argv) == 7 and sys.argv[5] == "--optional_output":
	output_file = sys.argv[6]
	for x in range(vertical_length):
		for y in range(horizontal_length):
			nodule = blank_image[x][y]
			if nodule in nodule_colour:
				color_image[x][y] = nodule_colour[nodule]
	cv2.imwrite(output_file, color_image)