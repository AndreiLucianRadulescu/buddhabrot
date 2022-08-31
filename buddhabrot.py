import random
import numpy as np
import cv2
from tqdm import tqdm

HEIGHT, WIDTH = 400, 400
OUT_DIR = 'images/'

global MAX_COLOR
RED_ITERS = 20000
GREEN_ITERS = 200
BLUE_ITERS = 20

nr_samples = 1000000
max_val = 2.0
minimum = -max_val - max_val * 1j
maximum = max_val + max_val * 1j
real_range = maximum.real - minimum.real
imag_range = maximum.imag - minimum.imag

colors = {'blue':0, 'green':1, 'red':2}

def real_to_row(real, real_range = real_range, height = HEIGHT, minimum = minimum, maximum = maximum):
    return int((real - minimum.real) * (height / real_range))

def imag_to_col(imag, imag_range = imag_range, width = WIDTH, minimum = minimum, maximum = maximum):
    return int((imag - minimum.imag) * (WIDTH / imag_range))

def generate_points(c, nr_iterations):
    i = 0
    z = 0 + 0 * 1j
    result = []

    while i < nr_iterations and abs(z) <= max_val:
        z = z * z + c
        i += 1

        result.append(z)
    
    if i == nr_iterations:
        return []
    else:
        return result

def color_image(nr_samples, nr_iterations, maximum, minimum, height, width, real_range, color):
    for i in tqdm(range(nr_samples)):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        c = x + y * 1j

        points = generate_points(c, nr_iterations)
        
        for point in points:
            if point.real < maximum.real and point.real > minimum.real and point.imag < maximum.imag and point.imag > minimum.imag:
                row = real_to_row(point.real, minimum = minimum, maximum = maximum, height = height, real_range = real_range)
                col = imag_to_col(point.imag, minimum = minimum, maximum = maximum, width = width, imag_range = imag_range) 

                buddhabrot[row,col,colors[color]] += 1

buddhabrot = np.zeros((HEIGHT, WIDTH, 3), dtype = np.uint64)

color_image(nr_samples, RED_ITERS, maximum, minimum, HEIGHT, WIDTH, real_range, 'red')
color_image(nr_samples, GREEN_ITERS, maximum, minimum, HEIGHT, WIDTH, real_range, 'green')
color_image(nr_samples, BLUE_ITERS, maximum, minimum, HEIGHT, WIDTH, real_range, 'blue')

max_value = np.max(buddhabrot)

scale = 255 / max_value
for row in range(HEIGHT):
    for col in range(WIDTH):
        buddhabrot[row,col,0] = np.uint8(buddhabrot[row,col,0] * scale)
        buddhabrot[row,col,1] = np.uint8(buddhabrot[row,col,1] * scale)
        buddhabrot[row,col,2] = np.uint8(buddhabrot[row,col,2] * scale)

buddhabrot = buddhabrot.astype(np.uint8)

cv2.imwrite(OUT_DIR + 'buddhabrotMoreRed.jpg', buddhabrot)  