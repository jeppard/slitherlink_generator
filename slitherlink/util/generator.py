
from typing import Generator
from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.point import Point
from slitherlink.model.slitherlink import Slitherlink
from slitherlink.util.debug import timeit
from slitherlink.util.filter import filterLineByPoint, filterLineByState


def getLineNeighbors(line: Line, slitherlink: Slitherlink):
    for point in line.points:
        yield from filter(lambda x: x != line,
                          filterLineByPoint(slitherlink.linelist, point))


def getUnknownPatches(slitherlink: Slitherlink):
    def getPoints(point: Point, lines: set[Line] | None = None):
        points: set[Point] = set()
        if lines is None:
            lines = set()
        for line in filterLineByState(
                filterLineByPoint(slitherlink.linelist, point),
                LineState.UNKNOWN):
            if line not in lines:
                lines.add(line)
                for point in line.points:
                    points.update(getPoints(point, lines))
                    points.add(point)
        return points
    seenPoints = set()
    for point in slitherlink.points:
        if point in seenPoints:
            continue
        seenPoints.add(point)
        lines = [*filterLineByPoint(slitherlink.linelist, point)]
        numSet = sum(1 for _ in filterLineByState(lines, LineState.SET))
        if numSet == 0:
            points = getPoints(point)
            seenPoints.update(points)
            yield getPoints(point)
