import random
import numpy as np
import cv2

HEIGHT, WIDTH = 500, 500
OUT_DIR = 'images/'

RED_ITERS = 2000
GREEN_ITERS = 200
BLUE_ITERS = 20

nr_samples = 4000000
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
    for i in range(nr_samples):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        c = x + y * 1j

        points = generate_points(c, nr_iterations)
        
        for point in points:
            if point.real < maximum.real and point.real > minimum.real and point.imag < maximum.imag and point.imag > minimum.imag:
                row = real_to_row(point.real, minimum = minimum, maximum = maximum, height = height, real_range = real_range)
                col = imag_to_col(point.imag, minimum = minimum, maximum = maximum, width = width, imag_range = imag_range) 

                buddhabrot[row,col,colors[color]] += 1
    
if __name__ == "__main__":
    buddhabrot = np.zeros((HEIGHT, WIDTH, 3), dtype = np.uint8)

    color_image(nr_samples, RED_ITERS, maximum, minimum, HEIGHT, WIDTH, real_range, 'red')
    color_image(nr_samples, GREEN_ITERS, maximum, minimum, HEIGHT, WIDTH, real_range, 'green')
    color_image(nr_samples, BLUE_ITERS, maximum, minimum, HEIGHT, WIDTH, real_range, 'blue')

    print("got here")
    cv2.imwrite(OUT_DIR + 'buddhabrot.jpg', buddhabrot)  