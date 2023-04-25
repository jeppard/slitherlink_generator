
from slitherlink.gui.field import FieldGui
from slitherlink.gui.gui_options import GUIOptions
from slitherlink.gui.line import LineGui
from slitherlink.gui.menu import Menu
from slitherlink.gui.point import PointGui
import tkinter
import os


from slitherlink.model.line_state import LineState
from PIL import ImageTk, Image

ICONS = ['Entry', 'X', 'Pfeil_hoch', 'Pfeil_runter', 'Sechseck_Rechteck',
         'Sechseck_Wabe', 'Empty_1x4', 'Grid', 'Freihand', 'Import',
         'Neuer_Rundweg', 'Quadratisch', 'Sechseck', 'Weiter', 'Zurück']


def run():
    root = tkinter.Tk()
    root.configure(background=GUIOptions.BACKGROUND_COLOR)
    images = {
        icon: ImageTk.PhotoImage(image=Image.open(os.path.join(
            os.path.dirname(__file__), "img", f"{icon}.gif")))
        for icon in ICONS
    }
    menu = Menu(screen=root, images=images)
    menu.mainMenu()
    root.mainloop()
