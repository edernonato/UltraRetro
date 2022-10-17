from tkinter import *

import subprocess
import os
BACKGROUND_COLOR = "Black"


def access_emulator():
    print(f"Opening ")
    path = "/home/eder/roms/mega/"
    roms = os.listdir(path)
    print(roms)
    open_rom(roms[0])


def open_rom(rom):
    print(rom)
    os.system(f"mednafen /home/eder/roms/mega/'{rom}'")


window = Tk()
window.title("UltraRetro")
window.attributes("-fullscreen", True)
window.config(padx=0, pady=0, background=BACKGROUND_COLOR)

bg = PhotoImage(file="/home/eder/UltraRetro/UltraRetroImages/bg_img.png")
label1 = Label(window, image=bg, )
label1.place(x=0, y=0, anchor="center")


mega_drive_button = Button(fg="white", width=30, height=5, text="MEGA DRIVE", font=("Arial", 12, "italic"), highlightcolor="White", highlightthickness=0, bg="Black", command=access_emulator)
mega_drive_button.grid(row=0, column=0, columnspan=2)

snes_button = Button(fg="white", width=30, height=5, text="SUPER NINTENDO", font=("Arial", 12, "italic"), highlightcolor="White", highlightthickness=0, bg="Black", command=access_emulator)
snes_button.grid(row=1, column=0, columnspan=2)


window.mainloop()

