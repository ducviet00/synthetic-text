import random


def add_stack_kind_text_no_split(chars_list, rect_x, rect_y, most_right, most_bottom, box_size,
                                 flag_random_of_char, axis, stack):
    """
    Add a stack to KIND TEXT.

    :param chars_list:
    :param rect_x:
    :param rect_y:
    :param most_right:
    :param most_bottom:
    :param box_size:
    :param flag_random_of_char:
    :param axis:
    :param stack:
    :return:
    """
    # TODO: if lastest character == ) thi chinh gia tri weight giam xuong.
    # TODO: dieu chinh rect_y cho phu hop, khi flag_random_of_char == True
    # if flag_random_of_char:
    #     box_size += 2
    if axis == 1:

        # height = box_size
        height = box_size - 4    # TODO: dung ti le tuong tu `int(10*(box_size/33))`
        # weight = min(len(chars_list), most_right - rect_x//box_size) * box_size - 14
        min_len = min(len(chars_list), (most_right - rect_x)//box_size)
        weight = min_len * box_size - int(10*(box_size/33))
        # rect_x_2 = rect_x + box_size * real_len_chars

    elif axis == 0:
        # if FLAG_CHECK_BIG_TITLE:
        #     raise ValueError("WTF?")
        # hight = min(len(chars_list), most_bottom - rect_y//box_size) * box_size
        min_len = min(len(chars_list), (most_bottom - rect_y)//box_size)
        height = min_len * box_size - 4
        # weight = box_size - 14
        weight = box_size - int(10*(box_size/33))

    stack.append((rect_x, rect_y+4, weight, height-4, chars_list[:min_len]))


def add_stack_kind_text_no_split_v3(chars_list, rect_x, rect_y, most_right, most_bottom, box_size,
                                 flag_random_of_char, axis, stack):
    """
    Add a stack to KIND TEXT.

    :param list chars_list:
    :param rect_x:
    :param rect_y:
    :param most_right:
    :param most_bottom:
    :param box_size:
    :param flag_random_of_char:
    :param axis:
    :param stack:
    :return:
    """
    # TODO: if lastest character == ) thi chinh gia tri weight giam xuong.
    # TODO: dieu chinh rect_y cho phu hop, khi flag_random_of_char == True
    # if flag_random_of_char:
    #     box_size += 2
    count_none = chars_list.count(None)

    if axis == 1:

        height = box_size
        min_len = min(len(chars_list), (most_right - rect_x)//box_size)
        # weight = min_len * box_size - int(10*(box_size/33))
        weight = min_len * box_size - count_none*box_size
        rect_x += count_none*box_size

    elif axis == 0:
        min_len = min(len(chars_list), (most_bottom - rect_y)//box_size)
        # height = min_len * box_size - 4
        height = min_len * box_size - count_none*box_size
        # weight = box_size - int(10*(box_size/33))
        weight = box_size
        rect_y += count_none*box_size

    stack.append((rect_x, rect_y, weight, height, chars_list[count_none:min_len]))


def add_stack_kind_text_split(char, index, rect_x, rect_y, of, box_size, axis, stack):
    rand_of_x = random.randint(-1, 1)
    rand_of_y = random.randint(-1, 1) + 4
    rand_of_box_size_x = random.randint(-1, 1) - int(10*(box_size/33))
    rand_of_box_size_y = random.randint(-1, 1) - 4 - 4
    if axis == 1:
        # stack.append((rect_x+box_size*index-of, rect_y-of, box_size, box_size, [char]))
        stack.append((rect_x+box_size*index-of+rand_of_x, rect_y-of+rand_of_y,
                      box_size+rand_of_box_size_x, box_size+rand_of_box_size_y, [char]))
    elif axis == 0:
        # stack.append((rect_x-of, rect_y+box_size*index-of, box_size, box_size, [char]))
        stack.append((rect_x-of+rand_of_x, rect_y+box_size*index-of+rand_of_y,
                      box_size+rand_of_box_size_x, box_size+rand_of_box_size_y, [char]))


def add_stack_kind_text_split_v3(char, index, rect_x, rect_y, of, box_size, axis, stack):
    """

    :param str char:
    :param index:
    :param rect_x:
    :param rect_y:
    :param of:
    :param box_size:
    :param axis:
    :param stack:
    :return:
    """
    if not char.isdigit():
        rand_of_x = random.randint(-1, 1)
        rand_of_y = random.randint(-1, 1)
        rand_of_box_size_x = random.randint(-1, 1)
        rand_of_box_size_y = random.randint(-1, 1)
        if axis == 1:
            stack.append((rect_x+box_size*index-of+rand_of_x, rect_y-of+rand_of_y,
                          box_size+rand_of_box_size_x, box_size+rand_of_box_size_y, [char]))
        elif axis == 0:
            stack.append((rect_x-of+rand_of_x, rect_y+box_size*index-of+rand_of_y,
                          box_size+rand_of_box_size_x, box_size+rand_of_box_size_y, [char]))

    else:
        rand_of_x = random.randint(-1, 1)
        rand_of_y = random.randint(-1, 1)
        rand_of_box_size_x = random.randint(-1, 1)
        rand_of_box_size_y = random.randint(-1, 1)

        new_of_x = random.randint(1, 3)
        # new_of_y = random.randint(1, 2)
        new_of_y = 1

        if axis == 1:
            rect_x = rect_x + box_size * index - of + rand_of_x + new_of_x
            rect_y = rect_y - of + rand_of_y + new_of_y
            weight = box_size + rand_of_box_size_x - new_of_x - random.randint(1, 2)
            height = box_size + rand_of_box_size_y - new_of_y - random.randint(1, 2)

        elif axis == 0:
            rect_x = rect_x - of + rand_of_x + new_of_x
            rect_y = rect_y + box_size * index - of + rand_of_y + new_of_y
            weight = box_size + rand_of_box_size_x - new_of_x - random.randint(1, 2)
            height = box_size + rand_of_box_size_y - new_of_y - random.randint(1, 2)

        stack.append((rect_x, rect_y,
                      weight, height, [char]))