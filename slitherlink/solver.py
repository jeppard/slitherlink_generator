from collections import deque
import copy
from slitherlink.model.error import UnsolvableException
from slitherlink.model.field import Field
from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.slitherlink import Slitherlink


class SolverOptions:
    MAX_DEPTH = 4


def isSolved(slitherlink: Slitherlink):
    return all(field.isSolved() for field in slitherlink.fieldlist) and \
        all(point.isSolved() for point in slitherlink.points) and \
        slitherlink.hasOnePath()


def isSolvable(slitherlink: Slitherlink):
    return all(field.isSolvable() for field in slitherlink.fieldlist) and \
        all(point.isSolvable() for point in slitherlink.points) and \
        slitherlink.isSolvable()


def solve(slitherlink: Slitherlink, start: Field):
    lineQueue: deque[tuple[Line, int]] = deque(
        (line, 1) for line in start.linelist)
    while lineQueue:
        currentLine, depth = lineQueue.popleft()
        if currentLine.state != LineState.UNKNOWN:
            continue
        try:
            result = currentLine.setState(LineState.SET)
            if not isSolvable(slitherlink):
                raise UnsolvableException(
                    "Slitherlink contectivity Constraint")
        except UnsolvableException as _:
            currentLine.setState(LineState.UNSET)

        else:
            try:
                setLines = copy.deepcopy(result)
                for line in result:
                    line.setState(LineState.UNKNOWN)
                unsetLines = currentLine.setState(LineState.UNSET)
                if not isSolvable(slitherlink):
                    raise UnsolvableException(
                        "Slitherlink contectivity Constraint")
            except UnsolvableException as _:
                currentLine.setState(LineState.SET)
            else:
                for line in unsetLines:
                    if line not in setLines:
                        line.setState(LineState.UNKNOWN)
                        continue
                    stateSet = setLines[setLines.index(line)].state
                    if line.state != stateSet:
                        line.setState(LineState.UNKNOWN)
