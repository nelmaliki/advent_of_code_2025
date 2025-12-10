import dataclasses
import enum
from typing import Tuple, Union


@dataclasses.dataclass
class Location:
    x: int
    y: int


# brute force because I'm tired
def pt1_solution(locations: list[Location]) -> int:
    squares: list[Tuple[Location, Location, int]] = []
    for location in locations:
        for location2 in locations:
            area = (max(location.x, location2.x) - min(location.x, location2.x) + 1) \
                   * (max(location.y, location2.y) - min(location.y, location2.y) + 1)
            squares.append((location, location2, area))
    s = sorted(squares, key=lambda square: square[2], reverse=True)
    return s[0][2]


class Rectangle():
    def __init__(self, corner_a: Location, corner_b: Location):
        right = max(corner_a.x, corner_b.x)
        left = min(corner_a.x, corner_b.x)
        bottom = max(corner_a.y, corner_b.y)
        top = min(corner_a.y, corner_b.y)

        self.top_left = Location(left, top)
        self.top_right = Location(right, top)
        self.bottom_left = Location(left, bottom)
        self.bottom_right = Location(right, bottom)

    def contains(self, location: Location) -> bool:
        return self.top_left.x < location.x < self.top_right.x and self.top_left.y < location.y < self.top_right.y

    def area(self) -> int:
        width = self.bottom_right.x - self.top_left.x + 1
        height = self.bottom_right.y - self.top_left.y + 1
        return width * height

    def corners(self) -> list[Location]:
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]


class RelativeDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


@dataclasses.dataclass
class Line:
    start: Location
    end: Location

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def contains(self, location: Location) -> bool:
        if self.is_vertical():
            return (location.x == self.end.x and
                    (self.start.y <= location.y <= self.end.y or self.end.y <= location.y <= self.start.y))
        elif self.is_horizontal():
            return (location.y == self.end.y and
                    (self.start.x <= location.x <= self.end.x or self.end.x <= location.x <= self.start.x))
        else:
            raise Exception("Error: Diagonal lines are not supported.")

    def relative_direction(self, location: Location) -> Union[RelativeDirection, None]:
        if self.is_vertical():
            if self.start.y <= location.y <= self.end.y or self.end.y <= location.y <= self.start.y:
                if location.x > self.end.x:
                    return RelativeDirection.RIGHT
                elif location.x < self.end.x:
                    return RelativeDirection.LEFT
                return None
            elif self.start.x == location.x:
                if location.y > self.end.y and location.y > self.start.y:
                    return RelativeDirection.UP
                elif location.y < self.end.y and location.y < self.start.y:
                    return RelativeDirection.DOWN
            else:
                return None
        elif self.is_horizontal():
            if self.start.x <= location.x <= self.end.x or self.end.x <= location.x <= self.start.x:
                if location.y > self.end.y:
                    return RelativeDirection.UP
                elif location.y < self.end.y:
                    return RelativeDirection.DOWN
                return None
            elif self.start.y == location.y:
                if location.x > self.end.x and location.x > self.start.x:
                    return RelativeDirection.RIGHT
                elif location.x < self.end.x and location.x < self.start.y:
                    return RelativeDirection.LEFT
            else:
                return None
        else:
            raise Exception("Error: Diagonal lines are not supported.")


@dataclasses.dataclass
class Shape:
    lines: list[Line]

    def contains(self, location: Location) -> bool:
        relative_directions: dict[RelativeDirection, int] = {RelativeDirection.UP: 0, RelativeDirection.DOWN: 0,
                                                             RelativeDirection.LEFT: 0, RelativeDirection.RIGHT: 0}

        for line in self.lines:
            if line.contains(location):
                return True
            relative_direction = line.relative_direction(location)
            if relative_direction is not None:
                relative_directions[relative_direction] += 1

        #Ray-Casting Algorithm: Odd number of intersections on all sides mean that the point is inside of the shape
        #Even numbe
        return ((relative_directions[RelativeDirection.LEFT] % 2) == 1
                and (relative_directions[RelativeDirection.RIGHT] % 2) == 1
                and (relative_directions[RelativeDirection.DOWN] % 2) == 1
                and (relative_directions[RelativeDirection.UP] % 2) == 1)


def pt2_solution(locations: list[Location]) -> int:
    squares: list[Tuple[Location, Location, int]] = []
    valid_shape = create_valid_shape(locations)
    for i, location in enumerate(locations[:-1]):
        for location2 in locations[i + 1:]:
            rect = Rectangle(location, location2)
            if is_valid_rect(rect, valid_shape):
                squares.append((location, location2, rect.area()))
    s = sorted(squares, key=lambda square: square[2], reverse=True)
    return s[0][2]


def is_valid_rect(rect: Rectangle, valid_shape: Shape) -> bool:
    for corner in rect.corners():
        if not valid_shape.contains(corner):
            return False
    return True


# Computes valid area and breaks it down into list of squares
def create_valid_shape(locations: list[Location]) -> Shape:
    lines: list[Line] = []
    for i, location in enumerate(locations):
        next_location = locations[i + 1] if i + 1 < len(locations) else locations[0]
        lines.append(Line(location, next_location))
    return Shape(lines)


def read_file() -> list[Location]:
    open_file = open("puzzle_input.txt", "r")
    locations: list[Location] = []
    for line in open_file.readlines():
        locations.append(Location(int(line.split(",")[0]), int(line.split(",")[1])))
    return locations


def main() -> None:
    _l = read_file()
    print(f"Solution: {pt1_solution(_l)}")
    print(f"Solution 2: {pt2_solution(_l)}")


if __name__ == '__main__':
    main()
