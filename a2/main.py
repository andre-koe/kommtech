from LempelZivWelch import LempelZivWelch
from LempelZiv import LempelZiv

if __name__ == '__main__':

    with open('rfc2324.txt', 'r') as file:
        input_rfc = file.read()

    print(f"{len(input_rfc)}")

    zempel = LempelZiv(15) # 65535 Für Offset und Substr Länge
    enc = zempel.encode(input_rfc)
    dec = zempel.decode(enc[0], enc[1])

    #print(f"encoded rfc: {enc[0]}")
    print(f"encoded rfc Length: {len(enc[0])}")
    print(f"encoded rfc Bitstr: {enc[1]}")

    print(f"decoded rfc: {dec}")
    print(f"decoded rfc Length: {len(dec)}")
