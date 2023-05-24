import tkinter
from slitherlink.gui.field import FieldGui

from slitherlink.gui.gui_options import GUIOptions
import tkinter.filedialog
import tkinter.messagebox
from slitherlink.gui.field import FieldGui

from slitherlink.gui.gui_options import GUIOptions
from slitherlink.util.dashed_image_draw import DashedImageDraw
from ..gui.slitherlink import SlitherlinkGui
from PIL import ImageTk, Image


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
        self.canvasSize = (size[1][0] - size[0][0] + 2 * GUIOptions.MARGIN,
                           size[1][1] - size[0][1] + 2 * GUIOptions.MARGIN)
        self.selected: FieldGui | None = None

        for widget in self.screen.winfo_children():
            widget.destroy()

        self.canvas = tkinter.Canvas(self.screen,
                                     width=self.canvasSize[0],
                                     height=self.canvasSize[1],
                                     bg=GUIOptions.BACKGROUND_COLOR)
        self.canvas.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.exportButton = tkinter.Button(
            self.screen, text="Export", command=self.export)
        self.exportButton.grid(column=1, row=1)
        self.canvas.focus_set()
        self.screen.bind("<Button-1>", self.onClick)
        for i in range(10):
            self.canvas.bind(f"<KeyPress-{i}>", self.onNumberInputClosure(i))

    def export(self, _: tkinter.Event | None = None):
        filename = tkinter.filedialog.asksaveasfilename(parent=self.screen,
                                                        filetypes=[
                                                            ("PNG Image",
                                                             ".png"),
                                                            ("JPG Image",
                                                             ".jpeg"),
                                                            ("All Files",
                                                             ".*")
                                                        ],
                                                        title="Save as Image")
        if not filename:
            return
        idxExtension = filename.rfind('.')
        if idxExtension == -1:
            tkinter.messagebox.showerror(
                "EXPORT FAILED",
                "The export failed because no fileextension was given")
            return
        filename, extension = filename[:idxExtension], \
            filename[idxExtension:]
        if extension == ".eps":
            self.canvas.configure(bg=GUIOptions.BACKGROUND_COLOR)
            self.slitherlink.draw(self.canvas)
            self.canvas.update()
            self.canvas.postscript(
                file=filename+extension, colormode="color")
        else:
            solvedImg = Image.new("RGB", self.canvasSize,
                                  GUIOptions.BACKGROUND_COLOR)
            solvedDraw = DashedImageDraw(solvedImg)
            self.slitherlink.drawImage(solvedDraw)
            solvedImg.save(filename+extension)

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
