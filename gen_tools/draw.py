import numpy as np
import random
from gen_tools.noise import noisy_inversion_models, noisy_dotted_line
import cv2


def draw_shadow(img, shape, kind_shadow):
    ny, nx = shape
    y, x = np.mgrid[:ny, :nx]
    #     print(y.shape, x.shape)
    gradient = x * y / 5000
    # gradient ^= 255
    #     print(np.max(gradient))
    len_shape = len(img.shape)

    gradient = gradient / np.max(gradient) * np.sqrt(ny ** 2 + nx ** 2) / 9
    img_fake = img.copy()
    img_fake = img_fake.astype(np.float64)
    #     kind_shadow = 'topleft'
    if len_shape == 3:
        gradient = np.expand_dims(gradient, -1)

    if kind_shadow == 'topleft':
        gradient = gradient[::-1, ::-1]
        img_fake[:ny, :nx] -= gradient
    elif kind_shadow == 'topright':
        gradient = gradient[::-1, :]
        img_fake[:ny, -nx:] -= gradient
    elif kind_shadow == 'bottomleft':
        gradient = gradient[:, ::-1]
        img_fake[-ny:, :nx] -= gradient
    elif kind_shadow == 'bottomright':
        gradient = gradient
        img_fake[-ny:, -nx:] -= gradient

    #     print("gradient", np.max(gradient), np.min(gradient))

    #     img_fake = img - gradient
    #     print(np.max(img_fake), np.min(img_fake))

    img_fake -= np.min(img_fake)
    img_fake /= np.max(img_fake)
    img_fake *= 255
    # img_fake = np.clip(img_fake, 0, 255)

    #     print(np.max(img_fake), np.min(img_fake))

    #     show_img(img_fake, gray=True, figsize=(20,20))
    return img_fake.astype(np.uint8)


def draw_solid_line(img, rect_x, rect_y, rect_w, rect_h, color):
    img[rect_y: rect_y+rect_h, rect_x: rect_x+rect_w] = color


def draw_bounding_box(img, rect_x, rect_y, rect_w, rect_h, thickness, color, kind_box):
    """

    :param img:
    :param rect_x:
    :param rect_y:
    :param rect_w:
    :param rect_h:
    :param thickness:
    :param color:
    :param kind_box:
    :return:
    """
    assert kind_box in [2, 4]
    draw_solid_line(img, rect_x, rect_y, rect_w, thickness, color)
    draw_solid_line(img, rect_x, rect_y, thickness, rect_h, color)

    if kind_box == 4:
        draw_solid_line(img, rect_x, rect_y+rect_h, rect_w+thickness, thickness, color)
        draw_solid_line(img, rect_x+rect_w, rect_y, thickness, rect_h+thickness, color)


def draw_noise(img, kind='dotted_line'):
    """
    Draw noise to image.
    :param img:
    :param kind:
    :return:
    """
    if kind == 'inversion_area':
        tmp_random = random.random()
        if tmp_random < 0.4:
            noise_type = 'gauss'
        else:
            noise_type = None

        img = noisy_inversion_models(noise_type, img)

        if random.random() > 0.4:
            img = noisy_inversion_models("s&p", img,
                                         threshold_sp=0.3
                                         )
        if random.random() > 0.4:
            img = noisy_inversion_models("white_in_black", img,
                                         threshold_random_1=0.01,
                                         threshold_random_2=0.3
                                         )
    elif kind == 'dotted_line':

        if random.random() > 0.4:
            noise_type = 'gauss'
        elif random.random() > 0.1:
            noise_type = 'poisson'
        else:
            noise_type = None

        img = noisy_dotted_line(noise_type, img)

        if random.random() > 0.3:
            img = noisy_dotted_line("s&p", img)

        if random.random() > 0.2:
            img = noisy_dotted_line("white_in_black", img)

    elif kind == 'text':

        if random.random() > 0.4:
            noise_type = 'gauss'
        elif random.random() > 0.1:
            noise_type = 'poisson'
        else:
            noise_type = None

        img = noisy_dotted_line(noise_type, img)

        if random.random() > 0.3:
            img = noisy_dotted_line("s&p", img)
    else:
        raise ValueError("kind = {} not support!".format(kind))

    return img


