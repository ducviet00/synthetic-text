

def read_dict_file(path):
    """
    return
    :param path:
    :return:
    """
    list_lines = []
    max_len = None
    with open(path, encoding='utf-8') as fi:
        for line in fi:
            line = line.strip()
            if line:
                len_line = len(line)
                if max_len is None or max_len < len_line:
                    max_len = len_line
                list_lines.append(line)

    print("File", path, "Len dict", len(list_lines), "Max_len", max_len)
    return list_lines, max_len
