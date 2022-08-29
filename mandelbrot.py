import random
import numpy as np
from PIL import Image

OUT_DIR = 'images/'
nr_iterations = 1000000
HEIGHT, WIDTH = 400, 400
COLOR = (0,0,0) # black

mandelbrot = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
mandelbrot[:, :, :] = (255, 255, 255)
max_val = 2.0
minimum = -max_val - max_val * 1j
maximum = max_val + max_val * 1j
real_range = maximum.real - minimum.real
imag_range = maximum.imag - minimum.imag

def random_complex_nr(minimum, maximum):
    x = random.uniform(minimum.real, maximum.real)
    y = random.uniform(minimum.imag, maximum.imag)

    c = x + y * 1j
    return c

def real_to_row(real, real_range = real_range, height = HEIGHT, minimum = minimum, maximum = maximum):
    return int((real - minimum.real) * (height / real_range))

def imag_to_col(imag, imag_range = imag_range, width = WIDTH, minimum = minimum, maximum = maximum):
    return int((imag - minimum.imag) * (WIDTH / imag_range))

for i in range(nr_iterations):
    c = random_complex_nr(minimum, maximum)
    z = 0

    iterator = 0

    while iterator < 50 and abs(z) < max_val:
        z = z * z + c
        iterator += 1
    
    if abs(z) < max_val:
        row = real_to_row(real = c.real)
        col = imag_to_col(imag = c.imag)
        mandelbrot[row,col,:] = COLOR

Image.fromarray(mandelbrot).save(OUT_DIR + 'mandelbrot.jpg')

