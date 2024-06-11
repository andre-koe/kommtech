import numpy as np
import matplotlib.pyplot as plt

from a5.lib.komm._error_control_block import TerminatedConvolutionalCode, BlockDecoder, BlockEncoder
from a5.lib.komm._error_control_convolutional import ConvolutionalCode


"""In dieser Aufgabe soll die Übertragung eines Frames mit einem Convolutional Code zur Forward
   Error Correction (Fehlerkorrektur) simuliert werden. Das Ziel der Aufgabe ist, den besten
   Convolutional Code in Abhängigkeit der Bitfehlerrate zu bestimmen."""

"""Aufgabe 2:
   Wir betrachten in dieser Aufgabe den WLAN Faltungs-Code in Abbildung 1 mit eine nativen
   Code-Rate von 1/2 sowie die in Abbildung 2 und Abbildung 3 gegebenen Punktierungsmuster
   für Code-Raten von 3/4 und 2/3. Zusätzlich betrachten wir eine Convolutional Code mit Rate 1/3,
   der in oktaler Notation als 155,173,157 gegeben ist."""


def generate_binary_array(k, seed=None):
    np.random.seed(seed)
    return np.random.randint(2, size=k).tolist()


def generate_seeds(seed, M, lower=0, upper=100):
    np.random.seed(seed)
    return np.random.randint(lower, upper + 1, M).tolist()


def generate_error(frame, error_prob):
    errors = np.random.rand(*frame.shape) < error_prob
    return np.bitwise_xor(frame, errors.astype(int))


def simulate_cc(code: ConvolutionalCode, frame_length: int, frame_count: int, error_prob: float, seed: int, pattern):
    patterns = {
        '1/3': [1, 1, 1],  # Kein Punktierungsmuster
        '1/2': [1, 1, 0, 1, 1, 0],
        '2/3': [1, 1, 1, 0, 1, 1, 1, 0],
        '3/4': [1, 1, 1, 1, 0, 1, 1, 1, 1, 0]
    }

    t_code = TerminatedConvolutionalCode(convolutional_code=code, num_blocks=frame_length,
                                         mode='zero-termination')
    seeds = generate_seeds(seed, frame_count, lower=0, upper=frame_count * 10)  # contains seeds for frame generation
    frames = [generate_binary_array(frame_length, s) for s in seeds]
    frames_encoded = encode_messages(t_code, frames)
    original_decoded = decode_messages(t_code, frames_encoded)
    frames_encoded_punctured = [puncture(encoded, patterns[pattern]) for encoded in frames_encoded]
    error_frames = [generate_error(frame, error_prob) for frame in frames_encoded_punctured]
    frames_encoded_depunctured = [depuncture(punctured_encoded, patterns[pattern], len(frames_encoded[0])) for
                                  punctured_encoded in error_frames]

    frames_decoded = decode_messages(t_code, frames_encoded_depunctured)

    ### Stats

    # number_of_frames_with_errors = count_diff_frames(frames_encoded_punctured, error_frames)
    # number_of_correct_frames = frame_count - number_of_frames_with_errors
    # number_of_total_errors = count_bit_errors(frames_encoded_punctured, error_frames)
    # avg_bit_error_count_per_frame = number_of_total_errors / float(frame_count)
    # number_of_remaining_error_frames = count_diff_frames(original_decoded, frames_decoded)

    return stats(code, seed, frame_length, frame_count, pattern, error_prob, frames_encoded_punctured, error_frames,
                 original_decoded, frames_decoded)
    # ConvolutionalCode(code, k, M, pb, s)


def encode_messages(t_code: TerminatedConvolutionalCode, frames):
    encoder = BlockEncoder(t_code)

    return [encoder(f) for f in frames]


def decode_messages(t_code: TerminatedConvolutionalCode, frames):
    decoder = BlockDecoder(t_code, method="viterbi_soft")
    return [decoder(np.array(f, dtype=float)) for f in frames]


