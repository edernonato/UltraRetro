import matplotlib
from tkinter import *
from emulator import create_emulators_list, window_type, generate_exit_button, DEFAULT_ULTRA_RETRO_PATH
from start_window import initial_screen
from handle_keys import on_key_press

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
    window.update()
    create_emulators_list()
    generate_exit_button()
    window.bind('<KeyPress>', on_key_press)
    window.mainloop()


start()
