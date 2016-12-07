import re
from collections import namedtuple

from common import BaseInputParser, DataClass


class InputParser(BaseInputParser):
    @property
    def ip_addresses(self):
        for line in self.lines:
            raw_split = re.split("(\[[a-z]+\])", line.strip())

            hypernets = []
            supernets = []
            for line in raw_split:
                    if line.startswith("[") and line.endswith("]"):
                        hypernets.append(line[1:-1])
                    else:
                        supernets.append(line)

            yield IPAddress(supernets=supernets, hypernets=hypernets)


class IPAddress(DataClass):
    def __init__(self, supernets, hypernets):
        super().__init__(supernets=supernets, hypernets=hypernets)


class Validator:
    @staticmethod
    def has_abba(text):
        for index, _ in enumerate(text[3:]):
            first_pair = (text[index], text[index+1])
            second_pair = (text[index+2], text[index+3])

            if first_pair == tuple(reversed(second_pair)) and first_pair != second_pair:
                return True
        return False


    @staticmethod
    def get_abas(text: str):
        abas = []
        for index, _ in enumerate(text[2:]):
            if text[index] == text[index+2] and text[index] != text[index+1]:
                abas.append(text[index]+text[index+1]+text[index+2])
        return abas

    @staticmethod
    def has_bab(aba: str, text: str):
        bab = aba[1]+aba[0]+aba[1]
        return bab in text

    @staticmethod
    def validate_with_abba(ip_address: IPAddress):
        for hypernet in ip_address.hypernets:
            if Validator.has_abba(hypernet):
                return False

        for supernet in ip_address.supernets:
            if Validator.has_abba(supernet):
                return True

        return False

    @staticmethod
    def validate_with_ssl(ip_address: IPAddress):
        # if aba in supernet and bab in hypernet
        all_abas = []
        for supernet in ip_address.supernets:
            abas = Validator.get_abas(supernet)
            if abas:
                all_abas += abas
        for hypernet in ip_address.hypernets:
            for aba in all_abas:
                if Validator.has_bab(aba, hypernet):
                    return True


def main():
    parser = InputParser()

    tls_ip_addresses = 0
    for address in parser.ip_addresses:
        if Validator.validate_with_abba(address):
            tls_ip_addresses += 1

    print("There are %s ip addresses that support TLS according to ABBA validation" % tls_ip_addresses)

    ssl_ip_addresses = 0
    for address in parser.ip_addresses:
        if Validator.validate_with_ssl(address):
            ssl_ip_addresses += 1

    print("There are %s ip addresses that support SSL" % ssl_ip_addresses)

if __name__ == '__main__':
    main()
