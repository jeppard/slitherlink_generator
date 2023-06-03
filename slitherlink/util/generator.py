
from functools import lru_cache
from typing import Generator
from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.point import Point
from slitherlink.model.slitherlink import Slitherlink
from slitherlink.util.debug import timeit
from slitherlink.util.filter import filterLineByPoint, filterLineByState

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..model.point import Point


@lru_cache
def getLineNeighbors(line: Line, slitherlink: Slitherlink):
    neighbors: list[Line] = []
    for point in line.points:
        for neighbor in getLinesByPoint(point, slitherlink):
            if neighbor != line:
                neighbors.append(neighbor)
    return neighbors


@lru_cache
def getLinesByPoint(point: 'Point', slitherlink: Slitherlink):
    return slitherlink.linesPerPoint[point]


def getConnectedPoints(point: Point, slitherlink: Slitherlink,
                       allowedLineState=LineState.UNKNOWN,
                       lines: set[Line] | None = None):
    points: set[Point] = set([point])
    if lines is None:
        lines = set()
    for line in filterLineByState(
        getLinesByPoint(point, slitherlink),
            LineState.UNKNOWN):
        if line not in lines:
            lines.add(line)
            for point in line.points:
                points.update(getConnectedPoints(point, slitherlink,
                                                 allowedLineState, lines))
                points.add(point)
    return points


def getUnknownPatches(slitherlink: Slitherlink):
    return slitherlink.patches
