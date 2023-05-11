from typing import TYPE_CHECKING
from typing import Iterable
if TYPE_CHECKING:
    from slitherlink.model.field import Field

    from slitherlink.model.line import Line
    from slitherlink.model.line_state import LineState
    from slitherlink.model.point import Point


def filterLineByState(iter: Iterable['Line'], state: 'LineState'):
    yield from filter(lambda x: x.state == state, iter)


def filterLineByPoint(iter: Iterable['Line'], point: 'Point'):
    return filter(lambda x: point in x.points, iter)


def filterFieldByLine(iter: Iterable['Field'], line: 'Line'):
    return filter(lambda x: line in x.linelist, iter)
