import re
from collections import namedtuple
from enum import IntEnum


class Direction(IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3


Coordinate = namedtuple('Coordinate', 'x y')

Instruction = namedtuple('Instruction', 'direction length')

class InputParser:

    def __init__(self, file_name):
        self.file_name = file_name

    def _instructions(self):
        with open(self.file_name, "rt") as input_file:
            current_direction = Direction.North
            for line in input_file:
                raw_instructions = [instruction.strip() for instruction in line.split(",")]

                for raw_instruction in raw_instructions:
                    raw_direction = re.split("(R|L)", raw_instruction)


                    value_addition = 1 if raw_direction[1] is "R" else -1

                    new_direction = Direction((current_direction.value + value_addition) % 4)
                    current_direction = new_direction


                    yield Instruction(
                        direction= new_direction,
                        length=raw_direction[2]
                    )

    def parse(self):
        current_position = Coordinate(x=0, y=0)
        for instrution in self._instructions():
            length = int(instrution.length)
            x = int(current_position.x)
            y = int(current_position.y)

            if instrution.direction is Direction.North:
                current_position = Coordinate(x=x, y=y + length)
            elif instrution.direction is Direction.East:
                current_position = Coordinate(x=x + length, y=y)
            elif instrution.direction is Direction.South:
                current_position = Coordinate(x=x, y=y - length)
            else: # direction is West
                current_position = Coordinate(x=x - length, y=y)

        return current_position


def main():
    final_destionation = InputParser("input.txt").parse()
    print("End is {blocks_away} blocks away".format(blocks_away=final_destionation.x+final_destionation.y))

if  __name__ =='__main__':
    main()
