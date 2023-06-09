from collections import deque
import copy
from itertools import chain
from slitherlink.model.error import UnsolvableError

from slitherlink.model.line_state import LineState
from typing import TYPE_CHECKING, Iterable
from slitherlink.util.debug import accumulate, timeit

from slitherlink.util.filter import filterLineByState
from slitherlink.util.generator import getLineNeighbors, getLinesByPoint, getUnknownPatches
if TYPE_CHECKING:
    from slitherlink.model.point import Point
    from slitherlink.model.field import Field
    from slitherlink.model.line import Line
    from slitherlink.model.slitherlink import Slitherlink


class SolverOptions:
    MAX_DEPTH = 1


def isSolved(slitherlink: 'Slitherlink'):
    return all(field.isSolved() for field in slitherlink.fieldlist) and \
        all(sum(1 for line in getLinesByPoint(point, slitherlink)
                if line.state == LineState.SET) in [0, 2]
            for point in slitherlink.points) and \
        slitherlink.hasOnePath()


def isPointSolved(point: 'Point', slitherlink: 'Slitherlink'):
    return sum(1 for line in filterLineByState(
        getLinesByPoint(point, slitherlink),
        LineState.SET)) in [0, 2]


def isPointSolvable(point: 'Point', slitherlink: 'Slitherlink'):
    lines = getLinesByPoint(point, slitherlink)
    numSet = sum(1 for line in lines if line.state == LineState.SET)
    if numSet > 2:
        return False
    numUnknown = sum(1 for line in lines if line.state == LineState.UNKNOWN)
    return not (numSet == 1 and numUnknown == 0)


# @timeit
def isSolvable(slitherlink: 'Slitherlink'):
    if isSolved(slitherlink):
        return True
    # TODO check if multiple loops are present

    seenPoints: set['Point'] = set()
    for path in slitherlink.paths:
        if all(isPointSolved(p, slitherlink) for l in path for p in l.points):
            return False
    patches = [*getUnknownPatches(slitherlink)]
    for patch in patches:
        if sum(1 for point in patch if sum(1 for _ in filterLineByState(
                getLinesByPoint(point, slitherlink),
                LineState.SET)) == 1) % 2 == 1:
            return False
    return None


@accumulate
def solve(slitherlink: 'Slitherlink'):  # Todo dont start at start
    from slitherlink.util.update import setLineState

    def tryAllCombinations(lines: list['Line']) -> list['Line']:
        if len(lines) == 0:
            return []
        if any(line.state != LineState.UNKNOWN for line in lines):
            return []
        updated = []
        currentLines = []
        try:
            currentLines = setLineState(
                lines[0], LineState.SET, slitherlink)
            currentLines += tryAllCombinations(lines[1:])
            if isSolvable(slitherlink) is False:
                raise UnsolvableError("Connectivity Constraint failed")
        except UnsolvableError:
            for line in currentLines:
                setLineState(line, LineState.UNKNOWN, slitherlink)
            return setLineState(lines[0], LineState.UNSET, slitherlink)
        else:
            unsetLines = []
            setLines = copy.deepcopy(currentLines)
            for line in currentLines:
                setLineState(line, LineState.UNKNOWN, slitherlink)
            try:
                unsetLines = setLineState(
                    lines[0], LineState.UNSET, slitherlink)
                unsetLines += tryAllCombinations(lines[1:])
                if isSolvable(slitherlink) is False:
                    raise UnsolvableError("Connectivity Constraint failed")
            except UnsolvableError:
                for line in unsetLines:
                    setLineState(line, LineState.UNKNOWN, slitherlink)
                return setLineState(lines[0], LineState.SET, slitherlink)
            else:
                idxSet, idxUnset = 0, 0
                setLines.sort()
                tmp = copy.deepcopy(unsetLines)
                for line in unsetLines:
                    setLineState(line, LineState.UNKNOWN, slitherlink)
                unsetLines = tmp
                unsetLines.sort()
                while idxSet < len(setLines) and idxUnset < len(unsetLines):
                    if setLines[idxSet] < unsetLines[idxUnset]:
                        idxSet += 1
                        continue
                    if setLines[idxSet] > unsetLines[idxUnset]:
                        idxUnset += 1
                        continue
                    if setLines[idxSet].state == unsetLines[idxUnset].state:
                        idx = slitherlink.linelist.index(setLines[idxSet])
                        line = slitherlink.linelist[idx]
                        updated.append(line)
                        updated.extend(setLineState(
                            line, setLines[idxSet].state, slitherlink))
                    idxSet += 1
                    idxUnset += 1
        return updated

    def initLineQueue():
        lineQueue.clear()
        for path in slitherlink.paths:
            lineQueue.extend([l] for l in filterLineByState(
                chain(getLineNeighbors(path[0], slitherlink),
                      getLineNeighbors(path[-1], slitherlink)),
                LineState.UNKNOWN))
        for field in slitherlink.fieldlist:
            if not field.isSolved():
                lineQueue.extend([l] for l in filterLineByState(
                    field.linelist, LineState.UNKNOWN))
    lineQueue: deque[list['Line']] = deque()
    initLineQueue()
    while lineQueue:
        lines = lineQueue.popleft()
        updated = tryAllCombinations(lines)
        if len(updated) == 0:
            if len(lines) < SolverOptions.MAX_DEPTH:
                lineQueue.extend(lines + [line]
                                 for line in getLineNeighbors(lines[-1],
                                                              slitherlink))
        else:
            initLineQueue()
