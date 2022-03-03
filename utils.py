def read_file(path):
    with open(path, 'r') as f_in:
        lines = f_in.readlines()
    filter_lines = set()
    for line in lines:
        filter_lines.add(line.strip())
    return list(filter_lines)

def write_txt(vocab, path):
    with open(path, 'w') as f_out:
        f_out.write("\n".join(vocab))
