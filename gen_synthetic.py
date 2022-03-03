import glob
import logging
import os
import random
import string

import cv2
import lmdb
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from skimage.transform import PiecewiseAffineTransform, warp
from tqdm import tqdm, trange

import config
from config import *
from gen_tools.color import rgb2hex
from gen_tools.draw_effects import *
from gen_tools.draw_lines import *
from gen_tools.fonts_ultis import get_supported_fonts, load_all_fonts
from gen_tools.gen_random import get_color, invert_bg
from utils import *

KIND_TEXT = 'text'

global patterns
patterns = None


def draw_text(img, text, xy, font_size, font, chars_color, background=False, direction=None, shadow=False, texture=False):
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
    if texture:
        mask = gen_pattern(mask)
        img.paste(mask, (0, 0), mask)
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
    bg.resize((size, size), Image.ANTIALIAS)
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
            img.paste(pattern, (x, y), pattern)
    return img


def gensyn_text(sentence, max_len, font_path, w=None, h=None, rotate=False, invert=False, table=False,
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
        y_offset = random.randint(30, 50) # add more 5*pi for piecewise_affine
        x_offset = random.randint(40, 80)
        y_padding = random.randint(30, 50) # add more 5*pi for piecewise_affine
        x_padding = random.randint(40, 80)
        text_height = text_height - text_y_offset
        text_width = text_width - text_x_offset
        img_h = text_height + y_offset + y_padding
        img_w = text_width + x_offset + x_padding
        if text_height < 20:
            return None
        img = np.ones([img_h, img_w, 3], dtype=np.uint8)
        tm_rnd = random.random()
        bg_color = max(back_ground_color)

        if random.random() < config.BOLD_BG_RATIO:
            img = Image.fromarray(img)
            img = gen_background(img)
            character_color_temp = invert_bg(img)
            if texture and random.choice([0, 1]):
                # add texture into background or text
                img = gen_pattern(img)
                texture = False
            bg = True
            if character_color_temp is not None:
                character_color = character_color_temp
            img = np.asarray(img)
        elif bg_color > BLACK or (bg_color <= BLACK and tm_rnd < 0.7):
            img[:, :] = back_ground_color
        else:
            img = gen_bg_black(img_w, img_h, bg_color)
            is_black = True
        # print(character_color)
        # print("img shape: ",img.shape)
        if table is True:
            draw_table(img, x_offset, y_offset, text_width,
                       text_height, img_w, img_h, invert=invert)
            img = draw_lines(img, num_lines=random.randint(1, 3))
        
        img = draw_disks(img, num_lines=random.randint(8, 20))

        img = draw_text(img,
                        sentence,
                        (x_offset, y_offset),
                        font_size,
                        font=font,
                        chars_color=character_color,
                        background=bg,
                        shadow=shadow,
                        texture=texture)

    else:
        img_w = random.uniform(h, w)
        img = np.ones([h, img_w, 3], dtype=np.uint8)
        img[:, :] = back_ground_color

    if augment and not is_black and not bg:
        img = augment_img(img)

    # if rotate:
    #     if random.random() < 3:
    #         angle = random.randint(5, 30)
    #         img = Image.fromarray(img)
    #         img = img.rotate(angle, expand=True)
    img = img[16:-16, :] # crop padding which was used for piecewise_affine
    return img

def piecewise_affine_transform(img):
    rows, cols = img.shape[0], img.shape[1]

    src_cols = np.linspace(0, cols, random.randint(10, 20))
    src_rows = np.linspace(0, rows, random.randint(10, 20))
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]

    # add sinusoidal oscillation to row coordinates
    dst_rows = src[:, 1] - np.sin(np.linspace(0, random.randint(3, 5) * np.pi, src.shape[0])) * 10
    dst_cols = src[:, 0]

    dst = np.vstack([dst_cols, dst_rows]).T


    tform = PiecewiseAffineTransform()
    tform.estimate(src, dst)

    out_rows = img.shape[0]
    out_cols = cols
    out = warp(img, tform, output_shape=(out_rows, out_cols))
    out *= 255
    out = out.astype(np.uint8)

    return out

