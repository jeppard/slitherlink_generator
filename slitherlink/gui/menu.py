
import tkinter
from PIL import ImageTk
from slitherlink.editor.editor import EditorGui

from slitherlink.generators.generator import SlitherlinkGenerator
from slitherlink.model.forms import OuterForm, SlitherlinkForm
from .gui_options import GUIOptions


class Menu():
    def __init__(self, screen: tkinter.Canvas,
                 images: dict[str, ImageTk.PhotoImage]) -> None:
        self.screen = screen
        self.images = images
        self.valInt = self.screen.register(self.validateInt)
        self.inc = self.screen.register(self.increment)
        self.dec = self.screen.register(self.decrement)
        self.upperbound = 99
        self.lowerbound = 1
        self.vCmdInt = (self.screen.register(self.validateInt), '%P')

        self.slitherlinkForm = SlitherlinkForm.SQUARE
        self.outerForm = OuterForm.RECTANGLE

        self.sizeX = tkinter.IntVar(self.screen, 1)
        self.sizeY = tkinter.IntVar(self.screen, 1)

    def generateSlitherlink(self):
        slitherlink = SlitherlinkGenerator.generate(
            self.slitherlinkForm,
            (self.sizeX.get(), self.sizeY.get()),
            self.outerForm)
        editor = EditorGui(slitherlink, self.images, self.screen)
        editor.draw()

    def validateInt(self, inp: int) -> bool:
        try:
            return self.lowerbound <= int(inp) <= self.upperbound
        except ValueError:
            return False

    @staticmethod
    def increment(variable: tkinter.IntVar, upperbound: int) -> None:
        if variable.get() + 1 <= upperbound:
            variable.set(variable.get() + 1)

    @staticmethod
    def decrement(variable: tkinter.IntVar, lowerbound: int) -> None:
        if variable.get() - 1 >= lowerbound:
            variable.set(variable.get() - 1)

    def mainMenu(self, prev: list[callable] = None):
        if prev is None:
            prev = [lambda: None]
        for widget in self.screen.winfo_children():
            widget.destroy()

        # Überschrift
        tkinter.Label(self.screen, image=self.images['Empty_1x4'],
                      font=GUIOptions.MENU_FONT,
                      **GUIOptions.MENU_COMMON_OPTIONS).grid(row=0, column=0)
        tkinter.Label(self.screen, text='Rundweg Generator',
                      font=GUIOptions.MENU_FONT,
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=0, column=0, pady=(26, 0))

        # Buttons
        tkinter.Button(self.screen, image=self.images['Neuer_Rundweg'],
                       command=lambda: self.neuerRundweg(
                           prev + [self.mainMenu]),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=1, column=0)

    def neuerRundweg(self, prev: list[callable] = None):
        if prev is None:
            prev = [lambda: None]
        for widget in self.screen.winfo_children():
            widget.destroy()

        # Überschrift
        tkinter.Label(self.screen, image=self.images['Empty_1x4']).grid(
            row=0, column=0)
        tkinter.Label(self.screen, text='Form auswählen',
                      font=GUIOptions.MENU_FONT,
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=0, column=0, padx=(26, 0))

        # Buttons
        tkinter.Button(self.screen, image=self.images['Quadratisch'],
                       command=lambda: self.getSizeSquare(
                           prev + [self.neuerRundweg]),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=1, column=0)
        tkinter.Button(self.screen, image=self.images['Sechseck'],
                       command=(lambda: self.getSizeSechseck(
                           prev + [self.neuerRundweg])),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=2, column=0)
        tkinter.Button(self.screen, image=self.images['Dreieckig'],
                       command=(lambda: self.getSizeDreieck(
                           prev + [self.neuerRundweg])),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=3, column=0)

        # Zurück
        tkinter.Button(self.screen, image=self.images['Zurück'],
                       command=lambda: prev[-1](prev[:-1]),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=4, column=0, pady=(20, 0))

    def getSizeCommon(self, prev):
        for widget in self.screen.winfo_children():
            widget.destroy()

        # Überschrift
        tkinter.Label(self.screen, image=self.images['Empty_1x4']
                      ).grid(row=0, column=0, columnspan=3)
        tkinter.Label(self.screen, text='Größe eingeben',
                      font=GUIOptions.MENU_FONT,
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=0, column=0, padx=(26, 0), columnspan=3)

        # Weiter
        tkinter.Button(self.screen, image=self.images['Weiter'],
                       command=self.generateSlitherlink,
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=4,
                              column=0,
                              columnspan=3)
        # Zurück
        tkinter.Button(self.screen, image=self.images['Zurück'],
                       command=lambda: prev[-1](prev[:-1]),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=5,
                              column=0,
                              columnspan=3)

    def getSizeRechteck(self, prev):
        self.getSizeCommon(prev)
        self.outerForm = OuterForm.RECTANGLE
        # Linke Seite
        tkinter.Label(self.screen, image=self.images['Entry'],
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=2, column=0)
        tkinter.Entry(self.screen, textvariable=self.sizeX,
                      font=GUIOptions.MENU_FONT, justify='center', width=2,
                      validate='key',
                      validatecommand=self.vCmdInt,
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=2, column=0)

        tkinter.Button(self.screen, image=self.images['Pfeil_hoch'],
                       command=lambda: self.increment(self.sizeX, 99),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=1, column=0)
        tkinter.Button(self.screen, image=self.images['Pfeil_runter'],
                       command=lambda: self.decrement(self.sizeX, 1),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=3, column=0)

        # Mitte
        tkinter.Label(self.screen, image=self.images['X'],
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=2, column=1)

        # Rechte Seite
        tkinter.Label(self.screen, image=self.images['Entry'],
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=2, column=2)
        tkinter.Entry(self.screen, textvariable=self.sizeY,
                      font=GUIOptions.MENU_FONT, justify='center', width=2,
                      validate='key', validatecommand=self.vCmdInt,
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=2, column=2)

        tkinter.Button(self.screen, image=self.images['Pfeil_hoch'],
                       command=lambda: self.increment(self.sizeY, 99),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=1, column=2)
        tkinter.Button(self.screen, image=self.images['Pfeil_runter'],
                       command=lambda: self.decrement(self.sizeY, 1),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=3, column=2)

    def getSizeDreieck(self, prev):
        self.slitherlinkForm = SlitherlinkForm.TRIANGLE
        self.getSizeRechteck(prev)

    def getSizeSquare(self, prev):
        self.slitherlinkForm = SlitherlinkForm.SQUARE
        self.getSizeRechteck(prev)

    def getSizeSechseck(self, prev, isOuterFormWabe=True):
        self.slitherlinkForm = SlitherlinkForm.HEXAGON
        if (isOuterFormWabe):
            self.outerForm = OuterForm.SLITHERLINK_FORM
        else:
            self.outerForm = OuterForm.RECTANGLE

        for widget in self.screen.winfo_children():
            widget.destroy()

        # Überschrift
        tkinter.Label(self.screen, image=self.images['Empty_1x4'],
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=0, column=0, columnspan=3)
        tkinter.Label(self.screen, text='Größe eingeben',
                      font=GUIOptions.MENU_FONT,
                      **GUIOptions.MENU_COMMON_OPTIONS
                      ).grid(row=0, column=0, padx=(26, 0), columnspan=3)

        # Form auswählen
        tkinter.Button(self.screen, image=self.images['Sechseck_Wabe'],
                       command=lambda:
                       None if isOuterFormWabe else self.getSizeSechseck(prev),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=1, column=0, sticky='E')
        tkinter.Button(self.screen, image=self.images['Sechseck_Rechteck'],
                       command=lambda: self.getSizeSechseck(
                           prev, False) if isOuterFormWabe else None,
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=1, column=2, sticky='W')

        # Wabe Ausgewählt
        if isOuterFormWabe:
            # Entry
            tkinter.Label(self.screen, image=self.images['Entry'],
                          **GUIOptions.MENU_COMMON_OPTIONS
                          ).grid(row=3, column=1)
            tkinter.Entry(self.screen, textvariable=self.sizeX, width=2,
                          font=GUIOptions.MENU_FONT, justify='center',
                          validate='key',
                          validatecommand=self.vCmdInt,
                          **GUIOptions.MENU_COMMON_OPTIONS
                          ).grid(row=3, column=1)

            # Hoch/Runter
            tkinter.Button(self.screen, image=self.images['Pfeil_hoch'],
                           command=lambda: self.increment(self.sizeX, 99),
                           **GUIOptions.MENU_COMMON_OPTIONS
                           ).grid(row=2, column=1)
            tkinter.Button(self.screen, image=self.images['Pfeil_runter'],
                           command=lambda: self.decrement(self.sizeX, 1),
                           **GUIOptions.MENU_COMMON_OPTIONS
                           ).grid(row=4, column=1)

        else:  # Rechteck
            # Linke Seite
            tkinter.Label(self.screen, image=self.images['Entry'],
                          **GUIOptions.MENU_COMMON_OPTIONS
                          ).grid(row=3, column=0)
            tkinter.Entry(self.screen, textvariable=self.sizeX,
                          font=GUIOptions.MENU_FONT, justify='center', width=2,
                          validate='key',
                          validatecommand=self.vCmdInt,
                          **GUIOptions.MENU_COMMON_OPTIONS
                          ).grid(row=3, column=0)

            tkinter.Button(self.screen, image=self.images['Pfeil_hoch'],
                           command=lambda: self.increment(self.sizeX, 99),
                           **GUIOptions.MENU_COMMON_OPTIONS
                           ).grid(row=2, column=0)
            tkinter.Button(self.screen, image=self.images['Pfeil_runter'],
                           command=lambda: self.decrement(self.sizeX, 1),
                           **GUIOptions.MENU_COMMON_OPTIONS
                           ).grid(row=4, column=0)

            # Mitte
            tkinter.Label(self.screen, image=self.images['X'],
                          **GUIOptions.MENU_COMMON_OPTIONS
                          ).grid(row=3, column=1)

            # Rechte Seite
            tkinter.Label(self.screen, image=self.images['Entry'],
                          **GUIOptions.MENU_COMMON_OPTIONS
                          ).grid(row=3, column=2)
            tkinter.Entry(self.screen, textvariable=self.sizeY,
                          font=GUIOptions.MENU_FONT, justify='center', width=2,
                          validate='key',
                          validatecommand=self.vCmdInt,
                          **GUIOptions.MENU_COMMON_OPTIONS
                          ).grid(row=3, column=2)

            tkinter.Button(self.screen, image=self.images['Pfeil_hoch'],
                           command=lambda: self.increment(self.sizeY, 99),
                           **GUIOptions.MENU_COMMON_OPTIONS
                           ).grid(row=2, column=2)
            tkinter.Button(self.screen, image=self.images['Pfeil_runter'],
                           command=lambda: self.decrement(self.sizeY, 1),
                           **GUIOptions.MENU_COMMON_OPTIONS,
                           ).grid(row=4, column=2)

        # Weiter
        if isOuterFormWabe:
            tkinter.Button(self.screen, image=self.images['Weiter'],
                           command=self.generateSlitherlink,
                           **GUIOptions.MENU_COMMON_OPTIONS
                           ).grid(row=5, column=0, columnspan=3)
        else:
            tkinter.Button(self.screen, image=self.images['Weiter'],
                           command=self.generateSlitherlink,
                           **GUIOptions.MENU_COMMON_OPTIONS
                           ).grid(row=5, column=0, columnspan=3)
        # Zurück
        tkinter.Button(self.screen, image=self.images['Zurück'],
                       command=lambda: prev[-1](prev[:-1]),
                       **GUIOptions.MENU_COMMON_OPTIONS
                       ).grid(row=6, column=0, columnspan=3)
