from typing import List, Optional, Tuple


def assemble(lines: List[str]) -> List[Tuple[str, Optional[int]]]:
    """Takes in a file in the form of a list of lines, returns a list of lines
    representing the assembled file.
    """
    return list(map(resolveAddrs, resolveLabels(*findLabels(removeComments(lines)))))


def assembleWithRegisterOffset(lines: List[str]) -> List[Tuple[str, Optional[int]]]:
    """Takes in a file in the form of a list of lines, returns a list of lines
    representing the assembled file. The addresses are offset by 0x10 to account
    for the registers.
    """
    return resolveAddrsWithOffset(
        resolveLabels(*findLabelsWithOffset(removeComments(lines)))
    )


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


def findLabelsWithOffset(lines: List[str]) -> Tuple[List[str], List[Tuple[int, str]]]:
    labels = []
    numLinesDeleted = 0
    offset = 0x10
    for i, line in enumerate(lines):
        if ":" in line:
            label, rest = line.split(":")  # only one label allowed on any line
            labels.append((i - numLinesDeleted + offset, label))
            if rest.strip() != "":
                lines[i] = rest
                if len(rest.strip().split()) > 1:
                    offset += 1
            else:
                lines[i] = None  # type: ignore  # will be filtered out
                numLinesDeleted += 1
        elif len(line.strip().split()) > 1:
            offset += 1
    print(f"Labels: {labels}")
    return list(filter(lambda x: x is not None, lines)), labels


def resolveLabels(lines: List[str], labels: List[Tuple[int, str]]) -> List[str]:
    for i in range(len(lines)):
        for labelIdx, label in labels:
            lines[i] = lines[i].replace(label, str(labelIdx))
    return lines


def resolveAddrs(line: str) -> Tuple[str, Optional[int]]:
    splitted = line.strip().split(" ")
    if len(splitted) == 1:
        return splitted[0], None
    else:
        instruction, arg = splitted
        if arg == "ip":
            return instruction, 0
        if arg == "sp":
            return instruction, 1
        if arg == "fp":
            return instruction, 2
        elif arg[0] == "x":
            return instruction, int(arg[1]) + 3
        else:
            return instruction, int(arg)


def resolveAddrsWithOffset(lines: List[str]) -> List[Tuple[str, Optional[int]]]:
    offset = 0x10
    result: List[Tuple[str, Optional[int]]] = []
    for line in lines:
        splitted = line.strip().split(" ")
        if len(splitted) == 1:
            result.append((splitted[0], None))
        else:
            instruction, arg = splitted
            offset += 1
            if arg == "ip":
                result.append((instruction, 0))
            if arg == "sp":
                result.append((instruction, 1))
            if arg == "fp":
                result.append((instruction, 2))
            elif arg[0] == "x":
                result.append((instruction, int(arg[1]) + 3))
            else:
                result.append((instruction, int(arg)))
    return result
