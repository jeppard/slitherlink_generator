
from slitherlink import solver
from slitherlink.model.line import Line
from slitherlink.model.line_state import LineState
from slitherlink.model.point import Point
from .field import Field


class Slitherlink():
    def __init__(self, fieldlist: list[Field]) -> None:
        self.fieldlist = fieldlist
        self.points = list(
            set([p for field in fieldlist for p in field.pointlist]))
        self.linelist = list(
            set([line for field in fieldlist for line in field.linelist]))
        for line in self.linelist:
            for p in line.points:
                p.registerLine(line)

    def hasOnePath(self) -> bool:
        graph: dict[Point, list[Point]] = {}
        num_lines = 0
        for line in filter(lambda x: x.state == LineState.SET, self.linelist):
            num_lines += 1
            if not line.points[0] in graph:
                graph[line.points[0]] = []
            if not line.points[1] in graph:
                graph[line.points[1]] = []
            graph[line.points[0]].append(line.points[1])
            graph[line.points[1]].append(line.points[0])
        if num_lines == 0:
            return False
        visited: set[Point] = set()
        try:
            queue = [next(iter(graph))]
        except StopIteration:
            return False
        cycle_len = 0
        while queue:
            item = queue.pop()
            if item in visited:
                continue
            visited.add(item)
            cycle_len += 1
            for p in graph[item]:
                queue.append(p)
        return cycle_len == num_lines
    pass
