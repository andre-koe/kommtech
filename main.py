# This is a sample Python script.
import heapq
import math
import random

import matplotlib.pyplot as plt

from EncodeDecode import EncodeDecode
from MessageSource import MessageSource
from arithmetic_compressor import AECompressor
from arithmetic_compressor.models import StaticModel


class HuffmanNode:
    def __init__(self, freq, chars):
        self.freq = freq
        self.chars = chars

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def word_information_value(word):
    values = {}
    word_length = len(word)
    for char in word:
        values[char] = values.get(char, 0) + 1

    for char, occurrence_count in values.items():
        probability = occurrence_count / word_length
        information_value = math.log2(1 / probability)
        values[char] = (occurrence_count, probability, information_value)
    return values


def return_information_value(information_dict: dict):
    information_acc = 0.0
    for value in information_dict.values():
        information_acc += value[0] * value[2]
    return information_acc


def return_min_bits(information_value: float):
    return math.ceil(information_value)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


### Aufgabe 1

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "Die angegebene Datei wurde nicht gefunden."
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"


def tokenize(content: str):
    return content.split()


def return_information(number, total):
    prob = number / total
    return math.log2(1 / prob)


def a_1_1_helper(list_of_words: list):
    map_of_word_lengths = {}
    for word in list_of_words:
        length = len(word)
        map_of_word_lengths[length] = map_of_word_lengths.get(length, 0) + 1
    return map_of_word_lengths


def a_1_1(list_of_words: list):
    map_of_word_lengths = a_1_1_helper(list_of_words)
    total_word_count = len(list_of_words)
    result = [(length, return_information(count, total_word_count)) for length, count in
              map_of_word_lengths.items()]
    result.sort(key=lambda entry: entry[1], reverse=True)
    return result


def a_1_3(wordlist: list, content: str, reverse=False, ignore_case=False):
    length = len(wordlist)
    prefix = ""
    chars = []
    information_gain = []
    last_len = length
    if reverse:
        wordlist = [word[::-1] for word in wordlist]
        content = content[::-1]
    if ignore_case:
        wordlist = [word.lower() for word in wordlist]
        content = content.lower()
    for char in content:
        prefix += char
        filtered_words = [word for word in wordlist if word.startswith(prefix)]
        filtered_length = len(filtered_words)
        chars.append(char)
        information_gain.append(return_information(filtered_length, last_len))
        last_len = filtered_length
    return chars, information_gain


def a_1_2(wordlist: list, character: str, index: int):
    return (character,
            index,
            len([word for word in wordlist
                 if len(word) > index and word[index] == character]))


def a_1_2_helper(wordlist: list, word: str, ignore_case=False):
    index = 0
    list_of_chars = []
    list_of_occurrences = []
    for char in word:
        if ignore_case:
            wordlist = [word.lower() for word in wordlist]
            char = char.lower()
        char, _, count = a_1_2(wordlist, char, index)
        list_of_chars.append(char)
        list_of_occurrences.append(return_information(count, len(wordlist)))
        index += 1
    return list_of_chars, list_of_occurrences


###################################################################

def return_character_occurrence_map(message: str):
    occurrence = {}
    for character in message:
        occurrence[character] = occurrence.get(character, 0) + 1
    return occurrence


def return_character_occurrence_prob(message: str) -> dict:
    occurrence = return_character_occurrence_map(message)
    for key, value in occurrence.items():
        occurrence[key] = value / len(message)
    return {k: v for k, v in sorted(occurrence.items(), key=lambda x: x[1], reverse=True)}


def return_encoded_string(string_to_encode: str, encoding_map: dict) -> str:
    return "".join([encoding_map[char] for char in string_to_encode])


###################################################################

def shannon_a_3_init(chars: str, ignore_case=False):
    if ignore_case:
        chars = chars.upper()
    character_occurrence_probs = return_character_occurrence_prob(chars)
    encoding_map = shannon_a_3([(k, v) for k, v in character_occurrence_probs.items()])
    encoded_string = return_encoded_string(chars, encoding_map)
    return encoded_string, encoding_map, len(encoded_string)


