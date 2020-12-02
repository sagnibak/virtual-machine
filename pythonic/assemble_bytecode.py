import argparse
from assembler import assembleWithRegisterOffset
from bytecode_assembler import assemble_bytecode

parser = argparse.ArgumentParser(description="Run an assembly file.")
parser.add_argument("-i", "--in_file", help="the file to read assembly from")
parser.add_argument("-o", "--out_file", help="the file to write bytecode to")
args = parser.parse_args()


with open(args.in_file, "r") as f:
    lines = f.readlines()

text_assembled = assembleWithRegisterOffset(lines)
bytecode_assembled = assemble_bytecode(text_assembled)

with open(args.out_file, "wb") as f:
    f.write(bytes(bytecode_assembled))
