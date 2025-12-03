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

def read_file() -> list[str]:
    open_file = open("puzzle_input.txt", "r")
    read_instructions: list[str] = [r.strip() for r in open_file.readlines()]
    return read_instructions


def main() -> None:
    ranges = read_file()
    print(f"Solution: {pt1_solution(ranges)}")

if __name__ == '__main__':
    main()
