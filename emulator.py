import os
from tkinter import *
from functools import partial
from start_window import initial_screen


DEFAULT_ULTRA_RETRO_PATH = "/home/complex/Desktop/UltraRetro/UltraRetro"
ROMS_FOLDER = "/usr/games/roms"
EMULATOR_LIST = os.listdir(ROMS_FOLDER)
global window
DEFAULT_BG = "Images/bg_img.png"


def window_type(janela):
    global window
    global DEFAULT_BG
    window = janela
    DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")


def access_emulator(emulator, index):
    remove_widgets(window)
    path = f"{ROMS_FOLDER}/{emulator}/"
    roms = os.listdir(path)
    roms.sort()
    window.title(f"{emulator.title()} Window")
    window.geometry("1920x1080")
    window.config(padx=0, pady=0, background="Black")
    bg_game = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/{emulator}.png")
    label_mega = Label(window, image=bg_game, background="Black")
    label_mega.place(x=0, y=0, relwidth=1, relheight=1)
    final_index = index + 22
    generate_roms(roms, index, final_index, emulator)
    back_button = Button(fg="white", width=30, height=2, text="Back", font=("Arial", 8, "italic"),
                            highlightcolor="White", highlightthickness=0, bg="Black",
                            command=back_to_menu)
    back_button.grid(row=0, column=4, columnspan=2)
    generate_up_button(index, emulator)
    generate_down_button(len(roms), index, emulator)
    window.mainloop()


def generate_up_button(index, emulator):
    if index <= 21:
        up_button_clicked = None
    else:
        up_button_clicked = partial(access_emulator, emulator, index - 22)

    up_button = Button(fg="white", width=30, height=2, text="Move  Up", font=("Arial", 8, "italic"),
                       highlightcolor="White", highlightthickness=0, bg="Black", command=up_button_clicked)
    up_button.grid(row=1, column=4, columnspan=2)


def generate_down_button(len_roms, index, emulator):
    final_index = index + 22
    if len_roms > 22:
        down_button_clicked = partial(access_emulator, emulator, final_index)
    else:
        down_button_clicked = None

    down_button = Button(fg="white", width=30, height=2, text="Move Down", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=down_button_clicked)
    down_button.grid(row=2, column=4, columnspan=2)


def create_emulators(name, index):
    access = partial(access_emulator, name, 0)
    emulator_button = Button(fg="white", width=30, height=5, text=name, font=("Arial", 12, "italic"),
                             highlightcolor="White", highlightthickness=0, bg="Black", command=access)
    emulator_button.grid(row=index, column=0, columnspan=2, pady=10)


def open_rom(emulator, rom):
    os.system(f"/usr/games/mednafen {ROMS_FOLDER}/{emulator}/'{rom}'")


def generate_roms(roms, index, final_index, emulator):
    if final_index > len(roms):
        final_index = len(roms)
    for i in range(index, final_index):
        if i <= len(roms):
            chosen_rom = partial(open_rom, emulator, roms[i])
            game_button = Button(fg="white", width=50, height=2, text=roms[i], font=("Arial", 10, "italic"),
                                    highlightcolor="White", highlightthickness=0, bg="Black",
                                    command=chosen_rom)
            game_button.grid(row=i - index, column=0, columnspan=3, padx=10, pady=5)


def remove_widgets(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def back_to_menu():
    global DEFAULT_BG
    remove_widgets(window)
    initial_screen(window)
    label1 = Label(window, image=DEFAULT_BG)
    label1.place(x=0, y=0, relwidth=1, relheight=1)
    create_emulators_list()
    generate_exit_button()
    window.mainloop()


def create_emulators_list():
    for emulator in EMULATOR_LIST:
        create_emulators(emulator, EMULATOR_LIST.index(emulator))


def generate_exit_button():
    row = len(EMULATOR_LIST)
    exit_button = Button(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=window.destroy)
    exit_button.grid(row=row, column=0, columnspan=2, pady=10)
