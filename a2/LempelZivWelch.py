class LempelZivWelch:

    def __init__(self):
        self.dictionary = {}
        self.dictionary_size = 0

    def encode(self, message: str, char_l: list) -> str:
        self.__init_dictionary(char_l)
        encoded_message = []
        s = message[0]
        for char in message[1:]:
            s_plus_c = s + char
            if s_plus_c in self.dictionary:
                s = s_plus_c
            elif s != '':
                encoded_message.append(s)
                self.dictionary[s_plus_c] = self.dictionary_size
                self.dictionary_size += 1
                s = char
        if s:
            encoded_message.append(self.dictionary[s])
        return ''.join(encoded_message)

    def __init_dictionary(self, char_l: list):
        for i, char in enumerate(char_l):
            self.dictionary[char] = i
        self.dictionary_size = len(char_l)
    @staticmethod
    def decode(bitstring: str, char_l: list) -> str:

        pass


