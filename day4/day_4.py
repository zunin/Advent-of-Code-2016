import re
from collections import namedtuple, Counter
from operator import itemgetter

from common import BaseInputParser


class InputParser(BaseInputParser):
    @property
    def rooms(self):
        for line in self.lines:
            raw_split = re.split("(\[.+\])", line.strip())
            dash_split = raw_split[0].split("-")

            yield Room(
                encrypted_name=dash_split[:-1],
                sector_id=dash_split[-1],
                checksum=raw_split[1][1:-1]
            )


class Room:
    RoomData = namedtuple("RoomData", "encrypted_name sector_id checksum")

    def __init__(self, encrypted_name, sector_id, checksum):
        self.data = self.RoomData(
            encrypted_name=encrypted_name,
            sector_id=int(sector_id),
            checksum=checksum
        )

    def __repr__(self):
        return self.data.__repr__().replace(
            self.RoomData.__name__,
            self.__class__.__name__
        )


class RoomValidator:
    @staticmethod
    def is_valid(room: Room):
        c = Counter(''.join(room.data.encrypted_name))

        counted_items = c.items()
        alphabetical = sorted(counted_items, key=itemgetter(0))
        frequency = sorted(alphabetical, key=itemgetter(1), reverse=True)

        calculated_checksum = "".join([letter[0] for letter in frequency[:5]])
        return calculated_checksum == room.data.checksum


def main():
    parser = InputParser()

    id_sum = 0
    for room in parser.rooms:
        if RoomValidator.is_valid(room):
            id_sum += room.data.sector_id

    print("Id sum is %s" % id_sum)

if __name__ == '__main__':
    main()
