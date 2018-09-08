import cv2
import numpy as np
import sys

def greyscale_histogram(image):
   histogram = [0]*256
   vertical_length = image.shape[0]
   horizontal_length = image.shape[1]
   for x in range(vertical_length):
      for y in range(horizontal_length):
         pixel_value = image[x][y]
         histogram[pixel_value] += 1
   return histogram

def get_binary_image(input_image):
   max_thresh = 0
   max_interclass_var = 0
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

   vertical_length = input_image.shape[0]
   horizontal_length = input_image.shape[1]
   blank_image = np.zeros((vertical_length, horizontal_length))
   input_image[input_image >= max_thresh] = 255
   input_image[input_image < max_thresh] = 0
   
   return input_image, max_thresh, histogram

def threshold_image(input_image, threshold):
   input_image[input_image >= threshold] = 255
   input_image[input_image < threshold] = 0
   return input_image

def count_peaks(histogram):
   count = 0
   max_pixel = len(histogram)-1
   for pixel_value, pixel_count in enumerate(histogram):
      left_end = max(0,pixel_value-50)
      right_end = min(max_pixel,pixel_value+50)
      if all(pixel_count > side_pixel for side_pixel in histogram[left_end:pixel_value]) and all(pixel_count > side_pixel for side_pixel in histogram[pixel_value+1:right_end]):
         count += 1
   return count

input_file = sys.argv[2]
n = int(sys.argv[3])
output_file = sys.argv[5]
input_image=cv2.imread(input_file, 0)
vertical_length = input_image.shape[0]

slices_threshes = []
histograms = []
peak_count = []

for x in range(n):
   slice_top_index = x * vertical_length / n
   slice_bottom_index = (x + 1) * vertical_length / n
   horizontal_slice = input_image[slice_top_index:slice_bottom_index, :]
   binary_sliced_image, slice_thresh, histogram = get_binary_image(horizontal_slice)
   slices_threshes.append(slice_thresh)
   peak_count.append(count_peaks(histogram))
   input_image[slice_top_index:slice_bottom_index, :] = binary_sliced_image

for x in range(n):
   slice_top_index = x * vertical_length / n
   slice_bottom_index = (x + 1) * vertical_length / n
   horizontal_slice = input_image[slice_top_index:slice_bottom_index, :]
   if peak_count[x] != 2:
      if x > 0 and peak_count[x-1] == 2:
         binary_sliced_image = threshold_image(horizontal_slice, slices_threshes[x-1])
         input_image[slice_top_index:slice_bottom_index, :] = binary_sliced_image
      elif x < n-1 and peak_count[x+1] == 2:
         binary_sliced_image = threshold_image(horizontal_slice, slices_threshes[x+1])
         input_image[slice_top_index:slice_bottom_index, :] = binary_sliced_image

cv2.imwrite(output_file, input_image)