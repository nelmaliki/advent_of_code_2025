import dataclasses
from math import floor


@dataclasses.dataclass
class Instruction:
    move_right: bool  # else left
    value: int


def solution_pt1(input: list[Instruction]) -> int:
    # starts at 50 so insert an R50 instruction here
    input.insert(0, Instruction(True, 50))
    zero_counts = 0
    running_total = 0
    for instruction in input:
        if instruction.move_right:
            running_total += instruction.value
        else:
            running_total -= instruction.value
        if (running_total % 100) == 0:
            zero_counts += 1
    return zero_counts

def solution_pt2(input: list[Instruction]) -> int:
    # starts at 50 so insert an R50 instruction here
    input.insert(0, Instruction(True, 50))
    zero_counts = 0
    running_total = 0
    for instruction in input:
        change = (instruction.value % 100 if instruction.move_right else (instruction.value  % 100) * -1)
        zero_counts += int(instruction.value / 100)
        zero_counts += 1 if running_total != 0 and (running_total + change >= 100 or running_total + change <= 0) else 0
        running_total = (running_total + change) % 100
    return zero_counts

# This solution sucks but can use to verify better solutions
def solution_pt2_control(input: list[Instruction]) -> int:
    # starts at 50 so insert an R50 instruction here
    input.insert(0, Instruction(True, 50))
    zero_counts = 0
    running_total = 0
    for instruction in input:
        tmp_total = running_total
        for i in range(instruction.value):
            if instruction.move_right:
                tmp_total += 1
            else:
                tmp_total -= 1
            if (tmp_total % 100) == 0:
                zero_counts += 1
        running_total = tmp_total
    return zero_counts


def read_file() -> list[Instruction]:
    # puzzle1_input
    open_file = open("puzzle1_input.txt", "r")
    read_instructions: list[Instruction] = [create_instruction(line) for line in open_file.readlines()]
    return read_instructions


def create_instruction(line: str) -> Instruction:
    if line[0] == "R":
        mv_right = True
    elif line[0] == "L":
        mv_right = False
    else:
        raise Exception(f"Invalid instruction: {line}")
    return Instruction(mv_right, int(line[1:]))


def main() -> None:
    instructions = read_file()
    for i in range(len(instructions)):
        control_answer = solution_pt2_control(instructions[:i])
        test_answer = solution_pt2(instructions[:i])
        if control_answer != test_answer:
            print(f"At line number {i}. Control: {control_answer} != {test_answer}. Halting")
            return
    print(f"Final Answer Control Solution: {solution_pt2_control([i for i in instructions])}")
    print(f"Final Answer Test Solution: {solution_pt2([i for i in instructions])}")


if __name__ == '__main__':
    main()
