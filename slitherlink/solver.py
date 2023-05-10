from collections import deque
import copy
from slitherlink.model.error import UnsolvableError

from slitherlink.model.line_state import LineState
from typing import TYPE_CHECKING
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
    def getConnected(line: 'Line', lines: set['Line'] | None = None):
        if lines is None:
            lines = set([line])
        for x in filterLineByState(getLineNeighbors(line, slitherlink),
                                   LineState.SET):
            if x not in lines:
                lines.add(x)
                lines.update(getConnected(x, lines))
        return lines
    if not (all(field.isSolvable() for field in slitherlink.fieldlist) and
            all(isPointSolvable(point, slitherlink)
                for point in slitherlink.points)):
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
        if all(isPointSolved(p, slitherlink) for l in path for p in l.points):
            return False
    patches = [*getUnknownPatches(slitherlink)]
    for patch in patches:
        if sum(1 for point in patch if sum(1 for _ in filterLineByState(
                filterLineByPoint(slitherlink.linelist, point),
                LineState.SET)) == 1) % 2 == 1:
            return False
    return None


def solve(slitherlink: 'Slitherlink', start: 'Field'):  # Todo dont start at start
    from slitherlink.util.update import setLineState

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
                updated += setLineState(line, state, slitherlink)
        except UnsolvableError:
            for line in updated:
                line.setState(LineState.UNKNOWN)
            continue
        if currentLine.state != LineState.UNKNOWN:
            continue
        try:
            result = setLineState(currentLine, LineState.SET, slitherlink)
            if isSolvable(slitherlink) is False:
                raise UnsolvableError(
                    "Slitherlink contectivity Constraint")
        except UnsolvableError as _:
            updated = setLineState(currentLine, LineState.UNSET, slitherlink)
            lineQueue.clear()
            lineQueue.extend(([], l) for line in updated
                             for l in filterLineByState(
                getLineNeighbors(line, slitherlink), LineState.UNKNOWN))

        else:
            try:
                setLines = copy.deepcopy(result)
                for line in result:
                    setLineState(line, LineState.UNKNOWN, slitherlink)
                unsetLines = setLineState(currentLine, LineState.UNSET,
                                          slitherlink)
                if isSolvable(slitherlink) is False:
                    for line in unsetLines:
                        setLineState(line, LineState.UNKNOWN, slitherlink)
                    raise UnsolvableError(
                        "Slitherlink contectivity Constraint")
            except UnsolvableError as _:
                updated = setLineState(currentLine, LineState.SET, slitherlink)
                lineQueue.clear()
                lineQueue.extend(([], l) for line in updated
                                 for l in filterLineByState(
                    getLineNeighbors(line, slitherlink), LineState.UNKNOWN))
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
                    lineQueue.clear()
                    lineQueue.extend(([], l) for line in changedLines
                                     for l in filterLineByState(
                        getLineNeighbors(line, slitherlink),
                        LineState.UNKNOWN)
                    )
