from collections import namedtuple
from enum import Enum


class Direction(Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


class InputParser:
    def __init__(self, file_name="input.txt"):
        self.file_name = file_name

    @property
    def lines(self):
        with open(self.file_name, "rt") as input_file:
            for line in input_file:
                yield line

    @property
    def instruction_lists(self):
        for line in self.lines:
            yield [Direction(character) for character in line.split("\n")[0]]


class Coordinate:
    def __init__(self, x, y, x_max=2, y_max=2, x_min=0, y_min=0):
        self.x = min([max([x, x_min]), x_max])
        self.y = min([max([y, y_min]), y_max])

    def __add__(self, other: Direction):
        if other is Direction.Up:
            return Coordinate(x=self.x, y=self.y-1)
        elif other is Direction.Down:
            return Coordinate(x=self.x, y=self.y+1)
        elif other is Direction.Left:
            return Coordinate(x=self.x-1, y=self.y)
        else:  # Right
            return Coordinate(x=self.x+1, y=self.y)


class Keypad:
    keys = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    def __getitem__(self, item: Coordinate):
        return self.keys[item.y][item.x]


class KeypadInstructionTracker:
    keypad = Keypad()
    position = Coordinate(1, 1)

    def get_position_after_position(self, instructions):

        for instruction in instructions:
            self.position = self.position + instruction

        return self.keypad[self.position]


def main():
    input_parser = InputParser()
    tracker = KeypadInstructionTracker()

    print([tracker.get_position_after_position(instructions) for instructions in input_parser.instruction_lists])

if __name__ == '__main__':
    main()