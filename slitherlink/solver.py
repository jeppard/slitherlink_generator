from collections import deque
import copy
from slitherlink.model.error import UnsolvableException

from slitherlink.model.line_state import LineState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from slitherlink.model.field import Field
    from slitherlink.model.line import Line
    from slitherlink.model.slitherlink import Slitherlink


class SolverOptions:
    MAX_DEPTH = 4


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
        except UnsolvableException:
            pass
        else:
            yield [l]
        l = copy.deepcopy(line)
        try:
            l.setState(LineState.UNSET)
        except UnsolvableException:
            pass
        else:
            yield [l]


@timeit
def isSolvable(slitherlink: 'Slitherlink'):
    slitherlink = copy.deepcopy(slitherlink)
    if not (all(field.isSolvable() for field in slitherlink.fieldlist) and
            all(point.isSolvable() for point in slitherlink.points)):
        return False
    # TODO
    if isSolved(slitherlink):
        return True
    stack = deque(getAllEndLines(slitherlink))
    try:
        while stack:
            current = stack.pop()
            updated: list['Line'] = []
            try:
                for line in current:
                    for l in slitherlink.linelist:
                        if line != l:
                            continue
                        updated += l.setState(line.state)
                if isSolved(slitherlink):
                    return True
            except UnsolvableException:
                pass
            else:
                for line in updated:
                    for point in line.points:
                        for l in point.lines:
                            if l.state != LineState.UNKNOWN:
                                continue
                            try:
                                i = copy.deepcopy(l)
                                i.setState(LineState.SET)
                            except UnsolvableException:
                                pass
                            else:
                                stack.append(current + [i])
                            try:
                                i = copy.deepcopy(l)
                                i.setState(LineState.UNSET)
                            except UnsolvableException:
                                pass
                            else:
                                stack.append(current + [i])
        return False
    except UnsolvableException as _:
        print("UNSOLVABLE")
        return False


def solve(slitherlink: 'Slitherlink', start: 'Field'):
    lineQueue: deque[tuple['Line', int]] = deque(
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
                    for line in unsetLines:
                        line.setState(LineState.UNKNOWN)
                    raise UnsolvableException(
                        "Slitherlink contectivity Constraint")
            except UnsolvableException as _:
                currentLine.setState(LineState.SET)
            else:
                for line in unsetLines:
                    if line not in setLines:
                        line.setState(LineState.UNKNOWN)
                        # TODO higher Depth
                        continue
                    stateSet = setLines[setLines.index(line)].state
                    if line.state != stateSet:
                        line.setState(LineState.UNKNOWN)
                        # TODO higher Depth
