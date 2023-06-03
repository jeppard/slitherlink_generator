import collections
import copy
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from slitherlink import solver
from slitherlink.gui.field import FieldGui

from slitherlink.gui.gui_options import GUIOptions
from slitherlink.gui.line import LineGui
from slitherlink.model.line_state import LineState
from slitherlink.util.dashed_image_draw import DashedImageDraw
from slitherlink.util.debug import profile
from slitherlink.util.update import setFieldLabel, setLineState
from ..gui.slitherlink import SlitherlinkGui
from PIL import ImageTk, Image


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
        tkinter.Button(self.screen, text="Back",
                       command=self.undo).grid(column=1, row=0)
        self.exportButton = tkinter.Button(
            self.screen, text="Export", command=self.export)
        self.exportButton.grid(column=1, row=1)
        self.canvas.focus_set()
        self.screen.bind("<Button-1>", self.onLeftClick)
        for i in range(10):
            self.screen.bind(f"<KeyPress-{i}>", self.onNumberInputClosure(i))
        self.canvas.bind("<KeyPress-BackSpace>", self.undo)

    def undo(self, _: tkinter.Event | None = None):
        if len(self.undoStack) > 0:
            self.slitherlink = self.undoStack.pop()
            self.draw()

    def export(self, _: tkinter.Event | None = None):
        filename = tkinter.filedialog.asksaveasfilename(parent=self.screen,
                                                        filetypes=[
                                                            ("PNG Image",
                                                             ".png"),
                                                            ("JPG Image",
                                                             ".jpeg"),
                                                            ("GIF Image",
                                                             ".gif"),
                                                            ("EPS File",
                                                             ".eps"),
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
                file=filename+"_solved"+extension, colormode="color")
            slitherlinkCopy = copy.deepcopy(self.slitherlink)
            for line in slitherlinkCopy.linelist:
                setLineState(line, LineState.UNKNOWN, slitherlinkCopy)
            self.canvas.delete('all')
            slitherlinkCopy.draw(self.canvas)
            self.canvas.update()
            self.canvas.postscript(file=filename+extension, colormode="color")
            self.draw()
        else:
            solvedImg = Image.new("RGB", self.canvasSize,
                                  GUIOptions.BACKGROUND_COLOR)
            solvedDraw = DashedImageDraw(solvedImg)
            self.slitherlink.drawImage(solvedDraw)
            solvedImg.save(filename+"_solved"+extension)
            slitherlinkCopy = copy.deepcopy(self.slitherlink)
            for line in slitherlinkCopy.linelist:
                setLineState(line, LineState.UNKNOWN, slitherlinkCopy)
            unsolvedImg = Image.new("RGB", self.canvasSize,
                                    GUIOptions.BACKGROUND_COLOR)
            unsolveDraw = DashedImageDraw(unsolvedImg)
            slitherlinkCopy.drawImage(unsolveDraw)
            unsolvedImg.save(filename+extension)

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
        @profile
        def onNumberInput(_: tkinter.Event):
            self.undoStack.append(copy.deepcopy(self.slitherlink))
            try:
                if self.selected is not None:
                    setFieldLabel(self.selected, number, self.slitherlink)
                    solver.solve(self.slitherlink)
                else:
                    clickPos = (self.screen.winfo_pointerx(),
                                self.screen.winfo_pointery())
                    pos = self.getPositionInsideCanvas(clickPos)
                    for field in self.slitherlink.fieldlist:
                        if field.isClicked(pos):
                            setFieldLabel(field, number, self.slitherlink)
                            solver.solve(self.slitherlink)
            except solver.UnsolvableError as _:
                print("Number not allowed")
                self.slitherlink = self.undoStack.pop()
            self.draw()
        return onNumberInput
