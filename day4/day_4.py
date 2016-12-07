import re
import string
from collections import namedtuple, Counter
from operator import itemgetter

from common import BaseInputParser, DataClass


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

    @property
    def valid_rooms(self):
        for room in self.rooms:
            if RoomValidator.is_valid(room):
                yield room


class Room(DataClass):
    def __init__(self, encrypted_name, sector_id, checksum):
        super().__init__(
            encrypted_name=encrypted_name,
            sector_id=int(sector_id),
            checksum=checksum
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


class RoomDecrypter:
    @staticmethod
    def _get_next_letter(character, rotation_number):
       index = string.ascii_lowercase.index(character)
       return string.ascii_lowercase[(index + rotation_number) % len(string.ascii_lowercase)]

    @staticmethod
    def decrypt(room: Room):
        name = "".join(room.data.encrypted_name)
        return "".join([RoomDecrypter._get_next_letter(character, room.data.sector_id) for character in name])


def main():
    parser = InputParser()

    id_sum = 0
    for room in parser.rooms:
        if RoomValidator.is_valid(room):
            id_sum += room.data.sector_id

    print("Id sum is %s" % id_sum)

    for room in parser.valid_rooms:
        if "north" in RoomDecrypter.decrypt(room):
            print("Sector ID of North Pole Objects are in room '%s' in sector %s" %
                  (RoomDecrypter.decrypt(room), room.data.sector_id))

if __name__ == '__main__':
    main()
