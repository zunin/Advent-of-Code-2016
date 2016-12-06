from collections import Counter

from common import BaseInputParser


class InputParser(BaseInputParser):
    @property
    def split_lines(self):
        for line in self.lines:
            yield [character for character in line.strip()]

    @property
    def columns(self):
        return zip(*self.split_lines)


class InputDecrypter:
    def get_most_common_letter(self, column):
        return Counter(''.join(column)).most_common(1)[0][0]

    def get_least_common_letter(self, column):
        return Counter(''.join(column)).most_common()[-1][0]

def main():
    parser = InputParser()
    decrypter = InputDecrypter()

    message = [decrypter.get_most_common_letter(column) for column in parser.columns]
    print("The message from Santa is '%s'" % "".join(message))

    message = [decrypter.get_least_common_letter(column) for column in parser.columns]
    print("The message with modified repetition code from Santa is '%s'" % "".join(message))

if __name__ == '__main__':
    main()
