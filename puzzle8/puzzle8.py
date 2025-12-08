import dataclasses
import math
from typing import Tuple


@dataclasses.dataclass(frozen=True)
class Location:
    x: int
    y: int
    z: int


class JunctionGraph:
    def __init__(self, junctions: list[Location]):
        self.graph: dict[Location, list[Location]] = {}
        for j in junctions:
            self.graph[j] = []

    def add_connection(self, loc1: Location, loc2: Location) -> None:
        self.graph[loc1].append(loc2)
        self.graph[loc2].append(loc1)

    def compute_subgraph_size(self, loc1: Location, cycle_detection: set[Location]) -> int:
        count = 1
        cycle_detection.add(loc1)
        for neighbor in self.graph[loc1]:
            if neighbor not in cycle_detection:
                count += self.compute_subgraph_size(neighbor, cycle_detection)
        return count

    def is_location_in_subgraph(self, start: Location, test: Location, cycle_detection: set[Location]) -> bool:
        if start == test:
            return True
        cycle_detection.add(start)
        for neighbor in self.graph[start]:
            if neighbor not in cycle_detection:
                if self.is_location_in_subgraph(neighbor, test, cycle_detection):
                    return True
        return False


def pt1_solution(junctions: list[Location]) -> int:
    adjacency_list: list[Tuple[Location, Location, float]] = []
    for i, loc in enumerate(junctions):
        for loc2 in junctions[i:]:
            if loc != loc2:
                distance = math.sqrt((loc.x - loc2.x) ** 2 + (loc.y - loc2.y) ** 2 + (loc.z - loc2.z) ** 2)
                adjacency_list.append((loc, loc2, distance))
    # sort on distance
    adjacency_list.sort(key=lambda adj: adj[2])
    graph = JunctionGraph(junctions)
    num_connections = 1000
    tmp = 0
    for adj in adjacency_list:
        if tmp < num_connections:  # and not graph.is_location_in_subgraph(adj[0], adj[1], set()):
            graph.add_connection(adj[0], adj[1])
            tmp += 1

    seen_so_far = set()
    sizes = []
    for loc in junctions:
        if loc not in seen_so_far:
            subgraph_size = graph.compute_subgraph_size(loc, seen_so_far)
            sizes.append(subgraph_size)
    sizes.sort(reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def pt2_solution(junctions: list[Location]) -> int:
    adjacency_list: list[Tuple[Location, Location, float]] = []
    for i, loc in enumerate(junctions):
        for loc2 in junctions[i:]:
            if loc != loc2:
                distance = math.sqrt((loc.x - loc2.x) ** 2 + (loc.y - loc2.y) ** 2 + (loc.z - loc2.z) ** 2)
                adjacency_list.append((loc, loc2, distance))
    # sort on distance
    adjacency_list.sort(key=lambda adj: adj[2])
    graph = JunctionGraph(junctions)

    for adj in adjacency_list:
        graph.add_connection(adj[0], adj[1])
        if len(all_compute_subgraph_sizes(graph, junctions)) == 1:
            return adj[0].x * adj[1].x
    return -1


def all_compute_subgraph_sizes(graph: JunctionGraph, junctions: list[Location]) -> list[int]:
    seen_so_far = set()
    sizes = []
    for loc in junctions:
        if loc not in seen_so_far:
            subgraph_size = graph.compute_subgraph_size(loc, seen_so_far)
            sizes.append(subgraph_size)
    sizes.sort(reverse=True)
    return sizes


def read_file() -> list[Location]:
    open_file = open("puzzle_input.txt", "r")
    junctions: list[Location] = []
    for line in open_file.readlines():
        digits = line.strip().split(",")
        junctions.append(Location(int(digits[0]), int(digits[1]), int(digits[2])))
    return junctions


def main() -> None:
    j = read_file()
    print(f"Solution: {pt1_solution(j)}")
    print(f"Solution: {pt2_solution(j)}")


if __name__ == '__main__':
    main()
