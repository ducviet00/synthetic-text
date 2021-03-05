import colorsys
import random

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

from gen_tools.noise import noisy_dotted_line, noisy_inversion_models


def gen_noise_cut_text(img):
    # if random.random() < ratio:
    img = Image.fromarray(img).convert('RGBA')

    w_img, h_img = img.size
    pattern = Image.open('noise.jpg', 'r').convert('RGBA')
    w, h = pattern.size
    size = w / 3, h / 3
    pattern.thumbnail(size, Image.ANTIALIAS)
    num_noise = random.randint(1, 4)
    for i in range(num_noise):
        angle = random.randint(0, 90)
        rotated = pattern.rotate(angle)
        fff = Image.new('RGBA', rotated.size, (255,) * 4)
        # create a composite image using the alpha layer of rot as a mask
        out = Image.composite(rotated, fff, rotated)
        # r_w,r_h= pattern.size
        r_w, r_h = rotated.size
        pos = (random.randint(0, w_img - r_w), random.randint(0, h_img - r_h))
        # img.paste(pattern,pos)
        img.paste(out, pos)
    img = img.convert('RGB')
    # else:
    #     img = Image.fromarray(img)
    return img

def noise_blur(img):
    filter_size = random.choice([3, 5])

    img = cv2.GaussianBlur(img, (filter_size, filter_size), 0)

    return img


def speckle(img):
    severity = np.random.uniform(0, 0.2 * 255)
    blur = ndimage.gaussian_filter(np.random.randn(*img.shape) * severity, 1)
    img_speck = (img + blur)
    img_speck[img_speck > 255] = 255
    img_speck[img_speck <= 0] = 0
    return img_speck


def add_salt_pepper_noise(img, value=255):
    img_copy = img.copy()
    ratio = random.uniform(0.05, 0.1)
    row, col, _ = img_copy.shape
    num_salt = np.ceil(img_copy.size * ratio)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img.shape]
    img[coords[0], coords[1], :] = value
    return img


def gen_bg_black(w, h, color):
    img = np.ones((h, w, 3), np.uint8) * color
    h, w, d = img.shape
    scale = 5
    for w_ in range(w // scale):
        for h_ in range(h):
            img[h_, w_ * scale] = np.random.choice([255, 0], p=[0.4, 0.6])
    for h_ in range(h // scale):
        for w_ in range(w):
            img[h_ * scale, w_] = np.random.choice([255, 0], p=[0.4, 0.6])
    return img


def get_shadow_color(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
    s = random.uniform(30, 50)
    v = random.uniform(30, 50)
    r, g, b = colorsys.hsv_to_rgb(h/360., s/100., v/100.)
    return [int(r*255), int(g*255), int(b*255)]