def augment_img(img):
    tmp_random = random.random()

    if random.random() < 1:
        mean = int(np.mean(img))
        if mean <= 127:
            value = max(mean - 10, 0)
        else:
            value = min(mean + 10, 255)
        img = add_salt_pepper_noise(img, value)
    if tmp_random < 0.4:
        img = noise_blur(img)
    elif tmp_random < 0.5:
        img = noise_blur(img)
        img = speckle(img)
    elif tmp_random < 0.6:
        img = speckle(img)
        img = noise_blur(img)
    else:
        img = speckle(img)
    img = img.astype(np.uint8)

    if random.random() < 1:
        img = piecewise_affine_transform(img)

    return img


def writeCache(env, cache):
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            txn.put(k.encode(), v)


def add_random_characters(sentence, max_len):
    loup_random = random.random()
    if loup_random < 0.30:
        sentence = sentence.lower()
    elif loup_random < 0.60:
        sentence = sentence.capitalize()
    else:
        sentence = sentence.upper()

    if random.random() < 0.2:
        space = random.choice([' ', ''])
        if random.random() < 0.5:
            sentence += space + \
                random.choice(string.punctuation + string.digits)
        else:
            sentence = random.choice(
                string.punctuation + string.digits) + space + sentence
    if len(sentence) > max_len:
        sentence = sentence[:max_len]
    return sentence


if __name__ == "__main__":
    list_font_path = glob.glob('fonts/*')
    list_font_path += glob.glob('fonts/*/*')
    list_font_path += glob.glob('fonts/*/*/*')
    font_dict = load_all_fonts(list_font_path)
    list_supported_font = get_supported_fonts(config.VOCAB, font_dict)
    using_random_font = True

    env = lmdb.open(OUTPUT_PATH, map_size=2e+12)  # 2 Terabyte
    logging.info(f"START GENERATING SYNTHETIC DATA TO {OUTPUT_PATH}")
    # lmdb cache
    cache = {}
    count = 0
    for gen in dict_gen.keys():
        if SAVE_FILE:
            out_images_save = os.path.join(OUTPUT_PATH, "imgs")
            os.makedirs(out_images_save)
        number_sens = len(dict_gen[gen])
        logging.info("\n***\n{} have: {} sentence".format(gen, number_sens))
        logging.info('Supported font: ', len(list_supported_font))

        # Uncomment to limit the number of words to gen
        # number_sens = 1000
        for i in trange(number_sens):
            # for font_path in tqdm(list_supported_font):
            for repeat_time in range(config.REPEAT_NUM):
                sentence = add_random_characters(
                    dict_gen[gen][i], config.MAX_LEN)
                if not sentence:
                    continue
                img = None
                while img is None:
                    try:
                        font_path = random.choice(list_supported_font)
                        img = gensyn_text(sentence,
                                          max_len=config.MAX_LEN,
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
                                          texture=False
                                          )
                    except:
                        img = None
                        logging.exception("FAILED")
                        break
                if img is None:
                    continue
                img = img[..., ::-1]
                img = img.astype(np.uint8)
                imageFile = '{}_{}.jpg'.format(count, gen)
                imageKey = 'image-%09d' % count
                labelKey = 'label-%09d' % count
                pathKey = 'path-%09d' % count
                dimKey = 'dim-%09d' % count

                imgH, imgW = img.shape[0], img.shape[1]
                cache[imageKey] = cv2.imencode('.jpg', img)[1].tobytes()
                cache[labelKey] = sentence.encode()
                cache[pathKey] = imageFile.encode()
                cache[dimKey] = np.array(
                    [imgH, imgW], dtype=np.int32).tobytes()
                count += 1

                if count % 10000 == 0:
                    writeCache(env, cache)
                    cache = {}

                while not cv2.imwrite(os.path.join(out_images_save, imageFile), img) and SAVE_FILE:
                    print("Try save img, font:", imageFile)

    nSamples = count - 1
    cache['num-samples'] = str(nSamples).encode()
    writeCache(env, cache)
    logging.info('\n===\nGenerated:', count)

    logging.info("\n***\nout_images_save\n", OUTPUT_PATH)
