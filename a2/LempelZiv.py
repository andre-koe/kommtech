### Zeichenkette wird über Tripel aus Position, Länge und nächstem
### Zeichen codiert
### – codiert wird längste Zeichenkette, die im bisherigen Text vorkam
### – Position wird ab der Stelle des codierten Zeichens rückwärts gezählt
### – Maximalwert für die Position beschränkt die Größe des Wörterbuchs
import math


class LempelZiv:

    def __init__(self, num_bits_length):
        self.num_bits_offset = 0
        self.num_bits_length = num_bits_length

    def encode(self, message: str) -> tuple:
        self.__find_largest_substring(message)
        print(f"NUM_BITS_OFFSET: {self.num_bits_offset}")
        list_of_tuples = self.__generate_references(message)

        unique_chars = set(message)
        num_bits_char = math.ceil(math.log2(len(unique_chars)))
        char_d = {char: format(i, f'0{num_bits_char}b') for i, char in enumerate(unique_chars)}

        bitstring = ""
        for offset, length, char in list_of_tuples:
            encoded_offset = format(offset, f'0{self.num_bits_offset}b')
            encoded_length = format(length, f'0{self.num_bits_length}b')
            encoded_char = char_d[char] if char else ""
            bitstring += encoded_offset + encoded_length + encoded_char

        return bitstring, char_d

    def decode(self, bitstring, char_d):
        rev_char_d = {v: k for k, v in char_d.items()}
        num_bits_char = len(next(iter(char_d.values())))
        result = ""

        i = 0
        while i < len(bitstring):
            if i + self.num_bits_offset + self.num_bits_length > len(bitstring):
                break

            offset_bits = bitstring[i:i + self.num_bits_offset]
            length_bits = bitstring[i + self.num_bits_offset:i + self.num_bits_offset + self.num_bits_length]
            char_bits = bitstring[i + self.num_bits_offset + self.num_bits_length:i + self.num_bits_offset
                                    + self.num_bits_length + num_bits_char]

            offset = int(offset_bits, 2)
            length = int(length_bits, 2)
            char = rev_char_d.get(char_bits, "")

            if offset > 0:
                start = max(0, len(result) - offset)
                end = start + length
                result += result[start:end]

            result += char

            i += self.num_bits_offset + self.num_bits_length + num_bits_char

        return result

    def __generate_references(self, message):
        tuples, substr, search_window, offset = self.__init_generate_references()
        for i in range(len(message)):
            substr += message[i]
            start_index = search_window.rfind(substr)
            if start_index == -1: #or len(substr) >= (2 ** self.num_bits_length - 1):
                tuples += [(offset, len(substr) - 1, message[i])]
                offset = 0
                substr = ""
                search_window = message[:i]
            elif i >= len(message) - 1:
                tuples += [(offset, len(substr), message[i])]
            else:
                offset = (i - len(substr) - start_index) + 1
        return tuples

    def __find_largest_substring(self, message):
        self.num_bits_length = math.ceil(math.log2(max([l for o, l, _ in self.__generate_references(message)])))
        self.num_bits_offset = math.ceil(math.log2(max([o for o, l, _ in self.__generate_references(message)])))

    @staticmethod
    def __init_generate_references():
        return [], "", "", 0

    ## Kept for learning purposes, incorrect tuple list generation due to updating the search window aswell as the
    ## character index together. This causes issues when dealing with the same character consecutively e.g. AAAAAAAA
    def __generate_backward_reference_tuples(self, message: str) -> list:
        max_length = 2**self.num_bits_length-1
        max_offset = 2**self.num_bits_offset-1

        list_of_tuples = []
        substr = ""
        go_back = 0
        substr_set = False

        for i in range(len(message)):
            char = message[i]
            substr += char
            current_substr = message[max(0, i - max_offset):i]
            found_at = current_substr.rfind(substr)
            if found_at == -1 or len(substr) >= max_length:
                list_of_tuples += [(go_back, len(substr) - 1, char)]
                substr = ""
                go_back = 0
                substr_set = False
            elif i == len(message) - 1:
                list_of_tuples += [(go_back, len(substr), char)]  # Done
            else:
                go_back = (i - found_at)
                if not substr_set:
                    substr_set = True
                    substr = char

        return list_of_tuples
