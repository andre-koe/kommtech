import math


class MessageSource:
    def __init__(self, word: str, ignore_case: bool = True):
        self.word = word
        if ignore_case:
            self.word = word.upper()
        self.character_occurrence = self.return_character_occurrence_map()
        self.character_occurrence_prob = self.return_character_occurrence_prob()
        self.character_information = self.return_character_information()
        self.character_entropy = self.return_character_entropy()
        self.total_information_value = self.return_total_information_value()
        self.total_entropy = self.return_total_entropy()
        self.min_bit_encoding = self.return_min_bit_encoding()

    def return_character_occurrence_map(self):
        occurrence = {}
        for character in self.word:
            occurrence[character] = occurrence.get(character, 0) + 1
        return occurrence

    def return_character_occurrence_prob(self) -> dict:
        occurrence = self.return_character_occurrence_map()
        for key, value in occurrence.items():
            occurrence[key] = value / len(self.word)
        return {k: v for k, v in sorted(occurrence.items(), key=lambda x: x[1], reverse=True)}

    def return_character_entropy(self) -> dict:
        entropy = {}
        for character in self.word:
            entropy[character] = self.character_occurrence_prob[character] * self.character_information[character]
        return {k: v for k, v in sorted(entropy.items(), key=lambda x: x[1], reverse=True)}

    def return_character_information(self) -> dict:
        information = {}
        for character in self.word:
            information[character] = math.log2(1 / self.character_occurrence_prob[character])
        return {k: v for k, v in sorted(information.items(), key=lambda x: x[1], reverse=True)}

    def return_total_information_value(self) -> float:
        total = 0
        for key, value in self.character_occurrence.items():
            total += value * self.character_information[key]
        return total

    def return_min_bit_encoding(self) -> int:
        return math.ceil(self.total_information_value)

    def return_total_entropy(self) -> float:
        total = 0
        for _, value in self.character_entropy.items():
            total += value
        return total

    def print(self):
        print(
            f"""Nachricht: {self.word[:20]}\n{self.word}\n\n===========================\n - Auftrittswahrscheinlichkeit Zeichen: {self.character_occurrence_prob}\n - Informationswert Zeichen:            {self.character_information}\n - Entropie Zeichen:                    {self.character_entropy}\n\n - Min Bits: {self.min_bit_encoding}\n - Total Entropy: {self.total_entropy}\n - Total Information: {self.total_information_value}\n===========================""")
