# This is a sample Python script.
import math
import matplotlib.pyplot as plt


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


def tokenize(file_content: str):
    return file_content.split()

def return_information(number, total):
    prob = number / total
    return math.log2(1 / prob)


def word_length_occurrence_mapping(list_of_words: list):
    map_of_word_lengths = {}
    for word in list_of_words:
        length = len(word)
        map_of_word_lengths[length] = map_of_word_lengths.get(length, 0) + 1
    return map_of_word_lengths


def word_information_value(list_of_words: list):
    map_of_word_lengths = word_length_occurrence_mapping(list_of_words)
    total_word_count = len(list_of_words)
    result = [(length, return_information(count, total_word_count)) for length, count in
              map_of_word_lengths.items()]
    result.sort(key=lambda entry: entry[1], reverse=True)
    return result


def draw(word_info):
    x = [entry[0] for entry in word_info]
    y = [entry[1] for entry in word_info]

    plt.scatter(x, y)

    # Titel und Achsenbeschriftungen hinzufügen
    plt.title('Informationsgehalt nach Wortlänge')
    plt.xlabel('Wortlänge')
    plt.ylabel('Informationsgehalt')

    # Zeige das Diagramm an
    plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #information_map = word_information_value("BRAUCHBAREBIERBRAUERBURSCHENBRAUENBRAUSENDESBRAUNBIER")
    #print([(key, value[0], value[1], value[2]) for key, value in sorted(information_map.items(), key=lambda item: item[1][1], reverse=True)])
    #print(return_information_value(information_map))

    file_content = read_file("wortliste.txt")     ### READ IN FILE - RETURN CONTENT AS STRING
    word_list = tokenize(file_content)     ### TURN STRING TO LIST
    word_info_map = word_information_value(word_list)

    ### DRAW
    draw(word_info_map)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
