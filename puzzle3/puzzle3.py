def pt1_solution(powerbanks: list[str]) -> int:
    acc = 0
    for powerbank in powerbanks:
        max_index = 0
        for index, cell in enumerate(powerbank[:-1]):
            if int(cell) > int(powerbank[max_index]):
                max_index = index
        second_max_index = max_index + 1
        for second_index, cell in enumerate(powerbank[second_max_index:]):
            if int(cell) > int(powerbank[second_max_index]):
                second_max_index = second_index + max_index + 1
        power = int(powerbank[max_index] + powerbank[second_max_index])
        acc += power
    return acc


def pt2_solution(powerbanks: list[str]) -> int:
    acc = 0
    for powerbank in powerbanks:
        num_cells = 12
        cell_indices: list[int] = []
        left_boundary = 0
        for x in range(num_cells):
            right_boundary = num_cells-1-x
            window = powerbank[left_boundary:-right_boundary] if right_boundary > 0 else powerbank[left_boundary:]
            index = index_of_max_digit(window)
            cell_indices.append(index + left_boundary)
            left_boundary = index + left_boundary + 1

        power = int("".join([powerbank[ind] for ind in cell_indices]))
        acc += power
    return acc


def index_of_max_digit(powerbank: str) -> int:
    max_index = 0
    for index, cell in enumerate(powerbank):
        if int(cell) > int(powerbank[max_index]):
            max_index = index
    return max_index


def read_file() -> list[str]:
    open_file = open("puzzle_input.txt", "r")
    read_instructions: list[str] = [r.strip() for r in open_file.readlines()]
    return read_instructions


def main() -> None:
    ranges = read_file()
    print(f"Solution pt 1: {pt1_solution(ranges)}")
    print(f"Solution pt 2: {pt2_solution(ranges)}")


if __name__ == '__main__':
    main()
