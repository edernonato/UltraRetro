import matplotlib
from tkinter import *
from PIL import Image
from emulator import create_emulators_list, window_type
from start_window import initial_screen, generate_exit_button

im = Image.open('Images/bg_img.png')
im.show()

matplotlib.use('Agg')
BACKGROUND_COLOR = "Black"
window = Tk()
DEFAULT_BG = PhotoImage(file="Images/bg_img.png")
bg = DEFAULT_BG
label1 = Label(window, image=bg)
label1.place(x=0, y=0, relwidth=1, relheight=1)


def start():
    initial_screen(window)
    window_type(window)
    create_emulators_list()
    generate_exit_button(window)
    window.mainloop()


start()
