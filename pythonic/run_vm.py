import argparse
from assembler import assemble
from assembly_interpreter import execute


parser = argparse.ArgumentParser(description="Run an assembly file.")
parser.add_argument("file", help="the file to run")
args = parser.parse_args()


with open(args.file, "r") as f:
    code = assemble(f.readlines())

execute(code, stack=[], mem=[0 for _ in range(0xFFFF)])
