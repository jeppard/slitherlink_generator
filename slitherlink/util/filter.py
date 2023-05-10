from collections.abc import Iterable

from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState


def filterLine(iter: Iterable[Line], state: LineState):
    for line in iter:
        if line.state == state:
            yield line
