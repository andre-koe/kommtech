import heapq

from MessageSource import MessageSource


class EncodeDecode:
    def __init__(self, msg: MessageSource, encoding_strategy: str):
        self.msg = msg
        self.encoding_strategy = encoding_strategy
        self.encoding_map = {}
        self.code, self.av_char_length, self.redundancy = self.encode(self.msg.word)

    def encode(self, word) -> tuple:
        word = word.upper()
        self.encoding_map.clear()
        character_occurrence_prob = self.msg.return_character_occurrence_prob()

        if self.encoding_strategy == 'shannon-fano':
            code = self.__shannon_init(word)
        else:
            code = self.__huffman_init(word)
        av_char_length = (
            sum([character_occurrence_prob[char] * len(self.encoding_map[char]) for char in self.encoding_map]))
        redundancy = av_char_length - self.msg.total_entropy
        return code, av_char_length, redundancy

    def decode(self, code: str) -> str:
        decoding_map = {v: k for k, v in self.encoding_map.items()}
        current_code = ""
        decoded_word = ""
        for char in code:
            current_code += char
            if current_code in decoding_map:
                decoded_word += decoding_map[current_code]
                current_code = ""
        return decoded_word

    # SHARED
    ###################################################################

    @staticmethod
    def __return_encoded_string(chars, encoding_map):
        """Catch trivial case where message consists of just one kind of character - encode with 0"""
        for char in chars:
            if encoding_map[char] == '':
                encoding_map[char] = '0'
        return "".join([encoding_map[char] for char in chars])

    # SHANNON - FANO IMPL
    ###################################################################

    def __shannon_init(self, chars: str, ignore_case=True):
        if ignore_case:
            chars = chars.upper()
        character_occurrence_probs = self.msg.return_character_occurrence_prob()
        self.encoding_map = self.__shannon([(k, v) for k, v in character_occurrence_probs.items()])
        encoded_string = self.__return_encoded_string(chars, self.encoding_map)
        return encoded_string

    def __shannon(self, character_occurrence_probs: list, prefix=''):
        if len(character_occurrence_probs) == 1:
            char, _ = character_occurrence_probs[0]
            return {char: prefix}

        upper, lower = self.__find_split_point(character_occurrence_probs)

        codes = {}
        codes.update(self.__shannon(upper, prefix + '0'))
        codes.update(self.__shannon(lower, prefix + '1'))
        return codes

    def __find_split_point(self, character_occurrence_probs: list) -> tuple:
        total_sum = sum([value for (_, value) in character_occurrence_probs])
        target_sum = total_sum / 2

        running_sum = 0
        split_point = 0

        for i, (_, value) in enumerate(character_occurrence_probs):
            if running_sum + value > target_sum:
                if abs(target_sum - running_sum) < abs((running_sum + value) - target_sum):
                    split_point = i
                else:
                    split_point = i + 1
                break
            running_sum += value

        return character_occurrence_probs[:split_point], character_occurrence_probs[split_point:]

    # HUFFMAN IMPL
    ###################################################################

    def __huffman_init(self, chars: str, ignore_case=True):
        if ignore_case:
            chars = chars.upper()
        character_occurrence_map = self.msg.return_character_occurrence_map()
        self.__huffman_prefix_generation(self.__huffman(character_occurrence_map), self.encoding_map)
        encoded_string = self.__return_encoded_string(chars, self.encoding_map)
        return encoded_string

    def __huffman(self, occurrence_map: dict):
        huffman_nodes = [HuffmanNode(v, k) for k, v in occurrence_map.items()]
        heapq.heapify(huffman_nodes)

        while len(huffman_nodes) > 1:
            node_1 = heapq.heappop(huffman_nodes)
            node_2 = heapq.heappop(huffman_nodes)
            new = HuffmanNode(node_1.freq + node_2.freq, (node_1, node_2))
            heapq.heappush(huffman_nodes, new)

        return huffman_nodes[0]

    def __huffman_prefix_generation(self, node, encoding_map: dict, prefix=''):
        if isinstance(node.chars, str):
            encoding_map[node.chars] = prefix
        else:
            self.__huffman_prefix_generation(node.chars[0], encoding_map, prefix + '0')
            self.__huffman_prefix_generation(node.chars[1], encoding_map, prefix + '1')


class HuffmanNode:
    def __init__(self, freq, chars):
        self.freq = freq
        self.chars = chars

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq
