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

    def _parse_instruction_to_coordinate(self, old_position, instruction, length):
        length = int(length)
        x = int(old_position.x)
        y = int(old_position.y)

        if instruction.direction is Direction.North:
            current_position = Coordinate(x=x, y=y + length)
        elif instruction.direction is Direction.East:
            current_position = Coordinate(x=x + length, y=y)
        elif instruction.direction is Direction.South:
            current_position = Coordinate(x=x, y=y - length)
        else:  # direction is West
            current_position = Coordinate(x=x - length, y=y)
        return current_position

    def get_final_position(self):
        current_position = Coordinate(x=0, y=0)
        for instruction in self._instructions():
                current_position = self._parse_instruction_to_coordinate(
                    current_position, instruction, instruction.length
                )

        return current_position

    def _get_all_locations(self):
        current_position = Coordinate(x=0, y=0)
        for instruction in self._instructions():
                length = int(instruction.length)
                while length > 0:
                    current_position = self._parse_instruction_to_coordinate(current_position, instruction, 1)
                    yield current_position
                    length -= 1

    def get_first_position_visited_twice(self):
        grid = {Coordinate(0, 0): 1}

        for position in self._get_all_locations():
            grid[position] = grid.get(position, 0) + 1
            if grid[position] >= 2:
                return position

        return None


def main():
    input_parser = InputParser("input.txt")
    final_destination = input_parser.get_final_position()
    print("End is {blocks_away} blocks away".format(blocks_away=final_destination.x+final_destination.y))

    position_visited_twice = input_parser.get_first_position_visited_twice()
    print("Real position is {blocks_away} blocks away".format(
        blocks_away=position_visited_twice.x+position_visited_twice.y)
    )


if __name__ == '__main__':
    main()
