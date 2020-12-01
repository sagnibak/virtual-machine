import argparse
from typing import List, Optional, Tuple

from virtual_machine import execute


def parse_line(line: str) -> Optional[Tuple[str, Optional[int]]]:
    line = line.split(";")[0]  # don't read comments
    if len(line) > 0:
        splitted = line.strip().split(" ")
        if len(splitted) == 1:
            return splitted[0], None
        else:
            arg = splitted[1]
            if arg[0] == "x":
                return splitted[0], int(splitted[1][1]) + 2
            else:
                return splitted[0], int(splitted[1])
    else:
        return None


parser = argparse.ArgumentParser(description="Run an assembly file.")
parser.add_argument("file", help="the file to run")
args = parser.parse_args()


code: List[Tuple[str, Optional[int]]]
with open(args.file, "r") as f:
    code = list(
        filter(lambda x: x is not None, map(
            parse_line, f.readlines()))  # type: ignore
    )

execute(code, stack=[], mem=[0 for _ in range(0xFFFF)])
