import dataclasses

@dataclasses.dataclass
class Instruction:
    move_right: bool #else left
    value: int

def solution(input: list[Instruction]) -> int:
    #starts at 50 so insert an R50 instruction here
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

def read_file() -> list[Instruction]:
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

if __name__ == '__main__':
    instructions = read_file()
    x = solution(instructions)
    print(x)

