import random

import cv2
import numpy as np
from skimage.draw import line_aa, disk

from gen_tools.color import *
from gen_tools.gen_random import gen_background_white_color, gen_black_color

KIND_TEXT = 'text'

def draw_disks(img, num_lines):
    rows, cols = img.shape[0], img.shape[1]
    radius = np.clip(random.gauss(1, 2), 1, 4)
    for i in range(num_lines):
        rr, cc = disk(
            (random.randint(5, rows-5),
            random.randint(10, cols-10)),
            radius
            )
        img[rr, cc] = random.randint(0, 150)

    return img


def draw_lines(img, num_lines):
    rows, cols = img.shape[0], img.shape[1]

    for i in range(num_lines):
        rr, cc, val = line_aa(
            random.randint(5, rows-5),
            random.randint(10, cols-10), 
            random.randint(5, rows-5), 
            random.randint(10, cols-10)
            )
        img[rr, cc, :] = val[:, np.newaxis]
    return img


def get_color_line(invert):
    """
    Color line for table line.
    need fix
    :return:
    """
    if invert:
        if random.random() < 0.5:
            color = gen_background_white_color(KIND_TEXT, lower_v=240)
        else:
            color = gen_background_white_color(KIND_TEXT, lower_v=180)
    else:
        color = gen_black_color(
            threshold_color=70, threshold_color2=150, threshold2=0.5)
    return color


def draw_one_line(img, top_left, top_right, bottom_right, bottom_left, invert, location=None):
    '''

    :param img:
    :param top_left:
    :param top_right:
    :param bottom_left:
    :param bottom_right:
    :param location:
    :return:
    '''

    color_line_ = get_color_line(invert=invert)
    if location is None:
        tmp_random = random.random()
        if tmp_random <= 0.25:
            location = 'top'
        elif tmp_random <= 0.5:
            location = 'right'
        elif tmp_random <= 0.75:
            location = 'left'
        else:
            location = 'bottom'

    if location == 'top':
        cv2.line(img, top_left, top_right, color_line_,
                 thickness=random.randint(1, 3))
    elif location == 'right':
        cv2.line(img, top_right, bottom_right, color_line_,
                 thickness=random.randint(1, 3))
    elif location == 'left':
        cv2.line(img, top_left, bottom_left, color_line_,
                 thickness=random.randint(1, 3))
    else:  # bottom
        cv2.line(img, bottom_left, bottom_right,
                 color_line_, thickness=random.randint(1, 3))


def draw_two_line(img, top_left, top_right, bottom_right, bottom_left, invert=False):
    '''
    Draw 2 lines
    :param img:
    :param top_left: top_left
    :param top_right: top_right
    :param bottom_left: bottom_left
    :param bottom_right: bottom_right
    :param x_offset:
    :param y_offset:
    :param new_w:
    :param new_h:
    :param text_width:
    :param text_height:
    :return:
    '''
    tmp_random = random.random()
    if tmp_random < 1 / 6:  # top, right
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='top', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='right', invert=invert)
    elif tmp_random < 2 / 6:  # // (top bottom)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='top', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='bottom', invert=invert)
    elif tmp_random < 3 / 6:  # top left
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='top', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='left', invert=invert)
    elif tmp_random < 4 / 6:  # bottom, left
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='bottom', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='left', invert=invert)
    elif tmp_random < 5 / 6:  # // (left, right)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='left', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='right', invert=invert)
    else:  # bottom, right
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='bottom', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='right', invert=invert)


def draw_third_line(img, top_left, top_right, bottom_right, bottom_left, invert=False):
    '''

    :param img:
    :param top_left:
    :param top_right:
    :param bottom_left:
    :param bottom_right:
    :param x_offset:
    :param y_offset:
    :param new_w:
    :param new_h:
    :param text_width:
    :param text_height:
    :return:
    '''

    tmp_random = random.random()

    if tmp_random <= 0.25:  # top, right, botom (left)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='top', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='right', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='bottom', invert=invert)
    elif tmp_random <= 0.5:  # bottom, left, right (top)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='right', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='bottom', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='left', invert=invert)
    elif tmp_random <= 0.75:  # top, left, bottom (right)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='top', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='left', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='bottom', invert=invert)
    else:  # top, right, left (bottom)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='top', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='right', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='left', invert=invert)


def draw_four_line(img, top_left, top_right, bottom_right, bottom_left, invert=False):
    '''

    :param img:
    :param top_left:
    :param top_right:
    :param bottom_left:
    :param bottom_right:
    :param x_offset:
    :param y_offset:
    :param new_w:
    :param new_h:
    :param text_width:
    :param text_height:
    :return:
    '''
    if random.random() < 0.5:
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='top', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='right', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='left', invert=invert)
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, location='bottom', invert=invert)
    else:
        cv2.rectangle(img, top_left, bottom_right, get_color_line(
            invert=invert), thickness=random.randint(2, 3))


def draw_table(img, x_offset, y_offset, text_width, text_height, img_w, img_h, invert=False):
    top_left = (x_left, y_top) = (random.randint(
        0, int(x_offset/2)), random.randint(0, int(y_offset/2)))
    top_right = (x_right, y_top) = (random.randint(
        img_w - int(x_offset/2), img_w), y_top)
    bottom_right = (x_right, y_bottom) = (
        x_right, random.randint(img_h - int(y_offset/2), img_h))
    bottom_left = (x_left, y_bottom)
    tmp_random = random.random()
    if tmp_random <= 0.0:
        pass
    elif tmp_random <= 0.3:
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, invert=invert)
    elif tmp_random <= 0.5:
        draw_two_line(img, top_left, top_right, bottom_right,
                      bottom_left, invert=invert)
    elif tmp_random <= 0.8:
        draw_third_line(img, top_left, top_right, bottom_right,
                        bottom_left, invert=invert)
    else:
        draw_four_line(img, top_left, top_right, bottom_right,
                       bottom_left, invert=invert)
