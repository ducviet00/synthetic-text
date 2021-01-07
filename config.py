import os

#SCENCE TEXT
BOLD_BG_RATIO = 0.0
SHADOW_RATIO = 0.5
BLUR_CHAR_RATIO = 0
CUT_TEXT_NOISE_RATIO = 0
# CHARS_LIST_PATH = 'resources/chars/extra_char_list.txt'
# CHARS_LIST_PATH = 'resources/chars/char_list_INFD20191022.txt'
# CHARS_LIST_PATH = 'resources/chars/char_list_INFD20190806.txt'
# CHARS_LIST_PATH = 'resources/chars/char_list_INFD20190823.txt'
# CHARS_LIST_PATH = 'resources/chars/char_list_INFD20200202.txt'
# CHARS_LIST_PATH = 'resources/chars/char_list_INFD20200228.txt'
# CHARS_LIST_PATH = "resources/chars/char_list_INFD20200423.txt"
CHARS_LIST_PATH = "resources/chars/char_list_INFD20201020.txt"


# MAP_DICT_PATH = 'resources/chars/map_dict.json'
# MAP_DICT_PATH = 'resources/chars/map_dict_20190628_v3.json'
MAP_DICT_PATH = 'resources/chars/map_dict_20200820.json'

# MAX_LABELS_NO = 100
# MAX_LABELS_NO_TEST = 150

MAX_LABELS_NO = 240
MAX_LABELS_NO_TEST = 241

# ================= Start settings for architectures of CRNN =====================================
CNN_TYPE_VGG = "CNN_TYPE_VGG"
CNN_TYPE_RESNET = "CNN_TYPE_RESNET"
CNN_TYPE_PVANET = "CNN_TYPE_PVANET"
CNN_TYPE = CNN_TYPE_VGG
# CNN_TYPE = CNN_TYPE_RESNET

# Mappings from types to implementation names
CNN_IMPLEMENTATIONS = {
    CNN_TYPE_VGG: "vgg",
    CNN_TYPE_RESNET: "resnet",
    CNN_TYPE_PVANET: "pvanet",
}
# ================= End settings for architectures of CRNN =======================================

# ================= Settings for HANDWRITING ===================
HANDWRITING_SINGLE_CHARS_FOLDER = "datasets/hand_writing/single_chars/from_infordio"
HANDWRITING_TRAINING_FOLDER = "datasets/hand_writing/real_sequences"
# HANDWRITING_TRAINING_FOLDER = "datasets/hand_writing/training_data"
CROSS_OUT_TEXT_FOLDER = "datasets/hand_writing/cross_out_text"
HANDWRITING_OFFLINE_RATIO = 0.4
CROSS_OUT_TEXT_RATIO = 0.2
HANDWRITING_SINGLE_CHAR_RATIO = 0.2
TRAINING_DATA_REAL_PRINT_RATIO = 0.05
TRAINING_DATA_SYNOFFLINE_RATIO = 0.05
DIFFICULT_REAL_IMGS_RATIO=0.1

HANDWRITING_ONLINE_RATIO = 1.0
DISTORT_SCALES = [0.8, 1.2]
DISTORT_SINGLE_CHAR_RATIO = 0.3
CONTRAST_CHAR_AUGMENT_RATIO = 0.4
DISTORT_ELASTIC_RATIO = 0.3
THRESHOLD_ITALIC_AUGMENT = 0.0
DASH_LINE_RATIO = 0.2
CLOSED_BORDER_SYNTHESIS = True

# ================= EXPERIMENTAL: Settings and constants for handling special characters =============================
SPECIAL_CHARS_PATH = "resources/chars/special_chars.py"
SPECIAL_CHARS_MAP_TO = "map_to"
SPECIAL_CHARS_IMGS_DIR = "imgs_dir"
SPECIAL_CHARS_IMGS = "imgs"
HAS_SPECIAL_CHARS = False
# HAS_SPECIAL_CHARS = True
SPECIAL_CHARS_DATA_RATIO = 0.0
# ====================================================================================================================

ACCEPTING_IMG_EXTENSIONS = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]