def shannon_a_3(character_occurrence_probs: list, prefix=''):
    if len(character_occurrence_probs) == 1:
        char, _ = character_occurrence_probs[0]
        return {char: prefix}

    upper, lower = find_split_point(character_occurrence_probs)

    codes = {}
    codes.update(shannon_a_3(upper, prefix + '0'))
    codes.update(shannon_a_3(lower, prefix + '1'))
    return codes


def find_split_point(character_occurrence_probs: list) -> tuple:
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


###################################################################

def huffman_a_3_init(chars: str, ignore_case=False):
    if ignore_case:
        chars = chars.upper()
    character_occurrence_map = return_character_occurrence_map(chars)
    encoding_map = {}
    huffman_a_3_tree_reconstruction(huffman_a_3(character_occurrence_map), encoding_map)
    encoded_string = return_encoded_string(chars, encoding_map)
    return encoded_string, encoding_map, len(encoded_string)


def huffman_a_3(occurrence_map: dict):
    huffman_nodes = [HuffmanNode(v, k) for k, v in occurrence_map.items()]
    heapq.heapify(huffman_nodes)

    while len(huffman_nodes) > 1:
        node_1 = heapq.heappop(huffman_nodes)
        node_2 = heapq.heappop(huffman_nodes)
        new = HuffmanNode(node_1.freq + node_2.freq, (node_1, node_2))
        heapq.heappush(huffman_nodes, new)

    return huffman_nodes[0]


def huffman_a_3_tree_reconstruction(node, encoding_map: dict, prefix=''):
    if isinstance(node.chars, str):
        encoding_map[node.chars] = prefix
    else:
        huffman_a_3_tree_reconstruction(node.chars[0], encoding_map, prefix + '0')
        huffman_a_3_tree_reconstruction(node.chars[1], encoding_map, prefix + '1')

###################################################################


def a_4_init():
    rfc_2324 = read_file("RFC-2324-HTCPCP.txt")

    count = 0
    to_be_encoded = []

    for count in range(10):
        count += 1
        to_be_encoded.append(MessageSource("".join(random.choices(rfc_2324, k=1000))))

    alg = ["SHANNON-FANO", "HUFFMAN", "ARITHMETIC ENCODING"]
    res = [len(val) for val in a_4_create_encodings(to_be_encoded)]

    draw_a_4(alg, res)


def a_4_create_encodings(tb_encoded: list[MessageSource]) -> tuple:
    encoded_shannon = []
    encoded_huffman = []
    encoded_arithmetic = []

    for un_encoded in tb_encoded:
        """ Encode with shannon """
        encoded_shannon.append(EncodeDecode(un_encoded, "shannon-fano").encode(un_encoded.word)[0])
        """ Encode with huffman """
        encoded_huffman.append(EncodeDecode(un_encoded, "huffman").encode(un_encoded.word)[0])
        """ Encode with arithmetic encoding """
        model = StaticModel(un_encoded.character_occurrence_prob)
        coder = AECompressor(model)
        encoded_arithmetic.append("".join([str(bit) for bit in coder.compress(un_encoded.word)]))
    return encoded_shannon, encoded_huffman, encoded_arithmetic


###################################################################


def draw_a_1_1(word_info):
    x = [entry[0] for entry in word_info]
    y = [entry[1] for entry in word_info]

    plt.scatter(x, y)

    plt.title('Informationsgehalt nach Wortlänge')
    plt.xlabel('Wortlänge')
    plt.ylabel('Informationsgehalt')

    plt.show()


def draw_bar_a_1_2(wordlist: list, word: str):
    x, y = a_1_2_helper(wordlist, word)

    plt.bar(x, y)

    plt.title(f'Informationsgehalt der Buchstaben in {word}')
    plt.xlabel('Buchstabe')
    plt.ylabel('Informationsgehalt')

    plt.show()


