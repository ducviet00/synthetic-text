import os
from utils import read_file

BOLD_BG_RATIO = 1.0 # SCENCE TEXT RATIO
SHADOW_RATIO = 0.5
BLUR_CHAR_RATIO = 0.1
CUT_TEXT_NOISE_RATIO = 0
VOCAB = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&''()*+,-./:;<=>?@[\]^_`{|}~ '
REPEAT_NUM = 1 # Number of repeating vocab times
MAX_LEN = 32
KIND_TEXT = 'text'

dict_gen = {}
dict_gen['vnwords'] = read_file("vnmesevocab.txt")
# dict_gen['wikiuni'] = read_file("unigram.txt")
# dict_gen['wikibi'] = read_file("bigram.txt")
# dict_gen['wikitri'] = read_file("trigram.txt")

OUTPUT_PATH = "~/synthetic/"
os.makedirs(OUTPUT_PATH, exist_ok=True)