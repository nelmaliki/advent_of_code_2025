from typing import NamedTuple


class Coordinate(NamedTuple):
    row: int
    col: int


nearby_coordinate_offsets = [(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1)]


def pt1_solution(coordinates: set[Coordinate]) -> int:
    acc = 0
    for coordinate in coordinates:
        present_neighbors = 0
        for offset in nearby_coordinate_offsets:
            neighbor = Coordinate(coordinate.row + offset[0], coordinate.col + offset[1])
            present_neighbors += 1 if neighbor in coordinates else 0
        if present_neighbors < 4:
            acc += 1
    return acc

def pt2_solution(coordinates: set[Coordinate]) -> int:
    acc = 0
    tmp_acc = 1
    while tmp_acc > 0:
        tmp_acc = 0
        removed_coordinates = set()
        for coordinate in coordinates:
            present_neighbors = 0
            for offset in nearby_coordinate_offsets:
                neighbor = Coordinate(coordinate.row + offset[0], coordinate.col + offset[1])
                present_neighbors += 1 if neighbor in coordinates else 0
            if present_neighbors < 4:
                tmp_acc += 1
                removed_coordinates.add(coordinate)
        [coordinates.remove(c) for c in removed_coordinates]
        acc += tmp_acc
    return acc

def read_file() -> set[Coordinate]:
    open_file = open("puzzle_input.txt", "r")
    coordinates: set[Coordinate] = set()
    for line_num, line in enumerate(open_file.readlines()):
        for char_num, char in enumerate(line):
            if char == "@":
                coordinates.add(Coordinate(row=line_num, col=char_num))
    return coordinates


def main() -> None:
    coordinates = read_file()
    print(f"Solution pt 1: {pt1_solution(coordinates)}")
    print(f"Solution pt 2: {pt2_solution(coordinates)}")


if __name__ == '__main__':
    main()
