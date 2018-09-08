import cv2
import sys

input_file = sys.argv[2]
output_file = sys.argv[4]

input_image = cv2.imread(input_file, 0)
output_image = cv2.blur(input_image, (5,5))

cv2.imwrite(output_file, output_image)
