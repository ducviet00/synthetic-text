import glob
import os

from fontTools.ttLib import TTFont
from PIL import ImageFont


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
