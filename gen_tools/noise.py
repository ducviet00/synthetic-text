import random
import numpy as np


def noisy_inversion_models(noise_typ, image, **kwargs):
    """
    Parameters
    ----------
    image : ndarray
        Input image data. Will be converted to float.
    mode : str
    One of the following strings, selecting the type of noise to add:

    'gauss'     Gaussian-distributed additive noise.
    'poisson'   Poisson-distributed noise generated from the data.
    's&p'       Replaces random pixels with 0 or 1.
    'speckle'   Multiplicative noise using out = image + n*image,where
                n is uniform noise with specified mean & variance.
    :param noise_typ:
    :param image:
    :return:
    """
    if noise_typ is None:
        return image.copy()
    if noise_typ == "gauss":
        row, col, ch = image.shape
        mean = 0
        var = 0.1
        # var = 10
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return noisy
    elif noise_typ == "s&p":
        row, col, ch = image.shape
        # s_vs_p = 0.5
        s_vs_p = kwargs.get('threshold_sp', 0.5)
        # amount = 0.004
        out = np.copy(image)

        # Pepper mode
        pepper_amount = 0.001
        num_pepper = np.ceil(pepper_amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0

        # Salt mode
        salt_amount = 0.01
        num_salt = np.ceil(salt_amount * image.size * s_vs_p)
        # num_salt = np.ceil(salt_amount * row * col * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[coords] = 255
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        # print("np.ceil(np.log2(vals)):", np.ceil(np.log2(vals)))
        # print("vals", vals)
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy

    elif noise_typ == "speckle":
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss
        return noisy

    elif noise_typ == "white_in_black":
        row, col, ch = image.shape
        out = image.copy()
        for r in range(row):
            for c in range(col):
                if (out[r, c] <= 100).all():
                    # if random.random() <= 0.02:
                    if random.random() <= kwargs.get('threshold_random_1', 0.02):
                        out[r, c] = [random.randint(250, 255)] * 3
                        # if r != 0 and r != row - 1 and c != 0 and c != col - 1 and random.random() <= 0.5:
                        if r != 0 and r != row - 1 and c != 0 and c != col - 1 \
                                and random.random() <= kwargs.get('threshold_random_2', 0.5):
                            out[r + random.choice([-1, 0, 1]), c + random.choice([-1, 0, 1])] = \
                                [random.randint(250, 255)] * 3
        return out
    else:
        raise Exception("noise_typ:{} is wrong!".format(noise_typ))


def noisy_dotted_line(noise_typ, image):
    """
    Parameters
    ----------
    image : ndarray
        Input image data. Will be converted to float.
    mode : str
    One of the following strings, selecting the type of noise to add:

    'gauss'     Gaussian-distributed additive noise.
    'poisson'   Poisson-distributed noise generated from the data.
    's&p'       Replaces random pixels with 0 or 1.
    'speckle'   Multiplicative noise using out = image + n*image,where
                n is uniform noise with specified mean & variance.
    :param noise_typ:
    :param image:
    :return:
    """
    if noise_typ is None:
        return image.copy()
    if noise_typ == "gauss":
        row, col, ch = image.shape
        mean = 0
        var = 0.1
        # var = 10
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return noisy
    elif noise_typ == "s&p":
        row, col, ch = image.shape
        s_vs_p = 0.5
        # amount = 0.004
        out = np.copy(image)

        # Pepper mode
        pepper_amount = 0.001
        num_pepper = np.ceil(pepper_amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0

        # Salt mode
        salt_amount = 0.01
        num_salt = np.ceil(salt_amount * image.size * s_vs_p)
        # num_salt = np.ceil(salt_amount * row * col * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        # out[coords] = 1
        out[coords] = 255
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy

    elif noise_typ == "speckle":
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss
        return noisy

    elif noise_typ == "white_in_black":
        row, col, ch = image.shape
        out = image.copy()
        for r in range(row):
            for c in range(col):
                if (out[r, c] <= 100).all():
                    # or ((out[r, c] <= 100).all() and out[r, c, 0] == out[r, c, 1] and out[r, c, 1] == out[r, c, 2]):
                    if random.random() <= 0.02:
                        # out[r, c] = WHITE
                        out[r, c] = [random.randint(250, 255)]*3
                        if r != 0 and r != row-1 and c != 0 and c != col - 1 and random.random() <= 0.5:
                            out[r + random.choice([-1, 0, 1]), c + random.choice([-1, 0, 1])] = [random.randint(250, 255)]*3
        return out
    else:
        raise Exception("noise_typ:{} is wrong!".format(noise_typ))


def noisy_crnn(noise_typ, image):
    """
    Parameters
    ----------
    image : ndarray
        Input image data. Will be converted to float.
    mode : str
    One of the following strings, selecting the type of noise to add:

    'gauss'     Gaussian-distributed additive noise.
    'poisson'   Poisson-distributed noise generated from the data.
    's&p'       Replaces random pixels with 0 or 1.
    'speckle'   Multiplicative noise using out = image + n*image,where
                n is uniform noise with specified mean & variance.
    :param noise_typ:
    :param image:
    :return:
    """
    if noise_typ is None:
        return image.copy()
    if noise_typ == "gauss":
        row, col, ch = image.shape
        mean = 0
        # var = 0.1
        var = 10
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return noisy
    elif noise_typ == "s&p":
        row, col, ch = image.shape
        s_vs_p = 0.5
        # amount = 0.004
        out = np.copy(image)

        # Pepper mode
        pepper_amount = 0.001
        num_pepper = np.ceil(pepper_amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0

        # Salt mode
        salt_amount = 0.01
        num_salt = np.ceil(salt_amount * image.size * s_vs_p)
        # num_salt = np.ceil(salt_amount * row * col * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        # out[coords] = 1
        out[coords] = 255
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy

    elif noise_typ == "speckle":
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss
        return noisy

    elif noise_typ == "white_in_black":
        row, col, ch = image.shape
        out = image.copy()
        for r in range(row):
            for c in range(col):
                if (out[r, c] <= 100).all():
                    # or ((out[r, c] <= 100).all() and out[r, c, 0] == out[r, c, 1] and out[r, c, 1] == out[r, c, 2]):
                    if random.random() <= 0.02:
                        # out[r, c] = WHITE
                        out[r, c] = [random.randint(250, 255)]*3
                        if r != 0 and r != row-1 and c != 0 and c != col - 1 and random.random() <= 0.5:
                            out[r + random.choice([-1, 0, 1]), c + random.choice([-1, 0, 1])] = [random.randint(250, 255)]*3
        return out
    else:
        raise Exception("noise_typ:{} is wrong!".format(noise_typ))