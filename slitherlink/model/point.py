from typing import TYPE_CHECKING
import dataclasses

from slitherlink.model.line_state import LineState
if TYPE_CHECKING:
    from slitherlink.model.line import Line


@dataclasses.dataclass(order=True, frozen=True)
class Point():
    x: int
    y: int
    lines: list['Line'] = dataclasses.field(
        default_factory=list, init=False, repr=False, compare=False)

    def registerLine(self, line: 'Line') -> None:
        self.lines.append(line)

    def update(self, depth=1):
        pass
