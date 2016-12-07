from collections import namedtuple

from common import BaseInputParser, DataClass


class InputParser(BaseInputParser):
    @property
    def triangles(self):
        for line in self.lines:
            dimensions = line.split()
            yield Triangle(a=dimensions[0], b=dimensions[1], c=dimensions[2])

    @property
    def triple_columns(self):
        triplet = []
        for line_number, line in enumerate(self.lines):
            triplet.append(line.split())
            if triplet and len(triplet) == 3:
                yield triplet
                triplet = []


    @property
    def column_triangles(self):
        for triplet in self.triple_columns:
            triangles = [
                Triangle(a=triplet[0][0], b=triplet[1][0], c=triplet[2][0]),
                Triangle(a=triplet[0][1], b=triplet[1][1], c=triplet[2][1]),
                Triangle(a=triplet[0][2], b=triplet[1][2], c=triplet[2][2]),
            ]
            for triangle in triangles:
                yield triangle


class Triangle(DataClass):
    def __init__(self, a, b, c):
        super().__init__(a=int(a), b=int(b), c=int(c))

    def is_valid(self):
        longest, middle, shortest = reversed(sorted(self.data))
        return (shortest + middle) > longest


def main():
    parser = InputParser()

    valid_triangles = 0
    for triangle in parser.triangles:
        if triangle.is_valid():
            valid_triangles += 1

    print("There are %s valid triangles on the walls" % valid_triangles)

    valid_triangles = 0
    for triangle in parser.column_triangles:
        if triangle.is_valid():
            valid_triangles += 1

    print("There are %s valid triangles in columns on the walls" % valid_triangles)


if __name__ == '__main__':
    main()