def draw_bar_a_1_3(wordlist: list, word: str, reverse: False):
    x, y = a_1_3(wordlist, word, reverse=reverse, ignore_case=True)

    plt.bar(x, y)

    if reverse:
        plt.title(f'Informationsgewinn der Buchstaben in {word} - {word[::-1]} Reversed')
    else:
        plt.title(f'Informationsgewinn der Buchstaben in {word}')
    plt.xlabel('Buchstabe')
    plt.ylabel('Informationsgewinn')

    plt.show()


def draw_a_4(alg: list, res: list):
    plt.bar(alg, res)

    plt.title('Durchschnittliche Länge der Kodierung bei 1000 Zeichen')
    plt.xlabel("Algorithm")
    plt.ylabel("Average #Bits")
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #information_map = word_information_value("BRAUCHBAREBIERBRAUERBURSCHENBRAUENBRAUSENDESBRAUNBIER")
    #print([(key, value[0], value[1], value[2]) for key, value in sorted(information_map.items(), key=lambda item: item[1][1], reverse=True)])
    #print(return_information_value(information_map))

    file_content = read_file("wortliste.txt")  ### READ IN FILE - RETURN CONTENT AS STRING
    word_list = tokenize(file_content)  ### TURN STRING TO LIST
    word_info_map = a_1_1(word_list)

    ### DRAW
    draw_a_1_1(word_info_map)
    draw_bar_a_1_2(word_list, "Xylofon")
    draw_bar_a_1_3(word_list, "Xylofon", reverse=False)
    draw_bar_a_1_3(word_list, "Xylofon", reverse=True)

    ### A.2
    msg = MessageSource("Hochschule")
    msg.print()

    ### A.3
    print("Shannon-Fano: ", shannon_a_3_init("Hochschule", ignore_case=True))
    print("Huffman:      ", huffman_a_3_init("Hochschule", ignore_case=True))

    msg_1 = MessageSource("Hochschule")
    msg_2 = MessageSource("HHHHH")
    msg_3 = MessageSource("EEEEE")

    encoding_11 = EncodeDecode(msg_1, "huffman")
    encoding_21 = EncodeDecode(msg_1, "shannon-fano")

    encoding_12 = EncodeDecode(msg_2, "huffman")
    encoding_22 = EncodeDecode(msg_2, "shannon-fano")

    encoding_13 = EncodeDecode(msg_3, "huffman")
    encoding_23 = EncodeDecode(msg_3, "shannon-fano")

    # encoding
    print("\n\nENCODING")
    print("\nHuffman Encoded: Hochschule is      ", encoding_11.encode("Hochschule"))
    print("Shannon-Fano Encoded: Hochschule is ", encoding_21.encode("Hochschule"))
    print("Huffman Encoded: HHHHH is           ", encoding_12.encode("HHHHH"))
    print("Shannon-Fano Encoded: HHHHH is      ", encoding_22.encode("HHHHH"))
    print("Huffman Encoded: EEEEE is           ", encoding_13.encode("EEEEE"))
    print("Shannon-Fano Encoded: EEEEE is      ", encoding_23.encode("EEEEE"))

    # decoding
    print("\n\nDECODING")
    print("\nHuffman Decoded: Code for Hochschule is      ", encoding_11.decode(encoding_11.encode("Hochschule")[0]))
    print("Shannon-Fano Decoded: Code for Hochschule is ", encoding_21.decode(encoding_21.encode("Hochschule")[0]))
    print("Huffman Decoded: Code for HHHHH is           ", encoding_12.decode(encoding_12.encode("HHHHH")[0]))
    print("Shannon-Fano Decoded: Code for HHHHH is      ", encoding_22.decode(encoding_22.encode("HHHHH")[0]))
    print("Huffman Decoded: Code for EEEEE is           ", encoding_13.decode(encoding_13.encode("EEEEE")[0]))
    print("Shannon-Fano Decoded: Code for EEEEE is      ", encoding_23.decode(encoding_23.encode("EEEEE")[0]))

    # A.4
    a_4_init()