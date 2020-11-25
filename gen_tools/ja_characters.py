import pickle

# def get_chars():
#     _char_in_txt = ""
#     for fn in CHARS_FILES:
#         with open(fn, encoding='utf-8') as fi:
#             # for line in fi:
#             #     char_in_txt.append(line.strip())
#             text = fi.read()
#             _char_in_txt += text.replace('\n', "").replace(" ", "").replace("\t", "").replace("\r", "")
#     _char_in_txt = list(set(_char_in_txt))
#     return _char_in_txt


# CHARS = [chr(i) for i in range(0x3000, 0x9FA5)]
# CHARS.extend([chr(i) for i in range(0xFF01, 0xFF9F)])
#
# CHARS = set(CHARS)
# print(len(CHARS))


# WIKI_CHARS = set()
#
# with open('/home/binhnq/VisualRecognition/infordio/hyper_document_generator/resources/all_wiki_chars.txt', encoding='utf-8') as fi:
#     for line in fi:
#         line = line.strip()
#         if line:
#             WIKI_CHARS.update(line)
#
# print(len(WIKI_CHARS))

# OCR_CHARS = set()
#
# with open('/home/binhnq/VisualRecognition/infordio/ocr/data0418/char_list.txt', encoding='utf-8') as fi:
#     text = fi.read()
#     OCR_CHARS.update(*text.replace('\n', "").replace(" ", "").replace("\t", "").replace("\r", ""))
#
# print(len(OCR_CHARS))

HIERARCHICAL_PATH = "resources/hierarchical_labels.pickle"


def process_ocr_chars():
    with open(HIERARCHICAL_PATH, 'rb') as fi:
        label_kinds = pickle.load(fi)

    char_dict = {
        'mozi': set()
    }

    all_chars = set()

    for kind in label_kinds:
        all_chars.update(label_kinds[kind])
        if kind in ['digit', 'symbol', 'alphabet']:
            char_dict[kind] = set(label_kinds[kind])
        else:
            char_dict['mozi'].update(label_kinds[kind])

    char_dict['all'] = all_chars

    return char_dict


def process_chr():

    chars = [chr(i) for i in range(0xFF01, 0xFF9F)]
    symbol = chars[:15]
    digit = chars[15:25]
    symbol.extend(chars[25:32])
    upper_char = chars[32: 58]
    symbol.extend(chars[58:64])
    lower_char = chars[64: 90]
    symbol.extend(chars[90:])

    return {
        'mozi': set([chr(i) for i in range(0x3000, 0x9FA5)]),
        'symbol': set(symbol),
        'digit': set(digit),
        'alphabet': set(upper_char+lower_char),
        'all': set([chr(i) for i in range(0x3000, 0x9FA5)] + chars)
    }


def _print_len(char_dict, name):
    for kind in sorted(char_dict):
        print("{name}_{kind}: {len}".format(name=name, kind=kind, len=len(char_dict[kind])))


def jp_chars():
    ocr_chars = process_ocr_chars()
    _print_len(ocr_chars, 'ocr')
    chr_chars = process_chr()
    _print_len(chr_chars, 'chr')

    return {
        'ocr': ocr_chars,
        'chr': chr_chars,
        # 'all': ocr_chars['all'].union(chr_chars['all'])
    }


JA_CHARS = jp_chars()


if __name__ == '__main__':
    list_chr_all = sorted([chr(i) for i in range(0x3000, 0x9FA5)] + [chr(i) for i in range(0xFF01, 0xFF9F)])
    # Write down all characters for chr().
    with open('chr_char_list.txt', 'w') as fo:
        for c in list_chr_all:
            fo.write('{}\n'.format(c))
