from itertools import combinations

import numpy as np


class BlockCode:

    # k: Anzahl Nutzbits
    # n: Anzahl CodeBits
    # p: Anzahl Prüfbits
    # max_corr_bits: maximale Anzahl korrigierter Bits (bis zu 2 soll unterstützt werden
    # G: Generatormatrix
    # P: Teil-Matrix wird übergeben
    # H: Kontrollmatrix
    # S: Syndrom-Tabelle
    def __init__(self, max_corr_bits: int, p: np.ndarray):
        self.P = p
        self.max_corr_bits = max_corr_bits

        self.k = 0
        self.n = 0
        self.G = np.eye(1)
        self.H = np.eye(1)
        self.S = {}

    def encode(self, message: np.array) -> np.array:
        self.k = len(message)
        self.G = self.__return_generator_matrix(self.k)
        codeword = (message @ self.G) % 2
        self.n = len(codeword)
        return codeword.astype(int)

    def decode(self, codeword) -> tuple:
        self.H = self.__return_parity_check_matrix(self.n - self.k)
        print(self.H)
        self.__generate_syndrome_table()
        syndrome = self.__return_syndrome(codeword)
        message = codeword[self.n - self.k:]
        if self.__count_error(syndrome) == 0:
            return message, 0
        else:
            codeword, count = self.__correct_error(syndrome, codeword)
            if codeword is None or count is None:
                return None, None
            message = codeword[self.n - self.k:]
            return message, count

    def __return_generator_matrix(self, dim: int) -> np.ndarray:
        return np.concatenate([self.P, self.__return_identity_matrix(dim)], axis=1)

    def __return_parity_check_matrix(self, dim: int) -> np.ndarray:
        return np.concatenate([self.__return_identity_matrix(dim), self.P.transpose()], axis=1)

    def __return_identity_matrix(self, dim: int) -> np.ndarray:
        return np.eye(dim)

    def __generate_syndrome_table(self):
        self.S = {}

        if self.max_corr_bits == 2:
            for i, j in combinations(range(self.n), 2):
                e = np.zeros((self.n,), dtype=int)
                e[i] = 1
                e[j] = 1
                s = (e @ self.H.transpose()) % 2
                self.S[self.__syndrome_to_int(s)] = tuple(e)

        for i in range(self.n):
            e = np.zeros((self.n,), dtype=int)
            e[i] = 1
            s = (e @ self.H.transpose()) % 2
            self.S[self.__syndrome_to_int(s)] = tuple(e)
        print(self.S)

    # Not wanted as we still correct in any case
    def __add_to_syndrome_table(self, syndrome: np.array, error: np.array):
        s = self.__syndrome_to_int(syndrome)
        if s in self.S:
            self.S[s] = tuple(error)
        else:
            self.S[s] = tuple(error)

    def __return_syndrome(self, codeword):
        return (codeword @ self.H.transpose()) % 2

    def __correct_error(self, syndrome, codeword):
        print("Syndrome: ", syndrome)
        error = self.S.get(self.__syndrome_to_int(syndrome))
        err_count = self.__count_error(error)
        y_correct = (error + codeword) % 2
        return y_correct, err_count

    def __count_error(self, error: np.array):
        return np.count_nonzero(error)

    def __print_syndrome_table(self):
        for key, value in self.S.items():
            print(f"{key}: {value}")

    def __syndrome_to_int(self, syndrome: np.array):
        syndrome = syndrome.astype(int)
        return int(''.join([f'{b}' for b in syndrome]), 2)