def count_equal_frames(l1, l2):
    count = 0
    for a, b in zip(l1, l2):
        if np.array_equal(a, b):
            count += 1
    return count


def count_diff_frames(l1, l2):
    count = 0
    for a, b in zip(l1, l2):
        if not np.array_equal(a, b):
            count += 1
    return count


def count_bit_errors(l1, l2) -> int:
    count = 0
    for a, b in zip(l1, l2):
        count += np.sum(a != b)
    return count


def stats(code, seed, frame_length, frame_count, pattern, error_prob, frames_encoded_punctured, error_frames,
          original_decoded, frames_decoded):
    return {
        "code": code,
        "seed": seed,
        "frame_length": frame_length,
        "frame_count": frame_count,
        "pattern": pattern,
        "error_prob": error_prob,
        "number_of_frames_with_errors": count_diff_frames(frames_encoded_punctured, error_frames),
        "number_of_correct_frames": frame_count - count_diff_frames(frames_encoded_punctured, error_frames),
        "number_of_total_errors": count_bit_errors(frames_encoded_punctured, error_frames),
        "avg_bit_error_count_per_frame": count_bit_errors(frames_encoded_punctured, error_frames) / float(frame_count),
        "number_of_remaining_error_frames": count_diff_frames(original_decoded, frames_decoded)
    }


def puncture(encoded_frame, pattern):
    punctured_frame = []
    pattern_length = len(pattern)
    for i, bit in enumerate(encoded_frame):
        if pattern[i % pattern_length] == 1:
            punctured_frame.append(bit)
    return np.array(punctured_frame)


def depuncture(received_frame, pattern, original_length):
    depunctured_frame = []
    pattern_length = len(pattern)
    j = 0
    for i in range(original_length):
        if pattern[i % pattern_length] == 1:
            if j < len(received_frame):
                depunctured_frame.append(received_frame[j])
                j += 1
            else:
                depunctured_frame.append(0)
        else:
            depunctured_frame.append(2)  # Verwende 2 für punktierte Bits
    return np.array(depunctured_frame)


def soft_decision_coding(received_frame):
    coded_frame = []
    for bit in received_frame:
        if bit == 2:
            coded_frame.append(0)  # Punktierte Bits werden als 0 behandelt
        else:
            coded_frame.append(1 if bit == 0 else -1)
    return np.array(coded_frame)


def simulate_fer(code: ConvolutionalCode, frame_length: int, frame_count: int, error_prob: float, pattern):
    t_code = TerminatedConvolutionalCode(convolutional_code=code, num_blocks=frame_length, mode='zero-termination')
    frames = [generate_binary_array(frame_length) for _ in range(frame_count)]
    frames_encoded = [t_code.enc_mapping(f) for f in frames]
    frames_punctured = [puncture(f, pattern) for f in frames_encoded]
    frames_with_errors = [generate_error(f, error_prob) for f in frames_punctured]
    frames_depunctured = [depuncture(f, pattern, len(frames_encoded[0])) for f in frames_with_errors]
    soft_decision_frames = [soft_decision_coding(f) for f in frames_depunctured]

    decoder = BlockDecoder(t_code, method="viterbi_soft")
    frames_decoded = [decoder(np.array(f, dtype=float)) for f in soft_decision_frames]

    return sum([not np.array_equal(f, d) for f, d in zip(frames, frames_decoded)]) / frame_count


def calculate_throughput(code_rate, fer):
    return code_rate * (1 - fer)


def plot(results: dict, code: ConvolutionalCode):
    plt.figure(figsize=(12, 6))
    plt.suptitle(f'({code.feedforward_polynomials})')

    plt.subplot(1, 2, 1)
    for rate, data in results.items():
        error_probs, fers, _ = zip(*data)
        plt.plot(error_probs, fers, label=f'Code-Rate {rate}')
    plt.xlabel('Bitfehlerwahrscheinlichkeit')
    plt.ylabel('Framefehlerrate (FER)')
    plt.title('Framefehlerrate vs. Bitfehlerwahrscheinlichkeit')
    plt.legend()

    plt.subplot(1, 2, 2)
    for rate, data in results.items():
        error_probs, _, throughputs = zip(*data)
        plt.plot(error_probs, throughputs, label=f'Code-Rate {rate}')
    plt.xlabel('Bitfehlerwahrscheinlichkeit')
    plt.ylabel('Durchsatz')
    plt.title('Durchsatz vs. Bitfehlerwahrscheinlichkeit')
    plt.legend()

    # plt.tight_layout()
    plt.show()

