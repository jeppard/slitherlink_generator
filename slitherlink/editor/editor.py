import tkinter
from slitherlink.gui.field import FieldGui

from slitherlink.gui.gui_options import GUIOptions
from ..gui.slitherlink import SlitherlinkGui
from PIL import ImageTk


class EditorGui():
    slitherlink: SlitherlinkGui

    def __init__(self,
                 slitherlink: SlitherlinkGui,
                 images: dict[str, ImageTk.PhotoImage],
                 screen: tkinter.Canvas) -> None:
        self.slitherlink = slitherlink
        self.images = images
        self.screen = screen
        size = self.slitherlink.getSize()
        self.selected = None

        for widget in self.screen.winfo_children():
            widget.destroy()

        self.canvas = tkinter.Canvas(self.screen,
                                     width=size[1][0] - size[0][0] +
                                     2 * GUIOptions.MARGIN,
                                     height=size[1][1] - size[0][1] +
                                     2 * GUIOptions.MARGIN,
                                     bg=GUIOptions.BACKGROUND_COLOR)
        self.canvas.pack()
        self.canvas.focus_set()
        self.screen.bind("<Button-1>", self.onClick)
        for i in range(10):
            self.canvas.bind(f"<KeyPress-{i}>", self.onNumberInputClosure(i))

    def getPositionInsideCanvas(self, pos: tuple[int, int]) -> tuple[int, int]:
        return (pos[0] - self.canvas.winfo_rootx(),
                pos[1] - self.canvas.winfo_rooty())

    def draw(self):
        self.canvas.delete("all")
        if self.selected is not None:
            self.selected.draw(self.canvas, selected=True)
        self.slitherlink.draw(self.canvas)

    def onClick(self, event) -> None:
        if event.widget != self.canvas:
            # Clicked outside of canvas
            self.selected = None
            self.draw()
            return
        self.selected = self.slitherlink.onClick((event.x, event.y))
        self.draw()

    def onNumberInputClosure(self, number: int) -> callable:
        def onNumberInput(_: tkinter.Event):
            if self.selected is not None:
                self.selected.updateLabel(number)
            else:
                clickPos = (self.screen.winfo_pointerx(),
                            self.screen.winfo_pointery())
                pos = self.getPositionInsideCanvas(clickPos)
                for field in self.slitherlink.fieldlist:
                    if field.isClicked(pos):
                        field.updateLabel(number)
            self.draw()
        return onNumberInput