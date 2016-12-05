class BaseInputParser:
    def __init__(self, file_name="input.txt"):
        self.file_name = file_name

    @property
    def lines(self):
        with open(self.file_name, "rt") as input_file:
            for line in input_file:
                yield line
