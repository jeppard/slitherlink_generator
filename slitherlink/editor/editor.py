import collections
import copy
import tkinter
from slitherlink import solver
from slitherlink.gui.field import FieldGui

from slitherlink.gui.gui_options import GUIOptions
from slitherlink.gui.line import LineGui
from slitherlink.model.line_state import LineState
from slitherlink.util.update import setFieldLabel
from ..gui.slitherlink import SlitherlinkGui
from PIL import ImageTk


class EditorGui():
    slitherlink: SlitherlinkGui

    def __init__(self,
                 slitherlink: SlitherlinkGui,
                 images: dict[str, ImageTk.PhotoImage],
                 screen: tkinter.Canvas | tkinter.Toplevel) -> None:
        self.slitherlink = slitherlink
        self.undoStack: collections.deque[SlitherlinkGui] = collections.deque()
        self.images = images
        self.screen = screen
        size = self.slitherlink.getSize()
        self.selected: FieldGui | None = None

        for widget in self.screen.winfo_children():
            widget.destroy()

        self.canvas = tkinter.Canvas(self.screen,
                                     width=size[1][0] - size[0][0] +
                                     2 * GUIOptions.MARGIN,
                                     height=size[1][1] - size[0][1] +
                                     2 * GUIOptions.MARGIN,
                                     bg=GUIOptions.BACKGROUND_COLOR)
        self.canvas.grid(column=0, row=0, sticky="nsew")
        tkinter.Button(self.screen, text="Back",
                       command=self.undo).grid(column=0, row=1)
        self.canvas.focus_set()
        self.screen.bind("<Button-1>", self.onLeftClick)
        for i in range(10):
            self.screen.bind(f"<KeyPress-{i}>", self.onNumberInputClosure(i))
        self.canvas.bind("<KeyPress-BackSpace>", self.undo)

    def undo(self, _: tkinter.Event | None = None):
        if len(self.undoStack) > 0:
            self.slitherlink = self.undoStack.pop()
            self.draw()

    def getPositionInsideCanvas(self, pos: tuple[int, int]) -> tuple[int, int]:
        return (pos[0] - self.canvas.winfo_rootx(),
                pos[1] - self.canvas.winfo_rooty())

    def draw(self):
        self.canvas.delete("all")
        isSolved = solver.isSolved(self.slitherlink)
        if isSolved:
            self.canvas.configure(bg=GUIOptions.SOLVED_BG_COLOR)
        else:
            self.canvas.configure(bg=GUIOptions.BACKGROUND_COLOR)
        if self.selected is not None:
            self.selected.draw(self.canvas, selected=True)
        self.slitherlink.draw(self.canvas)

    def onLeftClick(self, event: tkinter.Event) -> None:
        if event.widget != self.canvas:
            # Clicked outside of canvas
            self.selected = None
            self.draw()
            return
        for field in self.slitherlink.fieldlist:
            if field.isClicked((event.x, event.y)):
                self.selected = field
                self.draw()
                return

    def onNumberInputClosure(self, number: int):
        def onNumberInput(_: tkinter.Event):
            self.undoStack.append(copy.deepcopy(self.slitherlink))
            try:
                if self.selected is not None:
                    setFieldLabel(self.selected, number, self.slitherlink)
                    solver.solve(self.slitherlink, self.selected)
                else:
                    clickPos = (self.screen.winfo_pointerx(),
                                self.screen.winfo_pointery())
                    pos = self.getPositionInsideCanvas(clickPos)
                    for field in self.slitherlink.fieldlist:
                        if field.isClicked(pos):
                            setFieldLabel(field, number, self.slitherlink)
                            solver.solve(self.slitherlink, field)
            except solver.UnsolvableError:
                print("Number not allowed")
            self.draw()
        return onNumberInput
