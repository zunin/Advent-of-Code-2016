import hashlib

from common import BaseInputParser


class InputParser(BaseInputParser):
    @property
    def secret(self):
        for line in self.lines:
            return line


class MD5Hasher:
    def find_hash_with_prefix(self, id, prefix=0, prefix_length=5, password_length=8):
        part_1_password = []
        part_2_password = {}
        index = 0
        while len(part_1_password) < password_length or len(part_2_password) < password_length:
            id_plus_index = str(id)+str(index)
            hash_result = hashlib.md5(id_plus_index.encode()).hexdigest()

            if hash_result.startswith(prefix_length*str(prefix)):
                if len(part_1_password) < password_length:
                    part_1_password.append(hash_result[prefix_length])

                password_2_index = int(hash_result[prefix_length], 16)
                if len(part_2_password) < password_length and password_2_index < password_length and password_2_index not in part_2_password.keys():
                    part_2_password[password_2_index] = hash_result[prefix_length + 1]

            index += 1

        return part_1_password, part_2_password


def main():
    parser = InputParser()
    secret = parser.secret

    hasher = MD5Hasher()

    solution_1, solution_2 = hasher.find_hash_with_prefix(id=secret)
    print(solution_1, solution_2)
    print("The password is %s" % "".join(solution_1))
    print("The second door's password is %s" % "".join(solution_2.values()))

if __name__ == '__main__':
    main()
