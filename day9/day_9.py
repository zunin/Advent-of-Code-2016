import re

from common import *


class InputParser(BaseInputParser):
    @property
    def characters(self):
        for line in self.lines:
            for character in line:
                yield character


Marker = namedtuple("Marker", ["characters", "repeat"])


class Decompressor:
    input = ""
    is_parsing_marker = False
    marker = None
    marker_buffer = ""
    input_buffer = ""

    def process(self, characters):
        for character in characters:
            if not self.marker and not self.is_parsing_marker and character == "(":
                self.marker_buffer = ""
                self.is_parsing_marker = True
            elif self.is_parsing_marker and character == ")":
                self.is_parsing_marker = False
                marker_input = self.marker_buffer.split("x")
                self.marker = Marker(characters=int(marker_input[0]), repeat=int(marker_input[1]))
            elif self.is_parsing_marker:
                self.marker_buffer += character
            else:
                if self.marker:
                    self.input_buffer += character
                    self.marker = Marker(characters=self.marker.characters - 1, repeat=self.marker.repeat)
                    if self.marker.characters == 0:
                        self.input += self.marker.repeat * self.input_buffer
                        self.input_buffer = ""
                        self.marker = None
                else:
                    self.input += character

    def get_decompressed_input(self):
        return self.input.strip()


class DecompressorV2:
    regex = "(\(\d+x\d+\))"
    input = ""

    def process(self, characters):
        self.input = "".join(characters)

        while re.search(self.regex, self.input):
            #print(len(re.findall(self.regex, self.input)))
            match = re.search(self.regex, self.input)
            characters, repeat = match.group()[1:-1].split("x")
            marker = Marker(characters=int(characters), repeat=int(repeat))

            start_pos = match.span()[0]
            text = self.input[start_pos:start_pos+marker.characters+len(match.group())]
            replace_text = self.input[start_pos+len(match.group()):start_pos+marker.characters+len(match.group())]
            #print("replace with\n\t%s\n\t%s" % (text, replace_text))
            self.input = self.input.replace(
                text,
                replace_text * marker.repeat
            )

        return self.input

    def get_decompressed_input(self):
        return self.input.strip()


def main():
    parser = InputParser()
    decompressor = Decompressor()

    decompressor.process(parser.characters)

    print("Decompressed input is %s characters long." % len(decompressor.get_decompressed_input()))

    decompressorv2 = DecompressorV2()

    print(len(decompressorv2.process(parser.characters)))
    print(decompressorv2.process(parser.characters))



if __name__ == '__main__':
    main()
