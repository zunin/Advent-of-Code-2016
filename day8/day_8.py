from collections import Counter

from common import *


RectCmd = namedtuple("RectCmd", ["a", "b"])
RotateCmd = namedtuple("RotateCmd", ["axis", "index", "length"])
Coordinate = namedtuple("Coordinate", ["x", "y"])


class Screen:
    def __init__(self, height=6, length=50):
        self.height = height
        self.length = length
        self.data = {}

    def __getitem__(self, item: Coordinate):
        x = item.x % self.length
        y = item.y % self.height
        return self.data.get(Coordinate(x=x, y=y), ".")

    def __setitem__(self, key: Coordinate, value: str):
        x = key.x % self.length
        y = key.y % self.height
        self.data[Coordinate(x=x, y=y)] = value

    def __repr__(self):
        lines = []
        for y in range(0, self.height):
            line = []
            for x in range(0, self.length):
                line.append(self[Coordinate(x=x, y=y)])
            lines.append("".join(line))

        return "\n".join(lines)


class ParseError(RuntimeError):
    pass


class InputParser(BaseInputParser):
    @property
    def commands(self):
        for line in self.lines:
            split_line = line.split()
            command = split_line[0]

            if command == "rect":
                a, b = split_line[1].split("x")
                yield RectCmd(a=int(a), b=int(b))
            elif command == "rotate":
                yield RotateCmd(axis=split_line[1], index=split_line[2], length=split_line[4])
            else:
                raise ParseError("Command not recognized: %s" % command)


class CommandScreenEncoder:
    def __init__(self, screen: Screen):
        self.screen = screen

    def _handle_rect(self, command: RectCmd):
        for x in range(0, command.a):
            for y in range(0, command.b):
                self.screen[Coordinate(x=x, y=y)] = "#"

    def _handle_rotate(self, command: RotateCmd):
        rotation = {
            "x": range(0, self.screen.length),
            "y": range(0, self.screen.height),
        }

        axis, point = command.index.split("=")
        rotation[axis] = range(int(point), int(point)+1)

        old_screen = Screen(height=self.screen.height, length=self.screen.length)
        old_screen.data = dict(self.screen.data)

        delta_x = int(command.length) if axis == "y" else 0
        delta_y = int(command.length) if axis == "x" else 0

        axis_coordinates = [Coordinate(x=x, y=y) for x in rotation["x"] for y in rotation["y"]]
        new_coordinates = [
            Coordinate(
                x=(old_coordinate.x + delta_x) % self.screen.length,
                y=(old_coordinate.y + delta_y) % self.screen.height
            )
            for old_coordinate in axis_coordinates
        ]

        for old_coordinate, new_coordinate in zip(axis_coordinates, new_coordinates):
            self.screen[new_coordinate] = old_screen[old_coordinate]

    def parse_command(self, command):
        if isinstance(command, RectCmd):
            self._handle_rect(command)
        else:
            self._handle_rotate(command)

    def get_lit_pixels(self):
        c = Counter(self.screen.data.values())
        return c.get("#")



def main():
    parser = InputParser()
    encoder = CommandScreenEncoder(Screen())

    for command in parser.commands:
        encoder.parse_command(command)
        #print(command)

    print("There would be %s lit pixels on the display" % encoder.get_lit_pixels())

    print("The display shows\n%s" % encoder.screen)


if __name__ == '__main__':
    main()
