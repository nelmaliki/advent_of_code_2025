import dataclasses
import math
import re


@dataclasses.dataclass()
class Equation:
    operator: str
    operands: list[int]

    def solve(self) -> int:
        if self.operator == "+":
            return sum(self.operands)
        if self.operator == "*":
            return math.prod(self.operands)
        else:
            raise ValueError("Operand must be either + or *")


def read_file() -> list[Equation]:
    open_file = open("puzzle_input.txt", "r")
    equations: list[Equation] = []
    num_equations = len(re.split(" +", open_file.readline().strip()))
    open_file.seek(0)
    for i in range(num_equations):
        equations.append(Equation("", []))

    for line in open_file.readlines():
        for i, v in enumerate(re.split(" +", line.strip())):
            if v == '+' or v == '*':
                equations[i].operator = v
            else:
                equations[i].operands.append(int(v))

    return equations


def read_file_2() -> list[Equation]:
    open_file = open("puzzle_input.txt", "r")
    operators_per_equation = 4
    equations: list[Equation] = []
    #Index is line_number, value is num of characters in the line
    chars_in_line = [len(l) for l in open_file.readlines()]
    # seek to 5th line
    open_file.seek(sum([chars_in_line[i] for i in range(operators_per_equation)]))
    #index of operand in it's line, which is always the index of the first digit of the equation on all lines
    operand_ind: list[int] = []
    for op_group in re.finditer("[*+]", open_file.readline().strip()):
        equations.append(Equation(op_group.group(), []))
        operand_ind.append(op_group.start())

    for op_col_index, op_col_num in enumerate(operand_ind):
        end_col = operand_ind[op_col_index + 1]-1 if op_col_index < len(operand_ind)-1 else chars_in_line[-1]
        operands: list[int] = []
        for tmp_col in range(op_col_num, end_col):
            operand_as_str = ""
            for row in range(operators_per_equation):
                seek_pos = sum([chars_in_line[i] for i in range(row)]) + tmp_col
                open_file.seek(seek_pos)
                operand_as_str += open_file.read(1)
            operands.append(int(operand_as_str.strip()))
        equations[op_col_index].operands = operands
    return equations


def main() -> None:
    _equations = read_file()
    print(f"Solution pt1: {sum([x.solve() for x in _equations])}")
    _equations2 = read_file_2()
    print(f"Solution pt2: {sum([x.solve() for x in _equations2])}")


if __name__ == '__main__':
    main()
