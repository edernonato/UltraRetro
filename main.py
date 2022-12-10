import matplotlib
from tkinter import *
from emulator_class import Emulator
from start_window import initial_screen
from controller import JoystickControllers
import os


matplotlib.use('Agg')
BACKGROUND_COLOR = "Black"


def start():
    window = Tk()
    initial_screen(window)
    os.system("pulseaudio -D")
    emulator = Emulator(window)
    joysticks = JoystickControllers(window, emulator)
    default_bg = PhotoImage(file=f"{emulator.DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")
    bg = default_bg
    label1 = Label(window, image=bg)
    label1.place(x=0, y=0, relwidth=1, relheight=1)
    emulator.window_type(window, joysticks)
    window.update()
    window.bind('<KeyPress>', joysticks.on_key_press)
    emulator.create_emulators_list(0)
    emulator.update_application()
    window.mainloop()


start()