# ================= Settings and constants for freezing and incremental learning =====================================
FREEZING_NORMAL_CHARS = False
FREEZING_RNN = False
FREEZING_CNN = False
NUMBER_OF_NEW_CHARS= 0
BASE_LEARNING_RATE = 1e-5 # The base learning rate
CNN_LEARNING_RATE = 1  # The learning rate of CNN = CNN_LEARNING_RATE*NORMAL_LEARNING_RATE
RNN_LEARNING_RATE = 1 # The learning rate of RNN = RNN_LEARNING_RATE*NORMAL_LEARNING_RATE
FC_LEARNING_RATE_FOCUS_CHARS = 1 # The learning rate of FC = FC_LEARNING_RATE*NORMAL_LEARNING_RATE
FC_LEARNING_RATE_NORMAL_CHARS = 1 # The learning rate of FC = FC_LEARNING_RATE*NORMAL_LEARNING_RATE
# COPY_SPACE_WEIGHTS_TO_NEW_CHARS = True
COPY_SPACE_WEIGHTS_TO_NEW_CHARS = False
DATA_ONLY_NEW = False
SINGLE_CHAR_RATIO = 0.05
NEW_DATA_RATION = 0.05
FC_FOCUS_CHARS_VAR_NAME="FC_FOCUS_CHARS_VAR_NAME"
FC_NORMAL_CHARS_VAR_NAME="FC_NORMAL_CHARS_VAR_NAME"
# FOCUS_CHARS = [ "⊕", "⊝", "〃"]
FOCUS_CHARS = []
# FOCUS_CHARS = ["⊕", "⊝", "〃"]
# FOCUS_CHARS = ["Ä", "È", "à", "§", "〃"]
#[ "⊕", "⊝", "〃"]
# FOCUS_CHARS = ["〃", "カ", "力", '請', "詰", "油", "汕", "齒", "歯", "縱", "縦", "豸", "孝", "丿", "ノ", "{","⊕", "⊝"]
# FOCUS_CHARS=["㈱", "㈲", "㈹", "㊤", "㊥", "㊦", "㊧", "㊨", "㌃", "㌍", "㌔", "㌘", "㌢", "㌣", "㌦", "㌧", "㌫", "㌶", "㌻", "㍉", "㍊", "㍍", "㍑", "㍗", "㎡"]
FOCUS_CHARS_RATIO = 0
INSERT_SPACE_RATION = 0.0
INSERT_SPACE_MAX_NO = 3
# =====================================================================================================================

# ================= Settings and constants for transfer learning ======================================================
TRANSFER_LEARNING_TYPE_OLD_TO_NEW = "TRANSFER_LEARNING_TYPE_OLD_2_NEW"
TRANSFER_LEARNING_TYPE_NEW_TO_NEW = "TRANSFER_LEARNING_TYPE_NEW_2_NEW"
TRANSFER_LEARNING_TYPE = TRANSFER_LEARNING_TYPE_NEW_TO_NEW
# TRANSFER_LEARNING_TYPE = TRANSFER_LEARNING_TYPE_NEW_TO_NEW
# =====================================================================================================================


# ================= Settings and constants for resizing images ======================================================
RESIZE_SCALES = [0.8, 2.]
# =====================================================================================================================
#CONFIG_PKL_FILE
# SENTENCES_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/sentences_20200202.pkl'
# INDICES_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/indices_20200202.pkl'
# SENTENCES_REAL_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/sentences_real{}_20200202.pkl' # {} = _vert or _hori which fixed in code
# INDICES_REAL_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/indices_real{}_20200202.pkl' # {} = _vert or _hori which fixed in code

SENTENCES_PKL = '/home/vsocr/workspace_hieu_infordio3_ssd3/crnn_train_data/dev/sentences_20200228.pkl'
INDICES_PKL = '/home/vsocr/workspace_hieu_infordio3_ssd3/crnn_train_data/dev/indices_20200228.pkl'
SENTENCES_REAL_PKL = '/home/vsocr/workspace_hieu_infordio3_ssd3/crnn_train_data/dev/sentences_real{}_20200228.pkl' # {} = _vert or _hori which fixed in code
INDICES_REAL_PKL = '/home/vsocr/workspace_hieu_infordio3_ssd3/crnn_train_data/dev/indices_real{}_20200228.pkl'
INITIAL_FREQ_ANAL_FILE = "/home/vsocr/workspace_hieu_infordio3_ssd3/crnn_eval_data/high_quality/test/analysis_chars_weights.427-3.67977.csv"

# SENTENCES_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/sentences.pkl'
# INDICES_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/indices.pkl'
# SENTENCES_REAL_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/sentences_real{}.pkl' # {} = _vert or _hori which fixed in code
# INDICES_REAL_PKL = '/home/vsocr/workspace_hieu_infordio_ssd2/crnn_train_data/dev/indices_real{}.pkl'

