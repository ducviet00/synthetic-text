import imgaug.augmenters as iaa
import os
import string
import traceback
from gen_tools.draw import draw_noise_for_crnn, draw_shadow_full, noise_blur
from scipy import ndimage
from fontTools.ttLib import TTFont

from gen_tools.gen_random import random_size_char, generate_box_char_v2, gen_background_white_color, gen_black_color
from gen_tools.color import *
import glob
from tqdm import tqdm, trange
import numpy as np
import random
import cv2
import colorsys
from PIL import Image, ImageFilter, ImageStat, ImageEnhance
from PIL import ImageDraw
from PIL import ImageFont
from keras.preprocessing import image
import re
import config
import signal


KIND_TEXT = 'text'

global patterns
patterns = None

def read_map_dict():
    with open(config.MAP_DICT_PATH, encoding='utf-8') as fi:
        map_dict = json.load(fi)

    return map_dict


def random_size_char_crnn(x=20, y=65):
    """
    Gen randomly fontsize and box_size and ratio of these.
    :param x:
    :param y:
    :return:
    """
    fontsize = int(random.randint(x, y) * 0.8)
    # ratio = random.uniform(1.0, 1.08)
    if random.random() < 0.4:
        ratio = 1.0
    else:
        ratio = random.uniform(1.0, 1.08)
    box_size = int(fontsize * ratio)
    return fontsize, box_size


def augment_jpeg(img):
    # jpeg_degree = random.choice(range(101))
    jpeg_degree = 45
    # print ("Jpeg augmenting", jpeg_degree)
    jpeg_augment = iaa.JpegCompression(jpeg_degree)
    img = jpeg_augment.augment_image(img)

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


def random_padding_v2(len_text, max_len):
    padd_bottom = random.randint(0, 5)
    padd_top = random.randint(0, 3)
    # padd_bottom = 4
    padd_x = max_len - len_text

    tmp_random = random.random()

    if tmp_random < 0.15:
        padd_x += 1

    elif padd_x > 0 and tmp_random < 0.3:
        padd_x -= 1

    padd_right = random.randint(0, padd_x)
    padd_left = padd_x - padd_right

    return padd_top, padd_bottom, padd_right, padd_left


