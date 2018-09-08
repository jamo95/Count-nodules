import cv2
import numpy as np
import sys

input_file = sys.argv[2]
output_file = sys.argv[4]

def greyscale_histogram(image):
   histogram = [0]*256
   vertical_length = image.shape[0]
   horizontal_length = image.shape[1]
   for x in range(vertical_length):
      for y in range(horizontal_length):
         pixel_value = image[x][y]
         histogram[pixel_value] += 1
   return histogram

max_thresh = 0
max_interclass_var = 0

input_image=cv2.imread(input_file, 0)
histogram_values = list(range(256))
histogram = greyscale_histogram(input_image)

histogram_weights = np.multiply(histogram, histogram_values)
for x in range(0, 256):
   first_cluster_count = sum(histogram[:x+1])
   second_cluster_count = sum(histogram[x+1:])
   if first_cluster_count == 0 or second_cluster_count == 0 :
      continue
   first_mean =  sum(histogram_weights[:x+1]) / float(first_cluster_count)
   second_mean =  sum(histogram_weights[x+1:]) / float(second_cluster_count)
   square_mean_diff = (first_mean - second_mean) ** 2
   interclass_var = first_cluster_count * second_cluster_count * square_mean_diff
   if interclass_var > max_interclass_var:
      max_interclass_var = interclass_var
      max_thresh = x

input_image=cv2.imread(input_file, 0)
vertical_length = input_image.shape[0]
horizontal_length = input_image.shape[1]
blank_image = np.zeros((vertical_length, horizontal_length))
input_image[input_image >= max_thresh] = 255
input_image[input_image < max_thresh] = 0
cv2.imwrite(output_file, input_image)

if len(sys.argv) == 6 and sys.argv[5] == "--threshold":
   print(max_thresh)