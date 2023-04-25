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
        self.canvas.grid(column=1, row=1)
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.onClick)
        for i in range(10):
            self.canvas.bind(f"<KeyPress-{i}>", self.onNumberInputClosure(i))

    def draw(self):
        self.canvas.delete("all")
        if self.selected is not None:
            self.selected.draw(self.canvas, selected=True)
        self.slitherlink.draw(self.canvas)

    def onClick(self, event) -> None:
        print(f"Clicked at {event.x}, {event.y}")
        self.selected = self.slitherlink.onClick((event.x, event.y))
        self.draw()

    def onNumberInputClosure(self, number: int) -> callable:
        def onNumberInput(_: tkinter.Event):
            if self.selected is not None:
                self.selected.updateLabel(number)
            else:
                x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
                y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
                for field in self.slitherlink.fieldlist:
                    if field.isClicked((x, y)):
                        field.updateLabel(number)
            self.draw()
        return onNumberInput
