import matplotlib
from tkinter import *
from emulator import create_emulators_list, window_type, generate_exit_button, update_application,\
    DEFAULT_ULTRA_RETRO_PATH
from start_window import initial_screen
from handle_keys import on_key_press
from controller import JoystickControllers


matplotlib.use('Agg')
BACKGROUND_COLOR = "Black"
window = Tk()
DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/Nintendo.png")
bg = DEFAULT_BG
label1 = Label(window, image=bg)
label1.place(x=0, y=0, relwidth=1, relheight=1)


def start():
    initial_screen(window)
    joysticks = JoystickControllers(window)
    window_type(window, joysticks)
    window.update()
    window.bind('<KeyPress>', on_key_press)
    create_emulators_list()
    generate_exit_button()
    update_application()
    window.mainloop()


start()

