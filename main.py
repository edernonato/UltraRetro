import matplotlib
from tkinter import *
from pynput import keyboard

from emulator import create_emulators_list, window_type, generate_exit_button, move_focus_down, move_focus_up
from start_window import initial_screen

DEFAULT_ULTRA_RETRO_PATH = "/home/Eder/Desktop/UltraRetro/UltraRetro"
matplotlib.use('Agg')
BACKGROUND_COLOR = "Black"
window = Tk()
DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")
bg = DEFAULT_BG
label1 = Label(window, image=bg)
label1.place(x=0, y=0, relwidth=1, relheight=1)


# Using onKeyEvent to navigate on the game list, still need refactor
def onKeyPress(event):
    # print('end', 'You pressed %s\n' % (event.char,))
    if event.char.lower() == "s":
        move_focus_down()
    elif event.char.lower() == "w":
        move_focus_up()


def start():
    initial_screen(window)
    window_type(window)
    create_emulators_list()
    generate_exit_button()
    window.bind('<KeyPress>', onKeyPress)
    window.mainloop()

start()
