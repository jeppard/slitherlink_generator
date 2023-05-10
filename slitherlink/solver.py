from collections import deque
import copy
from slitherlink.model.error import StateError, UnsolvableError

from slitherlink.model.line_state import LineState
from typing import TYPE_CHECKING

from slitherlink.util.filter import filterLine
if TYPE_CHECKING:
    from slitherlink.model.field import Field
    from slitherlink.model.line import Line
    from slitherlink.model.slitherlink import Slitherlink


class SolverOptions:
    MAX_DEPTH = 1


def timeit(func):
    import time

    def timeit_wrap(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'{func.__name__} took {time.perf_counter()-start} seconds')
        return result
    return timeit_wrap


def isSolved(slitherlink: 'Slitherlink'):
    return all(field.isSolved() for field in slitherlink.fieldlist) and \
        all(point.isSolved() for point in slitherlink.points) and \
        slitherlink.hasOnePath()


def getAllEndLines(slitherlink: 'Slitherlink'):
    """
    This is a generator Function to yield all Lines that are next to a line
    with is set, but has no connection

    Args:
        slitherlink (Slitherlink): slitherlink from with the lines should be
        taken

    Yields:
        list[Line]: Yields 
    """
    for line in (line for point in slitherlink.points
                 for line in point.lines
                 if sum(1 for l in point.lines
                        if l.state == LineState.SET) == 1 and
                 line.state == LineState.UNKNOWN):
        l = copy.deepcopy(line)
        try:
            l.setState(LineState.SET)
        except UnsolvableError:
            pass
        else:
            yield [l]
        l = copy.deepcopy(line)
        try:
            l.setState(LineState.UNSET)
        except UnsolvableError:
            pass
        else:
            yield [l]


# @timeit
def isSolvable(slitherlink: 'Slitherlink'):
    def getConnected(line: 'Line', lines: set['Line'] | None = None):
        if lines is None:
            lines = set()
        for l in filterLine(line.getNeighbors(), LineState.SET):
            if l not in lines:
                lines.add(l)
                lines.update(getConnected(l, lines))
        return lines
    if not (all(field.isSolvable() for field in slitherlink.fieldlist) and
            all(point.isSolvable() for point in slitherlink.points)):
        return False
    if isSolved(slitherlink):
        return True
    # TODO check if multiple loops are present
    paths: list[set['Line']] = []
    seen: set['Line'] = set()
    for line in slitherlink.linelist:
        if line in seen:
            continue
        if line.state != LineState.SET:
            continue
        connected = getConnected(line)
        paths.append(connected)
        seen.update(connected)
    for path in paths:
        # ToDo detect Cycle
        if all(p.isSolved() for l in path for p in l.points):
            return False
    # TODO check if paths are connectable
    return None


def solve(slitherlink: 'Slitherlink', start: 'Field'):
    lineQueue: deque[tuple[list[tuple['Line', LineState]], 'Line']] = deque(
        ([], line) for line in start.linelist
        if line.state == LineState.UNKNOWN)
    while lineQueue:
        prevLines, currentLine = lineQueue.popleft()
        updated = []
        try:
            if any(line.state != LineState.UNKNOWN
                   for line, _ in prevLines) or \
                    currentLine.state != LineState.UNKNOWN:
                continue
            for line, state in prevLines:
                updated += line.setState(state)
        except UnsolvableError:
            for line in updated:
                line.setState(LineState.UNKNOWN)
            continue
        if currentLine.state != LineState.UNKNOWN:
            continue
        try:
            result = currentLine.setState(LineState.SET)
            if isSolvable(slitherlink) is False:
                raise UnsolvableError(
                    "Slitherlink contectivity Constraint")
        except UnsolvableError as _:
            updated = currentLine.setState(LineState.UNSET)
            lineQueue.clear()
            lineQueue.extend(([], l) for line in updated
                             for l in filterLine(
                line.getNeighbors(), LineState.UNKNOWN))

        else:
            try:
                setLines = copy.deepcopy(result)
                for line in result:
                    line.setState(LineState.UNKNOWN)
                unsetLines = currentLine.setState(LineState.UNSET)
                if isSolvable(slitherlink) is False:
                    for line in unsetLines:
                        line.setState(LineState.UNKNOWN)
                    raise UnsolvableError(
                        "Slitherlink contectivity Constraint")
            except UnsolvableError as _:
                updated = currentLine.setState(LineState.SET)
                lineQueue.clear()
                lineQueue.extend(([], l) for line in updated
                                 for l in filterLine(
                    line.getNeighbors(), LineState.UNKNOWN))
            else:
                changedLines: list['Line'] = []
                for line in unsetLines:
                    if line not in setLines:
                        line.setState(LineState.UNKNOWN)
                        continue
                    stateSet = setLines[setLines.index(line)].state
                    if line.state != stateSet:
                        line.setState(LineState.UNKNOWN)
                    else:
                        # Line Changed
                        changedLines.append(line)
                if len(changedLines) == 0:
                    if len(prevLines) + 1 >= SolverOptions.MAX_DEPTH:
                        continue
                    lineQueue.extend((prevLines + [(currentLine, state)], line)
                                     for line in filterLine(
                        currentLine.getNeighbors(), LineState.UNKNOWN)
                        for state in (LineState.SET, LineState.UNSET))
                else:
                    lineQueue.clear()
                    lineQueue.extend(([], l) for line in changedLines
                                     for l in filterLine(line.getNeighbors(),
                                                         LineState.UNKNOWN))