# ================= Settings and constants for real sentences =========================================================
REAL_SENS_DIR = 'resources/real_sequences/'
DICT_SENS='resources/dict'
LIST_DICT_PATH = [
    'resources/dict.txt',
    os.path.join(REAL_SENS_DIR, 'kenshinsho_dict.txt'),
    os.path.join(REAL_SENS_DIR, 'kenshinsho_operator.txt'),
    os.path.join(REAL_SENS_DIR, 'kenshinsho_unit.txt'),
    os.path.join(REAL_SENS_DIR, 'title_list.txt'),
    os.path.join(REAL_SENS_DIR, 'real_sen_65.txt'),
    os.path.join(REAL_SENS_DIR, '20190718_bad_crnn.txt'),
    os.path.join(REAL_SENS_DIR, 'blurred.txt'),
    os.path.join(REAL_SENS_DIR, 'blurred_v2.txt'),
    os.path.join(REAL_SENS_DIR, 'hybrid_invert_100c-p.txt'),
    os.path.join(REAL_SENS_DIR, 'OCR読取テスト.txt'),
    os.path.join(REAL_SENS_DIR, 'additional.txt'),
    # os.path.join(REAL_SENS_DIR, 'ope_train.txt'),
    os.path.join(REAL_SENS_DIR, 'dict_20190823.txt'),
    os.path.join(REAL_SENS_DIR, 'ope.txt'),
    os.path.join(REAL_SENS_DIR, 'ope_3.txt'),
    os.path.join(REAL_SENS_DIR, 'dict_20191129.txt'),
    os.path.join(REAL_SENS_DIR, 'kashikin_191203.txt'),
    os.path.join(REAL_SENS_DIR, 'kashikin_20191227.txt'),
    os.path.join(REAL_SENS_DIR, 'address_20200311.txt'),
    os.path.join(REAL_SENS_DIR, 'lastname_20200311.txt'),
    os.path.join(REAL_SENS_DIR, '20200311_hw_dict.txt'),
    os.path.join(REAL_SENS_DIR, 'dict_hw_collections_v1.txt'),
    # '''sua hehre'''
]
n = len(LIST_DICT_PATH) - 4
p = 1 - 0.7
LIST_DICT_FILE_PROB = [p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n, p/n,  p/n, p/n, p/n, 0.1, 0.1, 0.2, 0.3]
# LIST_DICT_FILE_PROB = None

GEN_CHAR_OR_DIGIT_RATIO = 0.2

LIST_FONTS = [
    'resources/20_fonts/',
    'resources/fonts_number',
    'resources/ominus_font',
    'resources/calligraphy_font',
    'resources/hw_font',
    '../noto-cjk/',
] #following this order, do not change!

LIST_FONTS_PROB = [0.1, 0.0, 0.1, 0.2, 0.5, 0.1]

LIST_DICT_SENS=[
    os.path.join(DICT_SENS, 'financial_words.txt'),
    os.path.join(DICT_SENS, 'dict.txt'),
    os.path.join(DICT_SENS, 'mecab.txt')
]
NEW_DICT_SELECTION_PROB = [0.00039306917465410467,0.044250093574754366,0.9553568372505916]
# =====================================================================================================================


# ================= Settings and constants for developping, DONT TOUCH IF YOU DONT UNDERSTAND WELL ====================
# balancing version: 0: no balancing,
#                    1: simply iterates all the characters,
#                    2: ignore characters already appeared in one iteration
#                    3: balancing by selecting the worse characters first, the error_rate is substracted
#                           by 5 after each selection,
#                    4: balancing by selecting the worse characters first, the error_rate is updated right
#                           away after each iteration
BALANCING_VERSION_0=0
BALANCING_VERSION_1=1
BALANCING_VERSION_2=2
BALANCING_VERSION_3=3
BALANCING_VERSION_4=4
BALANCING_VERSION_5=5
BALANCING_VERSION=BALANCING_VERSION_5
# BALANCING_VERSION = BALANCING_VERSION_0
USE_REAL_OR_PRE_GENERATED_IMGS=True
# USE_REAL_OR_PRE_GENERATED_IMGS=False
# =====================================================================================================================

_threshold_gen_chars_or_digit_1 = {
    'digit': 0.2,
    'alphabet': 0.35,
    'alphabet_digit': 0.5,
    'dict_sen': 0.7,
    # 'all': con lai
}

_threshold_gen_chars_or_digit_2 = {
    'digit': 0.4,
    'alphabet': 0.55,
    'alphabet_digit': 0.7,
    'dict_sen': 0.8,
    # 'all': con lai
}

_threshold_gen_chars_or_digit_21 = {
    'digit': 0.35,
    'alphabet': 0.5,
    'alphabet_digit': 0.55,
    'dict_sen': 0.65,
    'email': 0.85
    # 'all': con lai
}

_threshold_gen_chars_or_digit_22 = {
    'digit': 0.35,
    'alphabet': 0.4,
    'alphabet_digit': 0.45,
    'dict_sen': 0.8,
    'email': 0.9
    # 'all': con lai
}

_threshold_gen_chars_or_digit_23 = {
    'digit': 0.25,
    'alphabet': 0.3,
    'alphabet_digit': 0.35,
    'dict_sen': 0.7,
    'email': 0.8,
    'date_chars': 0.95
    # 'all': con lai
}

# _threshold_gen_chars_or_digit_23 = {
#     'digit': 0.8,
#     'alphabet': 0.45,
#     'alphabet_digit': 0.5,
#     'dict_sen': 0.75,
#     'email': 0.8,
#     'date_chars': 0.95
#     # 'all': con lai
# }

threshold_gen_chars_or_digit = _threshold_gen_chars_or_digit_23
CROP_TIGHT_TEXT_RATIO = 1.0

ITALIC_ON_REAL = False
sumary_dir = "/home/vsocr/workspace_hieu_infordio_ssd2/crnn_eval_data/summary_eval/"
#============================
MAX_LABELS_SYNTHESIS = 52
img_w = 1920
# img_w = 820
img_h = 32
pool_size = 2
activation = 'relu'


# configs for post-processing crnn
remove_duplicate_kanji=False
prioritize_number_in_single_char=False