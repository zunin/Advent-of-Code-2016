import re
from collections import namedtuple

from common import BaseInputParser


class InputParser(BaseInputParser):
    @property
    def ip_addresses(self):
        for line in self.lines:
            raw_split = re.split("(\[[a-z]+\])", line.strip())

            hypernets = []
            texts = []
            for line in raw_split:
                    if line.startswith("[") and line.endswith("]"):
                        hypernets.append(line[1:-1])
                    else:
                        texts.append(line)

            yield IPAddress(texts=texts, hypernets=hypernets)


class IPAddress:
    model = namedtuple("IPAddress", ["supernets", "hypernets"])

    def __init__(self, texts, hypernets):
        self.data = self.model(texts=texts, hypernets=hypernets)

    @property
    def supernets(self):
        return self.data.supernets

    @property
    def hypernets(self):
        return self.data.hypernets

    def __repr__(self):
        return self.data.__repr__().replace(
            self.model.__name__,
            self.__class__.__name__
        )


class Validator:
    @staticmethod
    def has_abba(text):
        for index, character in enumerate(text[3:]):
            first_pair = (text[index], text[index+1])
            second_pair = (text[index+2], text[index+3])

            if first_pair == tuple(reversed(second_pair)) and first_pair != second_pair:
                return True
        return False

    @staticmethod
    def validate_with_abba(ip_address: IPAddress):
        print(ip_address)
        for hypernet in ip_address.hypernets:
            if Validator.has_abba(hypernet):
                return False

        for supernet in ip_address.supernets:
            if Validator.has_abba(supernet):
                return True

        return False


def main():
    parser = InputParser()

    tls_ip_addresses = 0
    for address in parser.ip_addresses:
        if Validator.validate_with_abba(address):
            tls_ip_addresses += 1

    print("There are %s ip addresses that support TLS according to ABBA validation" % tls_ip_addresses)


if __name__ == '__main__':
    main()
