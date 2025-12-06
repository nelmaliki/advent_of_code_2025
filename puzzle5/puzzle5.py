import dataclasses
from typing import Union


@dataclasses.dataclass(frozen=True)
class Range:
    start: int
    end: int


def pt1_solution(valid_ids: list[Range], ids: list[int]) -> int:
    acc = 0
    for x in ids:
        for r in valid_ids:
            if is_id_in_range(x, r):
                acc += 1
                break
    return acc


def pt2_solution(valid_ids: list[Range]) -> int:
    #sorted(deduped_ids, key= lambda r: r.start)
    deduped_ids = deduplicate_ranges(valid_ids)
    num_valid_ids = 0
    for x in deduped_ids:
        num_valid_ids += (x.end - x.start) + 1
    return num_valid_ids

def deduplicate_ranges(ranges: list[Range]) -> list[Range]:
    tmp_ranges: list[Union[Range, None]] = sorted([r for r in ranges], key=lambda r: r.start)
    for i in range(len(tmp_ranges)-1):
        r1 = tmp_ranges[i]
        r2 = tmp_ranges[i+1]
        if r1.end >= r2.start:
            #327039828473999
            tmp_ranges[i+1] = Range(r1.start, max(r1.end, r2.end))
            tmp_ranges[i] = None
    return [r for r in tmp_ranges if r is not None]

# Takes ranges and combines them so that no number can be in two ranges
# Ex 1-5, 4-8, 3-9  -> 1-9
def deduplicate_ranges_2(ranges: list[Range]) -> list[Range]:
    tmp_ranges: list[Range] = [r for r in ranges]
    removed = set()
    for r1 in ranges:
        if r1 not in removed:
            min_window = r1.start
            max_window = r1.end
            to_remove = set()
            to_remove.add(r1)
            for r in tmp_ranges:
                if number_between_bounds(r.start, min_window, max_window):
                    if number_between_bounds(r.end, min_window, max_window):
                        to_remove.add(r)
                    else:
                        max_window = r.end
                        to_remove.add(r)
                elif number_between_bounds(r.end, min_window, max_window):
                    min_window = r.start
                    to_remove.add(r)
            for removable in to_remove:
                removed.add(removable)
                tmp_ranges.remove(removable)
            tmp_ranges.append(Range(min_window, max_window))
    return tmp_ranges

def number_between_bounds(id: int, start: int, end: int) -> bool:
    return start <= id <= end


def is_id_in_range(id: int, range: Range) -> bool:
    return number_between_bounds(id, range.start, range.end)


def create_range(range: str) -> Range:
    start = int(range.split("-")[0])
    end = int(range.split("-")[1])
    return Range(start, end)

def read_file() -> tuple[list[Range], list[int]]:
    open_file = open("puzzle_input.txt", "r")
    ranges: list[Range] = []
    ids: list[int] = []
    processing_ranges = True
    for line in open_file.readlines():
        if line == "\n":
            processing_ranges = False
            continue
        if processing_ranges:
            ranges += [create_range(line.strip())]
        else:
            ids += [int(line.strip())]
    return ranges, ids


def main() -> None:
    valid_ids, ids = read_file()
    print(f"Solution: {pt1_solution(valid_ids, ids)}")
    print(f"Solution 2: {pt2_solution(valid_ids)}")


if __name__ == '__main__':
    main()
