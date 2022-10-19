import matplotlib
from tkinter import *

from emulator import create_emulators_list, window_type, generate_exit_button
from start_window import initial_screen

DEFAULT_ULTRA_RETRO_PATH = "/home/complex/Desktop/UltraRetro/UltraRetro"
matplotlib.use('Agg')
BACKGROUND_COLOR = "Black"
window = Tk()
DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")
bg = DEFAULT_BG
label1 = Label(window, image=bg)
label1.place(x=0, y=0, relwidth=1, relheight=1)


def start():
    initial_screen(window)
    window_type(window)
    create_emulators_list()
    generate_exit_button()
    window.mainloop()


start()
