import hashlib

from common import BaseInputParser


class InputParser(BaseInputParser):
    @property
    def secret(self):
        for line in self.lines:
            return line


class MD5Hasher:

    def find_hash_with_prefix(self, id, prefix=0, prefix_length=5, password_length=8):
        password = []

        index = 0
        while len(password) < password_length:
            id_plus_index = str(id)+str(index)
            hash_result = hashlib.md5(id_plus_index.encode()).hexdigest()

            if hash_result.startswith(prefix_length*str(prefix)):
                password.append(hash_result[prefix_length])
            index += 1

        return "".join(password)


def main():
    parser = InputParser()
    secret = parser.secret

    hasher = MD5Hasher()

    print(hasher.find_hash_with_prefix(id=secret))


if __name__ == '__main__':
    main()
