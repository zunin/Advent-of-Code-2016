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
    InnerCoordinate = namedtuple("InnerCoordinate", "x y")

    def __init__(self, x, y):
        self.tuple = self.InnerCoordinate(x=x, y=y)

    def limit(self, x_max=2, y_max=2, x_min=0, y_min=0):
        x = min([max([self.tuple.x, x_min]), x_max])
        y = min([max([self.tuple.y, y_min]), y_max])
        self.tuple = self.InnerCoordinate(x=x, y=y)

    @property
    def x(self):
        return self.tuple.x

    @property
    def y(self):
        return self.tuple.y

    def __add__(self, other: Direction):
        if other is Direction.Up:
            return Coordinate(x=self.x, y=self.y-1)
        elif other is Direction.Down:
            return Coordinate(x=self.x, y=self.y+1)
        elif other is Direction.Left:
            return Coordinate(x=self.x-1, y=self.y)
        else:  # Right
            return Coordinate(x=self.x+1, y=self.y)

    def __repr__(self):
        return "%s(x=%s, y=%s)" % (self.__class__.__name__, self.x, self.y)

    def __eq__(self, other):
        return self.tuple.__eq__(other.tuple)

    def __lt__(self, other):
        return self.tuple.__lt__(other.tuple)

    def __hash__(self):
        return self.tuple.__hash__()

class Keypad:
    keys = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    def __getitem__(self, item: Coordinate):
        return self.keys[item.y][item.x]


class DiamondKeypad:
    keys = {
        Coordinate(x=2, y=0): 1,
        Coordinate(x=1, y=1): 2,
        Coordinate(x=2, y=1): 3,
        Coordinate(x=3, y=1): 4,
        Coordinate(x=0, y=2): 5,
        Coordinate(x=1, y=2): 6,
        Coordinate(x=2, y=2): 7,
        Coordinate(x=3, y=2): 8,
        Coordinate(x=4, y=2): 9,
        Coordinate(x=1, y=3): "A",
        Coordinate(x=2, y=3): "B",
        Coordinate(x=3, y=3): "C",
        Coordinate(x=2, y=4): "D",
    }


class DiamondKeypadInstructionTracker:
    keypad = DiamondKeypad()
    position = Coordinate(x=0, y=2)

    def filter(self, **kwargs):
        coordinates = self.keypad.keys
        for kwarg in kwargs:
            coordinates = {coordinate for coordinate in coordinates if coordinate.__getattribute__(kwarg) == kwargs[kwarg]}

        return coordinates

    def get_position_after_instructions(self, instructions):
        for instruction in instructions:
            next_position = self.position + instruction
            if self.keypad.keys.get(next_position):
                self.position = next_position
        return self.keypad.keys.get(self.position)


class KeypadInstructionTracker:
    keypad = Keypad()
    position = Coordinate(1, 1)

    def get_position_after_instructions(self, instructions):

        for instruction in instructions:
            self.position = self.position + instruction
            self.position.limit()

        return self.keypad[self.position]


def main():
    input_parser = InputParser()
    tracker = KeypadInstructionTracker()

    part_1 = ""
    for instructions in input_parser.instruction_lists:
        part_1 += str(tracker.get_position_after_instructions(instructions))

    print("First code is '%s'" % part_1)

    diamond_tracker = DiamondKeypadInstructionTracker()

    part_2 = ""
    for instructions in input_parser.instruction_lists:
        part_2 += str(diamond_tracker.get_position_after_instructions(instructions))

    print("Second code is '%s'" % part_2)

if __name__ == '__main__':
    main()
