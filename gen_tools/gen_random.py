import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def gen_line_bound():
    # st_line = random.randint(0, im_width // 2)
    # end_line = random.randint(im_width // 2 + 1, im_width)
    # end_line = random.randint(max(im_width // 2 + 1, st_line + 100), im_width)
    # end_line = random.randint(im_width // 2, )

    # if random.random() > 0.5:
    #     thick_line = -random.randint(2, 4)
    # else:
    thick_line = random.randint(1, 4)

    return thick_line


def generate_box_char(imgCV, fontname, size=(40, 40),
                      fill='#000000',
                      chars=['保', '険', '契', '約', '金', '額', ], fontsize=int(40 * 0.8)):
    img = Image.fromarray(imgCV)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontname, fontsize)

    offset_tmp = int(fontsize * 0.1)
    # offset_tmp = int(fontsize * 0.0005)
    # adjust
    for i in range(len(chars)):
        char = chars[i]
        # TODO: change fill value.
        # draw.text((0 + offset_tmp, 0 + offset_tmp), char, font=font, fill=fill)
        draw.text((0 + offset_tmp, 0), char, font=font, fill=fill)

    # img.save('filepath.png', 'png')
    return img


def generate_box_char_v3(imgCV, fontname, size=(40, 40),
                      fill='#000000',
                      chars=['保', '険', '契', '約', '金', '額', ], fontsize=int(40 * 0.8)):
    img = Image.fromarray(imgCV)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontname, fontsize)

    # offset_tmp = int(fontsize * 0.1)
    # offset_tmp = 0
    offset_tmp = int(fontsize * 0.08)
    # offset_tmp = int(fontsize * 0.0005)
    # adjust
    for i in range(len(chars)):
        char = chars[i]
        # TODO: change fill value.
        # draw.text((0 + offset_tmp, 0 + offset_tmp), char, font=font, fill=fill)
        # draw.text((0 + offset_tmp, 0), char, font=font, fill=fill)
        if not char.isdigit():
            draw.text((0 + offset_tmp, 0 - 3*offset_tmp), char, font=font, fill=fill)
        else:
            fontsize = int(fontsize * 0.995)
            draw.text((0 + 4 * offset_tmp, 0 - 4*offset_tmp), char, font=font, fill=fill)

        # draw.text((0, 0 + offset_tmp), char, font=font, fill=fill)

    # img.save('check_char.png', 'png')
    return img


def generate_box_char_v2(imgCV, fontname,
                      fill='#000000',
                      chars=['保', '険', '契', '約', '金', '額', ],
                      fontsize=int(40 * 0.8)):

    """
    v2 improve from v3
    :param imgCV:
    :param fontname:
    :param size:
    :param fill:
    :param chars:
    :param fontsize:
    :return:
    """
    img = Image.fromarray(imgCV)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(fontname,
                              fontsize
                              )

    # offset_tmp = 0
    offset_tmp = int(fontsize * 0.08)
    # adjust
    for i in range(len(chars)):
        char = chars[i]
        # TODO: change fill value.
        # draw.text((0, 0-5*offset_tmp), char, font=font, fill=fill)
        # draw.text((0, 0)+img.size, char, font=font, fill=fill)
        draw.text((0, 0-2*offset_tmp), char, font=font, fill=fill)
    return img


def gen_background_white_color(kind, **kwargs):
    if kind == 'inversion_area':
        tmp_random = random.random()
        if tmp_random >= 0.9:
            white_color = [255] * 3
        elif tmp_random >= 0.15:
            white_color = [random.randint(245, 255)] * 3
        else:
            white_color = [random.randint(245, 255), random.randint(245, 255), random.randint(245, 255)]
        return white_color

    elif kind == 'dotted_line':
        if random.random() >= 0.15:
            white_color = [random.randint(245, 255)] * 3
        else:
            white_color = [random.randint(245, 255), random.randint(245, 255), random.randint(245, 255)]
        return white_color

    elif kind == 'text':
        lower_v = kwargs.get('lower_v', 245)
        if random.random() >= 0.15:
            white_color = [random.randint(lower_v, 255)] * 3
        else:
            white_color = [random.randint(lower_v, 255), random.randint(lower_v, 255), random.randint(lower_v, 255)]
        return white_color


def gen_black_color(threshold_color=50, threshold_color2=100, threshold1=0.1, threshold2=0.7, threshold=0.5):
    # gen color of chars
    tmp_random = random.random()
    if tmp_random < threshold1:
        black_color = [0, 0, 0]
    elif tmp_random <= threshold2:
        # 3 chanel are equal
        if random.random() >= threshold:
            black_color = [random.randint(0, threshold_color)] * 3
        else:
            black_color = [random.randint(threshold_color, threshold_color2)] * 3
    else:
        # 3 chanel are different
        black_color = random.randint(0, threshold_color), \
                      random.randint(0, threshold_color), \
                      random.randint(0, threshold_color)
    return black_color