def demo():
    convolutional_code = ConvolutionalCode(feedforward_polynomials=[[0o133, 0o171]])
    test = generate_binary_array(7)
    code = TerminatedConvolutionalCode(convolutional_code=convolutional_code, num_blocks=7, mode='zero-termination')
    print("Test Code", test)
    encoder = BlockEncoder(code)
    encoded = encoder(test)
    patterns = {
        '1/3': [1, 1, 1],  # Kein Punktierungsmuster
        '1/2': [1, 1, 0, 1, 1, 0],
        '2/3': [1, 1, 1, 0, 1, 1, 1, 0],
        '3/4': [1, 1, 1, 1, 0, 1, 1, 1, 1, 0]
    }
    code_rate = '3/4'
    pattern = patterns[code_rate]
    punctured_encoded = puncture(encoded, pattern)
    error = generate_error(punctured_encoded, 0.0)
    depunctured_encoded = depuncture(punctured_encoded, pattern, encoded.shape[0])
    coding_table = soft_decision_coding(depunctured_encoded)
    decoder = BlockDecoder(code, method="viterbi_soft")
    print(f"""
            Encoded:        {encoded}
            Code-Rate:      {code_rate}
            Punctured:      {punctured_encoded}
            Error:          {error}
            Pattern:        {np.array(patterns[code_rate])}
            Depunctured:    {depunctured_encoded}
            Coding table:
            {coding_table}
            Decoded:        {decoder(np.array(coding_table, dtype=float))}
    """)
    res = simulate_cc(convolutional_code, 7, 10, 0.03, 42, "1/3")
    print(f"""
        STATS:
        =================================================================================
          CODE: {res['code']}
          SEED:                               {res['seed']}
          ERROR PROBABILITY:                  {res['error_prob']}
          FRAME LENGTH:                       {res['frame_length']}
          Number of frames transmitted:       {res['frame_count']}
          ---
          NUMBER OF ERROR FRAMES:             {res['number_of_frames_with_errors']}
          AVG BIT ERROR COUNT PER ENC FRAME:  {res['avg_bit_error_count_per_frame']}
          TOTAL ERROR COUNT OVERALL:          {res['number_of_total_errors']}
          ---
          CORRECTED AFTER DECODING:           {res['number_of_correct_frames']}
          REMAINING ERRORS AFTER DECODING:    {res['number_of_remaining_error_frames']}
        =================================================================================
        """)


if __name__ == "__main__":
    frame_length = 64
    frame_count = 20
    error_probs = np.linspace(0, 0.2, 21)
    code_rates = {
        '1/3': [1, 1, 1],  # Kein Punktierungsmuster
        '1/2': [1, 1, 0, 1, 1, 0],
        '2/3': [1, 1, 1, 0, 1, 1, 1, 0],
        '3/4': [1, 1, 1, 1, 0, 1, 1, 1, 1, 0]
    }

    convolutional_codes = [
        ConvolutionalCode(feedforward_polynomials=[[0o133, 0o171]]),
        ConvolutionalCode(feedforward_polynomials=[[0o155, 0o171, 0o157]])
    ]

    for convolutional_code in convolutional_codes:
        results = {rate: [] for rate in code_rates}

        for rate, pattern in code_rates.items():
            for error_prob in error_probs:
                fer = simulate_fer(convolutional_code, frame_length, frame_count, error_prob, pattern)
                throughput = calculate_throughput(eval(rate), fer)
                results[rate].append((error_prob, fer, throughput))

        plot(results, convolutional_code)
