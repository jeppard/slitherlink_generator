
import heapq
import math
from slitherlink.model.line_state import LineState
from typing import TYPE_CHECKING
from slitherlink.util.filter import filterLineByState

from slitherlink.util.generator import getLinesByPoint
if TYPE_CHECKING:
    from ..model.slitherlink import Slitherlink
    from ..model.point import Point


def distance(point1: 'Point', point2: 'Point'):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def isConnected(slitherlink: 'Slitherlink', start: 'Point', end: 'Point',
                allowedLineState: LineState = LineState.UNKNOWN):
    """Are these points connected via allowedLineState using A*

    Args:
        slitherlink (Slitherlink): Slitherlink Object start (Point): start
        point end (Point): end point allowedLineState (LineState, optional):
        Allowed LineState for Connections. Defaults to LineState.UNKNOWN.
    """
    heap = [(distance(start, end), start)]
    visited = set()
    backwards = {start: 0.0}
    heapq.heapify(heap)
    while heap:
        _, current = heapq.heappop(heap)
        visited.add(current)
        if current == end:
            return True
        for line in filterLineByState(getLinesByPoint(current, slitherlink),
                                      allowedLineState):
            for point in line.points:
                if point in visited:
                    continue
                backwards[point] = distance(
                    point, current) + backwards[current]
                heapq.heappush(
                    heap, (distance(point, end) + backwards[point], point))
    return False
