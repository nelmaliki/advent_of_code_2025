import dataclasses
import re
from typing import Union


@dataclasses.dataclass
class Location:
    x: int
    y: int


def pt1_solution(start: Location, splitters: list[Location]) -> int:
    beams_at_row: list[list[int]] = []
    max_rows = max([s.y for s in splitters])
    beams_at_row.insert(start.y, [start.x])
    num_splits = 0
    for row in range(start.y, max_rows + 1):
        next_step, num_splits_this_row = process_beam_step(beams_at_row[row], row, splitters)
        beams_at_row.append(next_step)
        num_splits += num_splits_this_row
    return num_splits


# Takes a list of beams at row_num and splitters and returns the list of beams at the next row
def process_beam_step(beams: list[int], row_num: int, splitters: list[Location]) -> tuple[list[int], int]:
    new_beams = set()
    num_splits = 0
    for beam in beams:
        split_occurred = False
        for split in splitters:
            if split.x == beam and split.y == row_num + 1:
                new_beams.add(split.x + 1)
                new_beams.add(split.x - 1)
                # break inner loop and proceed to next beam
                split_occurred = True
                num_splits += 1
                break
        if not split_occurred:
            # If no splitters found, beam continues down uninterrupted
            new_beams.add(beam)
    return [b for b in new_beams], num_splits


@dataclasses.dataclass(frozen=True)
class Beam:
    x_loc: int
    timelines: int


def pt2_solution(start: Location, splitters: list[Location]) -> int:
    beams_at_row: list[list[Beam]] = []
    max_rows = max([s.y for s in splitters])
    beams_at_row.insert(start.y, [Beam(start.x, 1)])
    num_splits = 0
    for row in range(start.y, max_rows + 1):
        next_step, num_splits_this_row = process_beam_step_2(beams_at_row[row], row, splitters)
        beams_at_row.append(next_step)
        num_splits += num_splits_this_row
    return sum([b.timelines for b in beams_at_row[max_rows + 1]])


# Takes a list of beams at row_num and splitters and returns the list of beams at the next row
def process_beam_step_2(beams: list[Beam], row_num: int, splitters: list[Location]) -> tuple[list[Beam], int]:
    new_beams: dict[int, int] = {}
    num_splits = 0
    for beam in beams:
        split_occurred = False
        for split in splitters:
            if split.x == beam.x_loc and split.y == row_num + 1:
                if split.x + 1 not in new_beams:
                    new_beams[split.x + 1] = beam.timelines
                else:
                    new_beams[split.x + 1] += beam.timelines
                if split.x - 1 not in new_beams:
                    new_beams[split.x - 1] = beam.timelines
                else:
                    new_beams[split.x - 1] += beam.timelines
                # break inner loop and proceed to next beam
                split_occurred = True
                num_splits += 1
                break
        if not split_occurred:
            # If no splitters found, beam continues down uninterrupted
            if beam.x_loc not in new_beams:
                new_beams[beam.x_loc] = beam.timelines
            else:
                new_beams[beam.x_loc] += beam.timelines
    return [Beam(loc, count) for loc, count in new_beams.items()], num_splits


def read_file() -> tuple[Location, list[Location]]:
    open_file = open("puzzle_input.txt", "r")
    splitters: list[Location] = []
    start: Union[Location, None] = None
    for line_num, line in enumerate(open_file.readlines()):
        s_loc = line.find("S")
        if s_loc >= 0:
            start = Location(s_loc, line_num)
        for op_group in re.finditer("\^", line.strip()):
            splitters.append(Location(op_group.start(), line_num))
    return start, splitters


def main() -> None:
    start, splitters = read_file()
    print(f"Solution: {pt1_solution(start, splitters)}")
    print(f"Solution pt 2: {pt2_solution(start, splitters)}")


if __name__ == '__main__':
    main()