# LIST_FILTER_SIZE = [_ for _ in range(3, 20, 2)]
LIST_FILTER_SIZE = [_ for _ in range(3, 20, 2)]


def noise_blur(img):
    # if img.shape[0] > 50:
    #     filter_size = random.choice(LIST_FILTER_SIZE)
    # else:
    #     filter_size = random.choice(LIST_FILTER_SIZE[: -5])

    filter_size = random.choice([3, 5])

    img = cv2.GaussianBlur(img, (filter_size, filter_size), 0)

    return img


def draw_noise_for_crnn(img):
    if random.random() > 0.4:
        noise_type = 'gauss'
    elif random.random() > 0.1:
        noise_type = 'poisson'
    else:
        noise_type = None

    img = noisy_dotted_line(noise_type, img)

    flag_noise = False
    if random.random() > 0.3:
        img = noisy_dotted_line("s&p", img)
        flag_noise = True

    if noise_type or flag_noise and random.random() < 0.8:
        img = noise_blur(img)

    return img


def gen_arr_duplicate(len_a, num_dup):
    a = np.zeros(len_a)
    for i in range(len_a):
        a[i] = i // num_dup
    return a


def draw_shadow_full(img, kind_shadow):
    ny, nx, _ = img.shape
    img_fake = img.copy()
    img_fake = img_fake.astype(np.float64)

    if kind_shadow == 'left' or kind_shadow == 'right':
        nx = random.randint(30, nx//2)

        duplicate = False
        if random.random() > 0.6:
            duplicate = True

        if duplicate:
            num_dup = 3
            if random.random() > 0.5:
                num_dup = 2

            a = gen_arr_duplicate(nx, num_dup)

            if random.random() > 0.4 and nx < 150:
                a = a * 3
            elif random.random() > 0.3 and nx < 150:
                a = a ** 2
        else:
            a = np.arange(0, nx)

            if random.random() > 0.4 and nx < 70:
                a = a * 3
            elif random.random() > 0.5 and nx < 50:
                a = a ** 2
        if kind_shadow == 'left':
            a = np.flip(a, axis=0)
        a[a > 150] = 150
        a = [a] * ny
        gradient = np.reshape(a, (len(a), len(a[0])))

        # nx = gradient.shape[1]
        if kind_shadow == 'left':
            img_fake[:ny, :nx] -= gradient[:, :, np.newaxis]
        elif kind_shadow == 'right':
            img_fake[:ny, img_fake.shape[1] - nx:] -= gradient[:, :, np.newaxis]
    elif kind_shadow == 'top' or kind_shadow == 'bottom':
        # if ny > 30:
        #     ny = random.randint(30, ny)
        # else:
        #     ny = random.randint(ny//4, ny)

        ny = random.randint(ny//4, ny)

        duplicate = False
        if random.random() > 0.6:
            duplicate = True

        if duplicate:
            num_dup = 2
            if random.random() > 0.5:
                num_dup = 3
            a = gen_arr_duplicate(ny, num_dup)  # Tao 1 array co do dai bang 1/num_dup cua shape

            # if random.random() > 0.4 and ny // num_dup < 80:
            #     a = a * 3
            # elif random.random() > 0.3 and ny // num_dup < 80:
            #     a = a ** 2
        else:
            a = np.arange(0, ny)

            # if random.random() > 0.4 and ny < 70:
            #     a = a * 3
            # elif random.random() > 0.5 and ny < 50:
            #     a = a ** 2
        a[a > 150] = 150
        if kind_shadow == 'top':
            a = np.flip(a, axis=0)

        a = [a] * nx
        gradient = np.reshape(a, (len(a), len(a[0])))
        gradient = gradient.T

        # ny, nx = gradient.shape
        if kind_shadow == 'top':
            img_fake[:ny, :nx] -= gradient[:, :, np.newaxis]
        elif kind_shadow == 'bottom':
            img_fake[img_fake.shape[0] - ny:, :nx] -= gradient[:, :, np.newaxis]
    # img_fake -= np.min(img_fake)
    # img_fake /= np.max(img_fake)
    # img_fake *= 255

    img_fake[img_fake < 0] = 0
    img_fake[img_fake > 255] = 255

    return img_fake.astype(np.uint8)
