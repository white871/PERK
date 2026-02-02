import ast
from pprint import pformat

def binary_to_braille_unicode(binary):
    # Dot values for dots 1–6
    dot_values = [1, 2, 4, 8, 16, 32]

    chars = []

    # Process every 6-bit cell
    for i in range(0, len(binary), 6):
        cell = binary[i:i+6]

        value = 0
        for j, bit in enumerate(cell):
            if bit == "1":
                value += dot_values[j]

        chars.append(chr(0x2800 + value))

    return "".join(chars)

with open("Transliteration\\brailleLib.txt", "r") as f:
    brailleLib = ast.literal_eval(f.read())

enabled = {}

for binary, outputs in brailleLib.items():
    for out in outputs:
        if out.startswith("_") and out.endswith("_"):
            word = out.replace("_", "")
            
            if word not in enabled:
                enabled[word] = {
                    "binary": binary,
                    "braille": binary_to_braille_unicode(binary),
                    "enabled": 1   # default ON
                }

formatted = pformat(enabled, width=100, sort_dicts=True)

with open("EPICS BCI Code\\Data\\enabled_contractions.txt", "w", encoding="utf-8") as f:
    f.write(formatted)