def get_shadow_color(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
    s = random.uniform(30, 50)
    v = random.uniform(30, 50)
    r, g, b = colorsys.hsv_to_rgb(h/360., s/100., v/100.)
    return [int(r*255), int(g*255), int(b*255)]


def draw_text_v3(img, text, xy, font_size, font, chars_color, background=False, direction=None, shadow=False, texture=False):
    # print(text, font_path)
    if random.random() < config.CUT_TEXT_NOISE_RATIO:
        img = gen_noise_cut_text(img)
    else:
        img = Image.fromarray(img)

    fill = rgb2hex(*chars_color)
    mask = Image.new("RGBA", img.size, 0)
    if texture and background:
        draw = ImageDraw.Draw(mask)
    else:
        draw = ImageDraw.Draw(img)
    img_w, img_h = img.size
    width_text, height_text = font.getsize(text)
    (text_x_offset, text_y_offset) = font.getoffset(text)

    if shadow and background and random.random() < config.SHADOW_RATIO:
        shadow_color = get_shadow_color(*chars_color)
        hex_shadow = rgb2hex(*shadow_color)
        xi = random.choice([-1, 0, 1])
        yi = random.choice([-1, 0, 1])
        for i in range(1, width_text//25):
            draw.text((-text_x_offset + xy[0] + i*xi, -text_y_offset + xy[1] +
                       i*yi), text, font=font, fill=hex_shadow, direction=direction)

    draw.text((-text_x_offset + xy[0], -text_y_offset + xy[1]),
              text, font=font, fill=fill, direction=direction)
    if texture and background:
        mask = gen_pattern(mask)
        img.paste(mask, (0,0), mask)
    tmp2 = random.random()
    if tmp2 <= config.BLUR_CHAR_RATIO:
        w_text, h_text = font.getsize(text)
        t = random.randint(2, 5)

        while len(text) > 15 and t != 0:
            x_blur = int(random.uniform(xy[0], xy[0] + w_text * 9 / 10))
            y_blur = int(random.uniform(0, img_h / 4))
            a = int(w_text / len(text))
            x2_blur = x_blur + a if a + x_blur < img_w else img_w
            y2_blur = int(random.uniform(img_h / 2, img_h))
            if x_blur > x2_blur:
                t = x_blur
                x_blur = x2_blur
                x2_blur = t
            croped = img.crop((x_blur, y_blur, x2_blur, y2_blur))
            if background:
                rate_blur = [1, 2]
            else:
                rate_blur = [1, 2, 3]
            blurred_image = croped.filter(
                ImageFilter.GaussianBlur(radius=random.choice(rate_blur)))
            img.paste(blurred_image, (x_blur, y_blur, x2_blur, y2_blur))
            t -= 1
        return np.array(img)
    return np.array(img)


def get_color_line(invert):
    """
    Color line for table line.
    :return:
    """
    if invert:
        if random.random() < 0.6:
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
    if tmp_random <= 0.7:
        pass
    elif tmp_random <= 0.8:
        draw_one_line(img, top_left, top_right, bottom_right,
                      bottom_left, invert=invert)
    elif tmp_random <= 0.9:
        draw_two_line(img, top_left, top_right, bottom_right,
                      bottom_left, invert=invert)
    elif tmp_random <= 0.95:
        draw_third_line(img, top_left, top_right, bottom_right,
                        bottom_left, invert=invert)
    else:
        draw_four_line(img, top_left, top_right, bottom_right,
                       bottom_left, invert=invert)


def get_img(dir):
    global patterns
    patterns = glob.glob('{}/*'.format(dir))
    # max_h_pattern = max([pattern.size[0] for pattern in patterns])
    # max_w_pattern = max([pattern.size[1] for pattern in patterns])
    return patterns

def gen_background(img):

    backgrounds = get_img('background')
    bg_dir = random.choice(backgrounds)
    bg = Image.open(bg_dir)
    size = max(img.size[0], img.size[1])*2
    bg.thumbnail((size, size), Image.ANTIALIAS)
    xstart = random.randrange(0, bg.size[0]-img.size[0])
    ystart = random.randrange(0, bg.size[1]-img.size[1])
    # random crop
    bg = bg.crop((xstart, ystart, xstart+img.size[0], ystart+img.size[1]))

    return bg

def gen_pattern(img):
    patterns_dir = get_img('pattern')
    dir = random.choice(patterns_dir)
    pattern = Image.open(dir).convert('RGBA')
    for x in range(0, img.size[0], pattern.size[0]):
        for y in range(0, img.size[1], pattern.size[1]):
            img.paste(pattern, (x,y), pattern)
    return img

def get_color(invert):
    if not invert:
        if random.random() < 0.6:
            back_ground_color = gen_background_white_color(
                KIND_TEXT, lower_v=240)
        else:
            back_ground_color = gen_background_white_color(
                KIND_TEXT, lower_v=180)
        character_color = gen_black_color(
            threshold_color=70, threshold_color2=150, threshold=0.7)

    else:
        if random.random() < 0.6:
            character_color = gen_background_white_color(
                KIND_TEXT, lower_v=240)
        else:
            character_color = gen_background_white_color(
                KIND_TEXT, lower_v=180)

        back_ground_color = gen_black_color(
            threshold_color=70, threshold_color2=150, threshold2=0.5)

    return character_color, back_ground_color


def invert_bg(img):
    if isinstance(img, Image.Image):
        h, s, v = img.convert('HSV').split()
        h = (np.mean(h) + 180 + random.uniform(-5, 5)) % 360
        s = random.randrange(90, 100)
        v = (100 - np.mean(v) - random.uniform(-5, 5)) % 100

        rgb = [int(i*255) for i in colorsys.hsv_to_rgb(h/360., s/100., v/100.)]
        
        return rgb
    else:
        return False


def paint_txt_v51(sentence, max_len, font_path, w=None, h=None, rotate=False, invert=False, table=False,
                  height_variant=True, augment=True, texture=False,
                  generating_test=False, shadow=False):
    """
    Sinh chu bt.
    1 px = 0.75 point; 1 point = 1.333333 px
    :param table:
    :param invert:
    :param rotate:
    :param Text sentence:
    :param max_len:
    :param utils.font_util.ListFonts list_fonts:
    :param w:
    :param h:
    :return:
    """
    if not generating_test:
        assert len(sentence) <= max_len, sentence

    character_color, back_ground_color = get_color(invert)

    BLACK = 150
    is_black = False
    bg_color = [255, 255, 255]
    bg = False

    if sentence != '' and sentence != ['']:
        random_font_size = random.random()
        if random_font_size < 0.85:
            font_size = random.randint(30, 40)
        elif random_font_size < 0.95:
            font_size = random.randint(40, 56)
        else:
            font_size = random.randint(56, 64)

        font = ImageFont.truetype(font_path, font_size)

        text_width, text_height = font.getsize("".join(sentence))
        (text_x_offset, text_y_offset) = font.getoffset("".join(sentence))
        y_offset = random.randint(1, 6)
        x_offset = random.randint(1, 6)
        y_padding = random.randint(1, 6)
        x_padding = random.randint(1, 6)
        text_height = text_height - text_y_offset
        text_width = text_width - text_x_offset
        img_h = text_height + y_offset + y_padding
        img_w = text_width + x_offset + x_padding
        if text_height < 20:
            return None
        img = np.ones([img_h, img_w, 3], dtype=np.uint8)
        tm_rnd = random.random()
        bg_color = max(back_ground_color)
        background_img = None

        if random.random() < config.BOLD_BG_RATIO:
            img = Image.fromarray(img)
            img = gen_background(img)
            character_color_temp = invert_bg(img)
            if texture and random.choice([0,1]):
                # add texture into background or text
                img = gen_pattern(img)
                texture = False
            bg = True
            if character_color_temp is not None:
                character_color = character_color_temp
            img = np.asarray(img)
            background_img = img
        elif bg_color > BLACK or (bg_color <= BLACK and tm_rnd < 0.7):
            img[:, :] = back_ground_color
            background_img = img
        else:
            img = gen_bg_black(img_w, img_h, bg_color)
            is_black = True
            background_img = img
        # print(character_color)
        # print("img shape: ",img.shape)
        if table is True:
            draw_table(img, x_offset, y_offset, text_width,
                       text_height, img_w, img_h, invert=invert)

        img = draw_text_v3(img,
                           sentence,
                           (x_offset, y_offset),
                           font_size,
                           font=font,
                           chars_color=character_color,
                           background=bg,
                           shadow=shadow,
                           texture=texture)

        if rotate:
            if random.random() < 0.4:
                img = image.random_rotation(
                    img, 0.5, row_axis=0, col_axis=1, channel_axis=2)
        # print('bacc', background_img.shape)
        # img = make_composite_italic(img, background_img)

    else:
        img_w = random.uniform(h, w)
        img = np.ones([h, img_w, 3], dtype=np.uint8)
        img[:, :] = back_ground_color

    if augment and not is_black and not bg:
     
        tmp_random = random.random()
        # img = augment_jpeg(img)
        if tmp_random < 0.2:
            mean = int(np.mean(img))
            if mean <= 127:
                value = max(mean - 10, 0)
            else:
                value = min(mean + 10, 255)
            img = add_salt_pepper_noise(img, value)
        elif tmp_random < 0.4:
            img = noise_blur(img)
        elif tmp_random < 0.6:
            img = noise_blur(img)
            img = speckle(img)
        elif tmp_random < 0.8:
            img = speckle(img)
            img = noise_blur(img)
        else:
            img = speckle(img)
    return img


def augment_img(img):
    tmp_random = random.random()
    if tmp_random < 0.4:
        img = noise_blur(img)
    elif tmp_random < 0.5:
        img = noise_blur(img)
        img = speckle(img)
    elif tmp_random < 0.6:
        img = speckle(img)
        img = noise_blur(img)
    elif tmp_random < 0.8:
        img = speckle(img)
    else:
        img = augment_jpeg(img)

    return img

# ========================================================================


def add_effect(img, back_ground_color):
    """
    Add effect to the image
    """

    img = np.array(img)
    # img = make_composite_italic(img, back_ground_color)
    tmp_random = random.random()
    if tmp_random < 0.2:
        mean = int(np.mean(img))
        if mean <= 127:
            value = max(mean - 20, 0)
        else:
            value = min(mean + 20, 255)
        img = add_salt_pepper_noise(img, value)
    elif tmp_random < 0.4:
        img = noise_blur(img)
    elif tmp_random < 0.5:
        img = noise_blur(img)
        img = speckle(img)
    elif tmp_random < 0.6:
        img = speckle(img)
        img = noise_blur(img)
    elif tmp_random < 0.8:
        img = speckle(img)
    else:
        img = augment_jpeg(img)
    return Image.fromarray(img.astype(np.uint8))


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

def read_file(path):
    with open(path, 'r') as input:
        lines = input.readlines()
    # return lines
    filter_lines = set()
    for line in lines:
        filter_lines.add(line.strip())
    return list(filter_lines)


def font_support_telephone(list_font):
    list_supported_font = []
    # bad_font_list = ['ZinHenaKokuryu', 'ArmedBanana', 'KouzanMouhituFont', 'ZinHenaBokuryu', 'ArmedLemon', 'nagayama_kai08', 'aoyagireisyosimo_ttf_2_01', 'SNsanafon', '851', 'ShigotoMemogaki-Regular-1-01', 'YuzuPenJiN_101', 'mitsu', 'MakibaFont13', 'HuiFont29', 'f_feltpen04', 'dining_m', 'SNsanafonyu', 'erisfont', 'nagurip', 'SistersF', 'HonyaJi-Re', 'mikachan', 'moon', 'crayon_1-1', 'SNsanafonmaru', 'c_jyunjun', 'ElmerFont']
    for font_path in list_font:
        # for bad_font in bad_font_list:
        #     if bad_font in font_path:
        #         break
        # else:
        #     list_supported_font.append(font_path)
        list_supported_font.append(font_path)
    return list_supported_font


def weave(list1, list2):
    lijst = []
    i = 0
    while i < len(list1):
        lijst.append(list1[i])
        if i < len(list2):
            lijst.append(list2[i])
        i += 1
    return lijst


def get_min_required_char_index(sentence, required_chars):
    if len(sentence) < 2:
        return len(sentence)
    min_index = 256
    for char in required_chars:
        if char in sentence:
            new_index = sentence.find(char)
            if new_index == 0:
                return 0
            elif new_index < min_index and new_index > 0:
                min_index = new_index
    if min_index == 256:
        return None
    return min_index

def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")

def load_all_fonts(font_paths):
    dict_unicode = {}
    for path in font_paths:
        files = glob.glob(os.path.join(path, "*"))
        for file in files:
            fn_lower = file.lower()
            if fn_lower.endswith((".ttc", ".otf", ".ttf")):
                try:
                    if "ttc" in fn_lower:
                        ttf = TTFont(file, 0, allowVID=0,
                                    ignoreDecompileErrors=False, fontNumber=0)
                    else:
                        ttf = TTFont(file, 0, allowVID=0,
                                    ignoreDecompileErrors=False, fontNumber=-1)
                    font = ImageFont.truetype(file, 10)
                    list_uchar = []
                    for x in ttf["cmap"].tables:
                        for y in x.cmap.items():
                            list_uchar.append(y[0])
                    ttf.close()
                    dict_unicode[file] = list_uchar
                except:
                    print("ERROR font:", file)
                    os.remove(file)
                    continue
    return dict_unicode


def check_support(list_uchar, text):
    for char in text:
        for char_extra in char:
            u_char = ord(char_extra)
            if u_char not in list_uchar:
                return False
    return True


def get_supported_fonts(text, font_dict):
    list_supported_font = []
    for font in font_dict:
        if check_support(font_dict[font], text):
            list_supported_font.append(font)
    return list_supported_font


if __name__ == "__main__":
    # signal.signal(signal.SIGALRM, handler)
    # signal.alarm(10)
    list_font_path = glob.glob(r'fonts/*')
    list_font_path += ["fonts"]
    font_dict = load_all_fonts(list_font_path)
    # sentence_path = "train_japanese_sentences.txt"
    word_path = "vnmesevocab.txt"

    dict_gen = {}
    repeat_num = 10000
    using_random_font = True
    using_random_sentence = False

    dict_gen['vnwords'] = read_file(word_path)  
    # dict_gen['sentence'] = read_file(sentence_path) #4518*35
    # out_path = "./testscencetext"
    out_path = "/mnt/disk4/viethd/1.25B-SCANNED-UNIWORD"
    list_supported_font = get_supported_fonts('đẳỡựạựỡớờỵý', font_dict)
    # Each key is a separate folder
    for gen in dict_gen.keys():
        save_path = out_path
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        out_images_save = os.path.join(save_path, "imgs")
        if not os.path.isdir(out_images_save):
            os.makedirs(out_images_save)
        else:
            print('\n\n Careful: Save folder already exist!!')
            exit()
        count = 0
        # Endof Each key is a separate folder
        number_sens = len(dict_gen[gen])
        print(
            "\n***\n{} have: {} sentence".format(gen, number_sens))

        # Uncomment to limit the number of words to gen
        # number_sens = 20
        print('Supported font: ', len(list_supported_font))
        for i in range(number_sens):
            ann = open(os.path.join(save_path, f"annotates_{i}.txt"), "w")
            # sentence = random.choice(dict_gen[gen])
            print(f"DONE: {i}/{number_sens} GENERATED: {count} imgs")
            sentence = dict_gen[gen][i]
            for repeat_time in trange(repeat_num):
                sentence = dict_gen[gen][i]
            
                if not sentence:
                    continue  
                lower_upper = random.random()
                if lower_upper < 0.50:
                    sentence = sentence.lower()
                elif lower_upper < 0.85:
                        sentence = sentence.capitalize() 
                elif lower_upper < 0.95:
                    sentence = sentence.upper()

                if random.random() < 0.4:
                    space = random.choice([' ', ''])
                    if random.random() < 0.2:
                        sentence += space + random.choice(string.punctuation)
                    elif random.random() < 0.2:
                        sentence = random.choice(string.punctuation) + space + sentence
                    elif random.random() < 0.2:
                        sentence = '\"' + sentence + '\"'
                    space = random.choice([' ', ''])
                    if random.random() < 0.2:
                        sentence = sentence + space + str(int(random.gauss(5., 5.)))
                    if random.random() < 0.2:
                        sentence = str(int(random.gauss(5., 5.))) + space + sentence
                    
                if len(sentence) >= 20:
                    sentence = dict_gen[gen][i]
                # while True:
                img = None
                while img is None:
                    font_path = random.choice(list_supported_font)
                    img = paint_txt_v51(sentence,
                                        max_len=20,
                                        font_path=font_path,
                                        w=1920,
                                        h=32,
                                        rotate=True,
                                        invert=False,
                                        table=True,
                                        height_variant=False,
                                        augment=True,
                                        generating_test=False,
                                        shadow=True,
                                        texture=True
                                        )
                if img is None:
                    continue
                img = img[...,::-1]
                img = img.astype(np.uint8)
                name_img = '{}_{}.png'.format(count, gen)
                # if img.save(os.path.join(out_images_save, name_img)):
                if cv2.imwrite(os.path.join(out_images_save, name_img), img):
                    ann.write(name_img + "\t" + sentence + "\n")
                    count += 1
                    # break
                # else:
                #     print("Save IMG failed")
                #     print("FONT:", font_path)
                #     print("SENCTENCE:", sentence)

            
                    
                # if not count % 10000:
                #     print(count, end='\n', flush=True)
            ann.close()
        print('\n===\nGenerated:', count)

        print("\n***\nout_images_save\n", save_path)

