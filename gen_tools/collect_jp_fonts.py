import os
import glob


def collect_jp_fonts(fonts_folder):
	list_jp_font = []
	for fn in os.listdir(fonts_folder):
		fn_lower = fn.lower()
		if 'jp' in fn_lower and os.path.splitext(fn)[1] in ['.ttc', '.otf']:
			if 'kr' in fn_lower and 'sc' in fn_lower and 'tc' in fn_lower:
				assert 'kr' not in fn_lower, "Format failure kr!"
				assert 'sc' not in fn_lower, "Format failure sc!"
				assert 'tc' not in fn_lower, "Format failure tc!"

			list_jp_font.append(os.path.join(fonts_folder, fn))
	return list_jp_font


def filter_bold_black_fonts(list_fonts):
	list_out = []
	for font_name in list_fonts:
		font_name_lower = font_name.lower()
		if 'bold' in font_name_lower:
			list_out.append(font_name)
		elif 'black' in font_name_lower:
			list_out.append(font_name)
	return list_out


def collect_jp_fonts_extra(fonts_folder):
	list_jp_font = []
	for fn in os.listdir(fonts_folder):
		fn_lower = fn.lower()
		if os.path.splitext(fn_lower)[1] in ['.ttc', '.otf', '.ttf']:
			list_jp_font.append(os.path.join(fonts_folder, fn))

	return list_jp_font


def collect_jp_fonts_extra_2(fonts_folder, path_list_extra_fonts='resources/list_extra_fonts.txt'):
	list_jp_font = []
	with open(path_list_extra_fonts, 'r', encoding='utf-8') as fi:
		for line in fi:
			line = line.strip()
			if line:
				list_jp_font.append(os.path.join(fonts_folder, line))

	return list_jp_font


def collect_jp_fonts_extra_3(fonts_folder):
	jp_font_dict = {
		'all': [],
		'normal': []
	}
	list_font_path = os.path.join(fonts_folder, 'list_fonts.txt')
	with open(list_font_path, encoding='utf-8') as fi:
		for line in fi:
			line = line.strip()
			if line:
				fn, kind = line.split('\t')
				fn = os.path.join(fonts_folder, fn)
				if kind == 'All':
					jp_font_dict['all'].append(fn)
					jp_font_dict['normal'].append(fn)
				elif kind == 'Normal':
					jp_font_dict['normal'].append(fn)
	# assert len(jp_font_dict['normal']) == 20
	# assert len(jp_font_dict['all']) == 18
	return jp_font_dict['all']


def collect_font_number(fonts_folder):
	list_fonts = []
	files = glob.glob(os.path.join(fonts_folder, "*"))
	for file in files:
		list_fonts.append(file)
	return list_fonts
