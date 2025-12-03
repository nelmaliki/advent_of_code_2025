import dataclasses

from sympy.plotting.textplot import is_valid


@dataclasses.dataclass
class Range:
    start: int
    end: int


def pt1_solution(ranges: list[Range]) -> int:
    acc = 0
    for r in ranges:
        for x in range(r.start, r.end + 1):
            if not is_valid_pt2(x):
                acc += x
    return acc

#should get same answer as original pt 1
def is_valid_pt1_control(id: int) -> bool:
    as_str = str(id)
    str_len = len(as_str)
    if str_len % 2 == 1:
        return True
    window_size = int(str_len / 2)
    # evenly divisible check
    num_chunks = str_len / window_size
    if float(int(num_chunks)) == num_chunks:
        chunks = [as_str[chunk_num * window_size:(chunk_num + 1) * window_size] for chunk_num in
                  range(int(num_chunks))]
        if all(x == chunks[0] for x in chunks):
            return False
    return True


def is_valid_pt2(id: int) -> bool:
    as_str = str(id)
    str_len = len(as_str)
    for window_size in range(1, int(str_len / 2)+1):
        # evenly divisible check
        num_chunks = str_len / window_size
        if float(int(num_chunks)) == num_chunks:
            chunks = [as_str[chunk_num * window_size:(chunk_num + 1) * window_size] for chunk_num in
                      range(int(num_chunks))]
            if all(x == chunks[0] for x in chunks):
                return False
    return True


def create_range(range: str) -> Range:
    start = int(range.split("-")[0])
    end = int(range.split("-")[1])
    return Range(start, end)


def read_file() -> list[Range]:
    open_file = open("puzzle_input.txt", "r")
    read_instructions: list[Range] = [create_range(r) for r in open_file.readline().split(",")]
    return read_instructions


def main() -> None:
    ranges = read_file()
    print(f"Solution: {pt1_solution(ranges)}")


if __name__ == '__main__':
    main()
