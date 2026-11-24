import sys
import re
from pathlib import Path

SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

for i in range(16):
    SYMBOLS[f"R{i}"] = i


COMP = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

DEST = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

JUMP = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

VALID_SYMBOL = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class AssemblerError(Exception):
    pass


def clean_line(line):
    """Remove comments and unnecessary whitespace."""
    line = line.split("//")[0]
    return "".join(line.split())


def first_pass(lines):
    """Find labels and store their ROM addresses."""
    symbols = SYMBOLS.copy()
    instructions = []
    rom_address = 0

    for line_number, raw_line in enumerate(lines, start=1):
        line = clean_line(raw_line)

        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]

            if not VALID_SYMBOL.fullmatch(label):
                raise AssemblerError(
                    f"Line {line_number}: Invalid label"
                )

            if label in symbols:
                raise AssemblerError(
                    f"Line {line_number}: Duplicate or reserved label"
                )

            symbols[label] = rom_address

        else:
            if "(" in line or ")" in line:
                raise AssemblerError(
                    f"Line {line_number}: Invalid instruction"
                )

            instructions.append((line_number, line))
            rom_address += 1

    return symbols, instructions


def assemble_a(line, symbols, variables, line_number):
    """Translate an A-instruction into 16-bit binary."""
    value = line[1:]

    if not value:
        raise AssemblerError(
            f"Line {line_number}: Missing A-instruction value"
        )

    if value.isdigit():
        address = int(value)

    else:
        if not VALID_SYMBOL.fullmatch(value):
            raise AssemblerError(
                f"Line {line_number}: Invalid instruction"
            )

        if value not in symbols:
            if value not in variables:
                variables[value] = len(variables) + 16

            address = variables[value]

        else:
            address = symbols[value]

    if not 0 <= address <= 32767:
        raise AssemblerError(
            f"Line {line_number}: Address out of range"
        )

    return format(address, "016b")


def assemble_c(line, line_number):
    """Translate a C-instruction into 16-bit binary."""

    if line.count("=") > 1 or line.count(";") > 1:
        raise AssemblerError(
            f"Line {line_number}: Invalid instruction"
        )

    if "=" in line:
        dest, remainder = line.split("=")
    else:
        dest, remainder = "", line

    if ";" in remainder:
        comp, jump = remainder.split(";")
    else:
        comp, jump = remainder, ""

    if (dest not in DEST or
            comp not in COMP or
            jump not in JUMP):
        raise AssemblerError(
            f"Line {line_number}: Invalid instruction"
        )

    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def assemble(input_file):
    """Convert a Hack assembly file into a .hack file."""

    lines = input_file.read_text(encoding="utf-8").splitlines()

    symbols, instructions = first_pass(lines)
    variables = {}

    machine_code = []

    for line_number, line in instructions:
        try:
            if line.startswith("@"):
                binary = assemble_a(
                    line, symbols, variables, line_number
                )
            else:
                binary = assemble_c(line, line_number)

            machine_code.append(binary)

        except AssemblerError:
            raise

        except Exception:
            raise AssemblerError(
                f"Line {line_number}: Invalid instruction"
            )

    output_file = input_file.with_suffix(".hack")

    output_file.write_text(
        "\n".join(machine_code) + "\n",
        encoding="utf-8"
    )

    print(f"Assembly successful!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Instructions generated: {len(machine_code)}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <input.asm>")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    try:
        assemble(input_file)

    except AssemblerError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
