from utils import profile_and_print_result, get_line_as_string_content


def hash_algorithm(value: str) -> int:
    current_hash_value = 0
    for c in value:
        current_hash_value = ((current_hash_value + ord(c)) * 17) % 256
    return current_hash_value


def read_input() -> [str]:
    return get_line_as_string_content("input1_day15").split(",")


def day15_part1() -> int:
    return sum(hash_algorithm(v) for v in read_input())


def get_same_label_pos(labels_and_focal_lengths: [str], label: str) -> int:
    for pos in range(len(labels_and_focal_lengths)):
        if labels_and_focal_lengths[pos].startswith(label):
            return pos
    return -1


def parser_sequence(op_character: str, value: str) -> (str, str):
    label_and_focal_length = value.split(op_character)
    label = label_and_focal_length[0]
    focal_length = label_and_focal_length[1]
    return label, focal_length, value.replace(op_character, " ")


def perform_hash_map(sequence: [str]) -> [[]]:
    boxes = [[] for _ in range(256)]
    for v in sequence:
        op_character = "=" if "=" in v else "-"
        label, focal_length, final_value = parser_sequence(op_character, v)
        box_pos = hash_algorithm(label)
        target_box = boxes[box_pos]
        old_label_pos = get_same_label_pos(target_box, label)

        if old_label_pos != -1:
            old_label = target_box[old_label_pos]
            target_box.remove(old_label)
            if op_character == "=":
                target_box.insert(old_label_pos, final_value)
        elif op_character == "=":
            target_box.append(final_value)
    return boxes


def get_box_focus(box: [str], box_pos: int) -> int:
    def focus(len_pos):
        return int(box[len_pos][-1])

    return sum(box_pos * (l_pos + 1) * focus(l_pos) for l_pos in range(len(box)))


def day15_part2() -> int:
    boxes = perform_hash_map(read_input())
    return sum(get_box_focus(boxes[pos], pos + 1) for pos in range(len(boxes)))


profile_and_print_result(day15_part1)
profile_and_print_result(day15_part2)

# Result => 506869. Time taken 0.0069539546966552734 (s)
# Result => 271384. Time taken 0.012644052505493164 (s)