def gen_font_path(list_fonts):
    return random.choice(list_fonts)


def gen_jpg_quality(kind):
    if kind == 'inversion_area':
        tmp_random = random.random()
        if tmp_random < 0.3:
            jpg_quality = random.randint(0, 70)
        elif tmp_random < 0.9:
            jpg_quality = random.randint(70, 100)
        else:
            jpg_quality = 100

        return jpg_quality
    elif kind == 'dotted_line':
        tmp_random = random.random()
        if tmp_random < 0.3:
            jpg_quality = random.randint(15, 100)
        elif tmp_random < 0.9:
            jpg_quality = random.randint(70, 100)
        else:
            jpg_quality = 100
        # jpg_quality = 20
        return jpg_quality
    elif kind == 'text':
        tmp_random = random.random()
        if tmp_random < 0.3:
            jpg_quality = random.randint(15, 100)
        elif tmp_random < 0.9:
            jpg_quality = random.randint(70, 100)
        else:
            jpg_quality = 100
        # jpg_quality = 20
        return jpg_quality
    else:
        raise ValueError("kind = {} not support!".format(kind))


def random_choices(seq, k=1):
    return [random.choice(seq) for _ in range(k)]


def gen_chars_list(char_in_text, dict_lines, min_len, max_len,
                   threshold_1=0.4, threshold_2=0.8,
                   index_replace=None, chars_replace=None):
    """

    :param index_replace:
    :param chars_replace: suggest values: ["1", "・"]
    :param char_in_text:
    :param dict_lines:
    :param int min_len:
    :param int max_len:
    :param float threshold_1: ti le su dung dict_lines
    :param float threshold_2: ti le replace char
    :return:
    """

    if random.random() > threshold_1:
        # normal
        chars_list = random_choices(char_in_text, k=random.randint(min_len, max_len))
    else:
        line = list(random.choice(dict_lines))
        len_line = len(line)
        if len_line > max_len:
            start = random.randint(0, len_line - max_len)
            return line[start:start+max_len]
        if len_line < min_len:
            line.extend(random_choices(char_in_text, k=min_len-len_line))
        # return line
        chars_list = line
        return chars_list

    if chars_list and chars_replace:
        if random.random() < threshold_2:
            if index_replace is not None and index_replace < len(chars_list):
                chars_list[index_replace] = random.choice(chars_replace)
            else:
                chars_list[random.randint(0, len(chars_list)-1)] = random.choice(chars_replace)
    return chars_list


def gen_chars_list_v4(char_in_text, min_len, max_len,
                   threshold_2=0.8,
                   index_replace=None, chars_replace=None):
    """

    :param index_replace:
    :param chars_replace: suggest values: ["1", "・"]
    :param char_in_text:
    :param dict_lines:
    :param int min_len:
    :param int max_len:
    :param float threshold_1: ti le su dung dict_lines
    :param float threshold_2: ti le replace char
    :return:
    """
    length = random.randint(min_len, max_len)

    if isinstance(char_in_text, list):
        # normal
        chars_list = random_choices(char_in_text, k=length)

        if chars_list and chars_replace:
            if random.random() < threshold_2:
                if index_replace is not None and index_replace < len(chars_list):
                    chars_list[index_replace] = random.choice(chars_replace)
                else:
                    chars_list[random.randint(0, len(chars_list)-1)] = random.choice(chars_replace)
        return chars_list
    else:
        chars_list = []
        if length:
            for char in char_in_text:
                chars_list.append(char)
                if len(chars_list) == length:
                    break
        return chars_list


def random_size_char(x=25, y=65):
    """
    Gen randomly fontsize and box_size and ratio of these.
    :param x:
    :param y:
    :return:
    """
    # fontsize = int(random.randint(20, 50)*0.8)
    # fontsize = int(random.randint(30, 65)*0.8)
    # fontsize = int(random.randint(40, 65)*0.8)
    fontsize = int(random.randint(x, y) * 0.8)
    # box_size = int(fontsize*1.6)
    # box_size = int(fontsize*1.1)
    ratio = random.uniform(1.005, 1.08)
    # box_size = int(fontsize*1.005)
    box_size = int(fontsize * ratio)
    return fontsize, box_size


def random_size_char_v2(x=20, y=65):
    """
    Gen randomly fontsize and box_size and ratio of these.
    :param x:
    :param y:
    :return:
    """
    fontsize = int(random.randint(x, y) * 0.8)
    ratio = random.uniform(1.005, 1.08)
    box_size = int(fontsize * ratio)
    return fontsize, box_size


def random_extra_box_size():
    """
    Gen randomly the extra_box_size, this is padding between 2 sentence lines.
    padding = 2 * extra_box_size
    :return:
    """
    tmp_random = random.random()
    if tmp_random > 0.7:
        extra_box_size = random.randint(4, 6)
    else:
        extra_box_size = random.randint(2, 4)
    return extra_box_size
