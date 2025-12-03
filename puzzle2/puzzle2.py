import dataclasses

from sympy.plotting.textplot import is_valid


@dataclasses.dataclass
class Range:
    start: int
    end: int

def pt1_solution(ranges: list[Range]) -> int:
    acc = 0
    for r in ranges:
        for x in range(r.start, r.end+1):
            if not is_valid(x):
                acc += x
    return acc

    #return sum([sum([id for id in range(r.start, r.end+1) if not is_valid(id)]) for r in ranges])

def is_valid(id: int) -> bool:
    as_str = str(id)
    if len(as_str) % 2 == 1:
        return True
    else:
        return as_str[0:int(len(as_str)/2)] != as_str[int(len(as_str)/2):]

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