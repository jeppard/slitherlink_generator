from collections import deque
import copy
from itertools import chain
from slitherlink.model.error import UnsolvableError

from slitherlink.model.line_state import LineState
from typing import TYPE_CHECKING, Iterable
from slitherlink.util.debug import timeit

from slitherlink.util.filter import filterLineByState, filterLineByPoint
from slitherlink.util.generator import getLineNeighbors, getUnknownPatches
if TYPE_CHECKING:
    from slitherlink.model.point import Point
    from slitherlink.model.field import Field
    from slitherlink.model.line import Line
    from slitherlink.model.slitherlink import Slitherlink


class SolverOptions:
    MAX_DEPTH = 1


def isSolved(slitherlink: 'Slitherlink'):
    return all(field.isSolved() for field in slitherlink.fieldlist) and \
        all(sum(1 for line in filterLineByPoint(slitherlink.linelist, point)
                if line.state == LineState.SET) in [0, 2]
            for point in slitherlink.points) and \
        slitherlink.hasOnePath()


def isPointSolved(point: 'Point', slitherlink: 'Slitherlink'):
    return sum(1 for line in filterLineByState(
        filterLineByPoint(slitherlink.linelist, point),
        LineState.SET)) in [0, 2]


def isPointSolvable(point: 'Point', slitherlink: 'Slitherlink'):
    lines = [*filterLineByPoint(slitherlink.linelist, point)]
    numSet = sum(1 for line in lines if line.state == LineState.SET)
    if numSet > 2:
        return False
    numUnknown = sum(1 for line in lines if line.state == LineState.UNKNOWN)
    return not (numSet == 1 and numUnknown == 0)


@timeit
def isSolvable(slitherlink: 'Slitherlink'):
    if isSolved(slitherlink):
        return True
    # TODO check if multiple loops are present

    for path in slitherlink.paths:
        if all(isPointSolved(p, slitherlink) for l in path for p in l.points):
            return False
    patches = [*getUnknownPatches(slitherlink)]
    for patch in patches:
        if sum(1 for point in patch if sum(1 for _ in filterLineByState(
                filterLineByPoint(slitherlink.linelist, point),
                LineState.SET)) == 1) % 2 == 1:
            return False
    return None


def solve(slitherlink: 'Slitherlink'):  # Todo dont start at start
    from slitherlink.util.update import setLineState

    def initLineQueue():
        lineQueue.clear()
        for path in slitherlink.paths:
            lineQueue.extend(([], line) for line in filterLineByState(
                chain(getLineNeighbors(path[0], slitherlink),
                      getLineNeighbors(path[-1], slitherlink)),
                LineState.UNKNOWN))
        for field in slitherlink.fieldlist:
            if not field.isSolved():
                lineQueue.extend(([], line) for line in filterLineByState(
                    field.linelist, LineState.UNKNOWN))
    lineQueue: deque[tuple[list[tuple['Line', LineState]], 'Line']] = deque()
    initLineQueue()
    while lineQueue:
        prevLines, currentLine = lineQueue.popleft()
        updated = []
        try:
            if any(line.state != LineState.UNKNOWN
                   for line, _ in prevLines) or \
                    currentLine.state != LineState.UNKNOWN:
                continue
            for line, state in prevLines:
                updated += setLineState(line, state, slitherlink)
        except UnsolvableError:
            for line in updated:
                line.setState(LineState.UNKNOWN)
            continue
        if currentLine.state != LineState.UNKNOWN:
            continue
        result: Iterable['Line'] = []
        try:
            result = setLineState(currentLine, LineState.SET, slitherlink)
            if isSolvable(slitherlink) is False:
                raise UnsolvableError(
                    "Slitherlink contectivity Constraint")
        except UnsolvableError as _:
            for line in result:
                setLineState(line, LineState.UNKNOWN, slitherlink)
            updated = setLineState(currentLine, LineState.UNSET, slitherlink)
            initLineQueue()

        else:
            unsetLines: Iterable['Line'] = []
            try:
                setLines = copy.deepcopy(result)
                for line in result:
                    setLineState(line, LineState.UNKNOWN, slitherlink)
                unsetLines = setLineState(currentLine, LineState.UNSET,
                                          slitherlink)
                if isSolvable(slitherlink) is False:
                    raise UnsolvableError(
                        "Slitherlink contectivity Constraint")
            except UnsolvableError as _:
                for line in unsetLines:
                    setLineState(line, LineState.UNKNOWN, slitherlink)
                updated = setLineState(currentLine, LineState.SET, slitherlink)
                initLineQueue()
            else:
                changedLines: list['Line'] = []
                for line in unsetLines:
                    if line not in setLines:
                        setLineState(line, LineState.UNKNOWN, slitherlink)
                        continue
                    stateSet = setLines[setLines.index(line)].state
                    if line.state != stateSet:
                        setLineState(line, LineState.UNKNOWN, slitherlink)
                        continue
                    # Line Changed
                    changedLines.append(line)

                if len(changedLines) == 0:
                    if len(prevLines) + 1 >= SolverOptions.MAX_DEPTH:
                        continue
                    lineQueue.extend((prevLines + [(currentLine, state)], line)
                                     for line in filterLineByState(
                        getLineNeighbors(currentLine, slitherlink),
                        LineState.UNKNOWN)
                        for state in (LineState.SET, LineState.UNSET)
                    )
                else:
                    initLineQueue()
