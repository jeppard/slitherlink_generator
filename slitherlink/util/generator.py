
from typing import Generator
from slitherlink.model.line import Line
from slitherlink.model.slitherlink import Slitherlink
from slitherlink.util.filter import filterLineByPoint


def getLineNeighbors(line: Line, slitherlink: Slitherlink):
    for point in line.points:
        yield from filter(lambda x: x != line,
                          filterLineByPoint(slitherlink.linelist, point))
