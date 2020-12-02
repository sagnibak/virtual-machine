import argparse
from assembler import assemble
from vm import VM


parser = argparse.ArgumentParser(description="Run bytecode file.")
parser.add_argument("file", help="the file to run")
args = parser.parse_args()


with open(args.file, "rb") as f:
    code = f.read()

mem = bytearray(0x100000)  # 1 MiB
mem[0x80 : 0x80 + len(code)] = code  # setup the code section
VM(mem).reset().run()
