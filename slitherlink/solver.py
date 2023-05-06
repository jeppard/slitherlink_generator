import z3

from typing import TYPE_CHECKING

from slitherlink.model.line_state import LineState
if TYPE_CHECKING:
    from slitherlink.model.line import Line
    from .model.slitherlink import Slitherlink


class SlitherlinkSolver():
    def __init__(self, slitherlink: 'Slitherlink'):
        self.slitherlink = slitherlink

    def addConstraints(self, solver: z3.Solver) -> None:
        for field in self.slitherlink.fields:
            if field.number is None:
                continue
            solver.add(
                z3.Sum([line.z3Var for line in field.linelist]) == field.number)
        for point in self.slitherlink.points:
            solver.add(z3.Or(z3.Sum([line.z3Var for line in point.lines]) == 2,
                             z3.Sum([line.z3Var for line in point.lines]) == 0))

    def isSolvable(self) -> bool:
        solver = z3.Solver()
        self.addConstraints(solver)
        return solver.check() == z3.sat

    def solve(self, line: 'Line') -> None:
        if not self.isSolvable():
            return

        if line.state != LineState.UNKNOWN:
            return
        solver = z3.Solver()
        self.addConstraints(solver)
        solver.check()
        model = solver.model()
        lineResult = z3.is_true(model.eval(line.z3Var))
        solver.add(line.z3Var != lineResult)
        if solver.check() == z3.unsat:
            print(lineResult)
            line.state = LineState.SET if lineResult else LineState.UNSET
            for point in line.points:
                for l in point.lines:
                    self.solve(l)
            for field in line.fields:
                for l in field.linelist:
                    self.solve(l)
