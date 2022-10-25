import os
from tkinter import *
from functools import partial
from start_window import initial_screen
from PIL import Image, ImageTk
from threading import Thread


DEFAULT_ULTRA_RETRO_PATH = "/home/complex/Desktop/UltraRetro/UltraRetro"
ROMS_FOLDER = "/usr/games/roms"
Applications = {"Mednafen": ["Mega Drive", "Super Nintendo", "Nintendo"], "PCSXR": "Playstation"}
EMULATOR_LIST = os.listdir(ROMS_FOLDER)
global window
global buttons
global label_images
global current_index
global roms
global current_rom
global final_index
global overlay_img
global DEFAULT_BG
current_rom_focus = None
current_focus = None


def window_type(janela):
    global window
    global DEFAULT_BG
    global label_images
    global current_index
    window = janela
    label_images = {}
    current_index = 1
    DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")


def create_emulators_list():
    for emulator in EMULATOR_LIST:
        create_emulators(emulator, EMULATOR_LIST.index(emulator))


def create_emulators(name, index):
    global current_index
    current_index = 0
    access = partial(access_emulator, name, 0)
    emulator_button = Button(fg="white", width=30, height=5, text=name, font=("Arial", 12, "italic"),
                             highlightcolor="White", highlightthickness=0, bg="Black", command=access)
    emulator_button.grid(row=index, column=0, columnspan=2, pady=10)
    move_focus_down()


def access_emulator(emulator, index):
    global roms
    global current_index
    global final_index
    current_index = 0
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
    move_focus_down()
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
    global final_index
    final_index = index + 22
    if len_roms > 22:
        down_button_clicked = partial(access_emulator, emulator, final_index)
    else:
        down_button_clicked = None

    down_button = Button(fg="white", width=30, height=2, text="Move Down", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=down_button_clicked)
    down_button.grid(row=2, column=4, columnspan=2)


def open_rom(emulator, rom):
    if emulator in Applications["Mednafen"]:
        os.system(f"/usr/games/mednafen '{ROMS_FOLDER}/{emulator}/{rom}'")
    elif emulator in Applications['PCSXR']:
        os.system(f"/usr/games/pcsxr -nogui -cdfile '{ROMS_FOLDER}/{emulator}/{rom}'")
    close_overlay()


def open_overlay(emulator, rom):
    global overlay_img
    global DEFAULT_ULTRA_RETRO_PATH
    global window         
    image1 = Image.open(f"{DEFAULT_ULTRA_RETRO_PATH}/Images/Games/overlay/7th Saga, The (USA).png")
    img = ImageTk.PhotoImage(image1)
    overlay_img = Label(image=img)
    overlay_img.place(x=0, y=0)
    func1 = partial(open_rom, emulator, rom)    
    Thread(target=func1).start()
    Thread(target=window.mainloop()).start()


def close_overlay():
    global overlay_img
    overlay_img.destroy()
    move_focus_down()
    move_focus_up()


def generate_roms(rom_games, index, final_index_roms, emulator):
    global buttons
    global current_rom_focus
    global final_index
    final_index = final_index_roms
    if final_index > len(rom_games):
        final_index = len(rom_games)
    buttons = {}
    for i in range(index, final_index):
        if i <= len(rom_games):
            chosen_rom = partial(open_overlay, emulator, rom_games[i])
            buttons[rom_games[i]] = Button(fg="white", width=50, height=2, text=rom_games[i],
                                           font=("Arial", 10, "italic"), highlightcolor="White",
                                           highlightthickness=0, bg="Black", command=chosen_rom,
                                           activeforeground="Red", cursor="man", takefocus=1)
            buttons[rom_games[i]].grid(row=i - index, column=0, columnspan=3, padx=10, pady=5)

    buttons[rom_games[index]].focus()
    current_rom_focus = buttons[rom_games[index]]


def move_focus_down():
    global current_index
    global DEFAULT_ULTRA_RETRO_PATH
    button = window.winfo_children()[current_index]
    button.configure(bg="Black")
    if current_index >= len(window.winfo_children()) - 1:
        current_index = 1
        button = window.winfo_children()[current_index]
    else:
        current_index += 1
        button = window.winfo_children()[current_index]

    # noinspection PyBroadException
    try:
        button.focus_force()
        button_text = button.cget('text')
        button_text = button_text.replace(".zip", ".png")
        image1 = Image.open(f"{DEFAULT_ULTRA_RETRO_PATH}/Images/Games/{button_text}")
        img = ImageTk.PhotoImage(image1)
    except Exception:
        img = ""

    button.configure(bg="Red")
    return display_game_img(img)


def move_focus_up():
    global current_index
    global DEFAULT_ULTRA_RETRO_PATH
    display_game_img("")
    button = window.winfo_children()[current_index]
    button.configure(bg="Black")
    if current_index <= 1:
        current_index = len(window.winfo_children()) - 1
        button = window.winfo_children()[current_index]
    else:
        current_index -= 1
        button = window.winfo_children()[current_index]
    # noinspection PyBroadException
    try:
        button.focus_force()
        button_text = button.cget('text')
        button_text = button_text.replace(".zip", ".png")
        image1 = Image.open(f"{DEFAULT_ULTRA_RETRO_PATH}/Images/Games/{button_text}")
        img = ImageTk.PhotoImage(image1)
    except Exception:
        img = ""

    button.configure(bg="Red")
    return display_game_img(img)


def display_game_img(image):
    global label_images
    for values in label_images.values():
        values.destroy()

    if image == '':
        for values in label_images.values():
            values.destroy()
        return
    global window
    label_image = Label(image=image)
    label_image.place(x=700, y=150)
    label_images[image] = label_image
    window.mainloop()


def remove_widgets(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def back_to_menu():
    global DEFAULT_BG
    global current_index
    current_index = 0
    remove_widgets(window)
    initial_screen(window)
    label1 = Label(window, image=DEFAULT_BG)
    label1.place(x=0, y=0, relwidth=1, relheight=1)
    create_emulators_list()
    generate_exit_button()
    window.mainloop()


def generate_exit_button():
    row = len(EMULATOR_LIST)
    exit_button = Button(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=window.destroy)
    exit_button.grid(row=row, column=0, columnspan=2, pady=10)
