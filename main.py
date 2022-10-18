from tkinter import *
import matplotlib
import os
from functools import partial

matplotlib.use('Agg')
BACKGROUND_COLOR = "Black"
window = Tk()


def access_emulator(emulator):
    path = f"/usr/games/roms/{emulator}/"
    roms = os.listdir(path)
    window.destroy()
    game_window = Tk()
    game_window.title("Emulator Window")
    game_window.geometry("1920x1080")
    game_window.config(padx=0, pady=0, background="Black")
    bg = PhotoImage(file=f"Images/{emulator}.png")
    label_mega = Label(game_window, image=bg, background="Black")
    label_mega.place(x=0, y=0, relwidth=1, relheight=1)
    for index in range(len(roms)):
        chosen_rom = partial(open_rom, emulator, roms[index])
        game_button = Button(fg="white", width=30, height=5, text=roms[index], font=("Arial", 8, "italic"),
                                highlightcolor="White", highlightthickness=0, bg="Black",
                                command=chosen_rom)
        game_button.grid(row=index, column=0, columnspan=2)

    exit_button = Button(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                            highlightcolor="White", highlightthickness=0, bg="Black",
                            command=lambda: [game_window.destroy(), create_window(), initial_screen()])
    exit_button.grid(row=len(roms) + 1, column=0, columnspan=2)
    game_window.mainloop()


def open_rom(emulator, rom):
    os.system(f"mednafen /usr/games/roms/{emulator}/'{rom}'")


def listing_roms(rom):
    print(rom)


def create_window():
    global window
    window = Tk()


def initial_screen():
    bg = PhotoImage(file="Images/bg_img.png")
    window.title("UltraRetro")
    window.geometry("1920x1080")
    window.config(padx=0, pady=0, background="White")
    label1 = Label(window, image=bg)
    label1.place(x=0, y=0, relwidth=1, relheight=1)

    access_mega = partial(access_emulator, 'mega')

    mega_drive_button = Button(fg="white", width=30, height=5, text="MEGA DRIVE", font=("Arial", 12, "italic"),
                               highlightcolor="White", highlightthickness=0, bg="Black", command=access_mega)
    mega_drive_button.grid(row=0, column=0, columnspan=2)

    access_snes = partial(access_emulator, 'snes')
    snes_button = Button(fg="white", width=30, height=5, text="SUPER NINTENDO", font=("Arial", 12, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black", command=access_snes)
    snes_button.grid(row=1, column=0, columnspan=2)
    exit_button = Button(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=window.destroy)
    exit_button.grid(row=2, column=0, columnspan=2)

    window.mainloop()


initial_screen()

