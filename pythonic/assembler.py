from typing import List, Optional, Tuple


def assemble(lines: List[str]) -> List[Tuple[str, Optional[int]]]:
    """Takes in a file in the form of a list of lines, returns a list of lines
    representing the assembled file.
    """
    return list(map(resolveAddrs, resolveLabels(*findLabels(removeComments(lines)))))


def removeComments(lines: List[str]) -> List[str]:
    for i, line in enumerate(lines):
        line = line.split(";")[0]  # remove comments
        line = line.strip()
        lines[i] = line if line != "" else None  # type: ignore  # filtered
    return list(filter(lambda x: x is not None, lines))  # remove blank lines


def findLabels(lines: List[str]) -> Tuple[List[str], List[Tuple[int, str]]]:
    labels = []
    numLinesDeleted = 0
    for i, line in enumerate(lines):
        if ":" in line:
            label, rest = line.split(":")  # only one label allowed on any line
            labels.append((i - numLinesDeleted, label))
            if rest.strip() != "":
                lines[i] = rest
            else:
                lines[i] = None  # type: ignore  # will be filtered out
                numLinesDeleted += 1
    return list(filter(lambda x: x is not None, lines)), labels


def resolveLabels(lines: List[str], labels: List[Tuple[int, str]]) -> List[str]:
    for i, line in enumerate(lines):
        for labelIdx, label in labels:
            lines[i] = lines[i].replace(label, str(labelIdx))
    return lines


def resolveAddrs(line: str) -> Tuple[str, Optional[int]]:
    splitted = line.strip().split(" ")
    if len(splitted) == 1:
        return splitted[0], None
    else:
        arg = splitted[1]
        if arg[0] == "x":
            return splitted[0], int(splitted[1][1]) + 2
        else:
            return splitted[0], int(splitted[1])
