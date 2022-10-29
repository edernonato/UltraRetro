import os
from tkinter import *
from functools import partial
from start_window import initial_screen
from PIL import Image, ImageTk
from threading import Thread
import pathlib
from tkvideo import tkvideo
import random


global window
global buttons
global label_images
global current_index
global final_index
global roms
global overlay_img
global DEFAULT_BG
global joystick
global emulator_clicked
global text_label
global video_label
global emulator_current_focus

DEFAULT_ULTRA_RETRO_PATH = pathlib.Path(__file__).parent.resolve()
ROMS_FOLDER = "/usr/games/roms"
# ROMS_FOLDER = "G:/roms/UltraRetro"
Applications = {"Mednafen": ["Mega Drive", "Super Nintendo", "Nintendo", "Game Boy Advance"], "PCSXR": "Playstation"}
EMULATOR_LIST = os.listdir(ROMS_FOLDER)
current_rom_focus = None
current_focus = None


def window_type(janela, control):
    global window
    global DEFAULT_BG
    global label_images
    global current_index
    global joystick
    joystick = control
    window = janela
    label_images = {}
    current_index = 1
    DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")


def update_application():
    cmd = partial(os.system, f"echo LOGINPASSWD | sudo -S {DEFAULT_ULTRA_RETRO_PATH}/gitpull.sh")
    button_img = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/update_button.png")
    update_button = Button(fg="Red", width=270, height=100, text="Update", highlightcolor="White",
                           bg="Black", image=button_img, borderwidth=0, command=cmd, compound=LEFT)
    update_button.grid(row=0, column=3, columnspan=2, padx=10, pady=10)
    window.mainloop()


def create_emulators_list():
    for emulator in EMULATOR_LIST:
        create_emulators(emulator, EMULATOR_LIST.index(emulator))


def create_emulators(name, index):
    global current_index
    global emulator_clicked
    emulator_clicked = name
    current_index = 0
    access = partial(access_emulator, name, 0)
    emulator_button = Button(fg="white", width=30, height=5, text=name, font=("Arial", 12, "italic"),
                             highlightcolor="White", highlightthickness=0, bg="Black", command=access)
    emulator_button.grid(row=index, column=0, columnspan=2, pady=10)
    move_focus_down()


def generate_video_label():
    global video_label
    global window
    global ROMS_FOLDER
    global emulator_current_focus
    # noinspection PyBroadException
    try:
        remove_video_label()
    except Exception:
        pass
    # noinspection PyBroadException
    try:
        video_label = Label()
        video_label.place(x=600, y=200)
        games = os.listdir(f"{ROMS_FOLDER}/{emulator_current_focus}/videos")
        game_index = random.randint(0, len(games) - 1)
        player = tkvideo(f"{ROMS_FOLDER}/{emulator_current_focus}/videos/{games[game_index]}", video_label, loop=1,
                         size=(800, 600))
        player.play()
        window.after(3000, generate_video_label)
    except Exception:
        pass


def remove_video_label():
    global video_label
    video_label.destroy()


def generate_text_label(emulator_focus):
    global text_label
    global video_label
    global ROMS_FOLDER
    global emulator_current_focus
    emulator_current_focus = emulator_focus
    if window.title() == "UltraRetro":
        games = os.listdir(f"{ROMS_FOLDER}/{emulator_focus}")
        text_label = Label(text=f"{emulator_focus}: {len(games)} Games", fg="white", width=100, height=5,
                           font=("Arial", 12, "italic"), highlightcolor="Black", highlightthickness=5, bg="Brown",
                           highlightbackground="Purple")
        text_label.place(x=550, y=900)
    generate_video_label()


def remove_text_label():
    global text_label
    global video_label
    # noinspection PyBroadException
    try:
        text_label.destroy()
    except Exception:
        pass
    # noinspection PyBroadException
    try:
        remove_video_label()
    except Exception:
        pass


def access_emulator(emulator, index):
    global roms
    global current_index
    global final_index
    global window
    global joystick
    global emulator_clicked
    emulator_clicked = emulator
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
    final_index = index + 20
    generate_roms(roms, index, final_index, emulator)

    # Button created for testing
    user = os.popen('whoami').read()
    new_button = Button(fg="white", width=30, height=2, text=f"{user}", font=("Arial", 12, "italic"),
                        highlightcolor="White", highlightthickness=0, bg="Black", takefocus=0)
    new_button.grid(row=0, column=5)

    joystick.update_emulator_index(len(roms), emulator, final_index)
    move_focus_down()
    joystick.update_root(window)
    window.mainloop()


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
    window.focus_force()
    joystick.update_root(window)


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
    global window
    global current_index
    global emulator_clicked
    global final_index
    remove_text_label()
    button = window.winfo_children()[current_index]
    button.configure(bg="Black", highlightbackground='Black', highlightthickness=0)
    if current_index >= len(window.winfo_children()) - 1:
        if window.title() != "UltraRetro" and len(roms) > 20:
            access_emulator(emulator_clicked, final_index)
        current_index = 1
        button = window.winfo_children()[current_index]
    else:
        current_index += 1
        button = window.winfo_children()[current_index]
    if isinstance(button, Label):
        move_focus_down()
    # noinspection PyBroadException
    try:
        button.focus_force()
        button_text = button.cget('text')
        button_text_formatted = format_image_file_name(button_text)
        image1 = Image.open(f"{button_text_formatted}")
        img = ImageTk.PhotoImage(image1)
    except Exception:
        img = ""
    button.configure(bg="Red", highlightbackground='Yellow', highlightthickness=5, highlightcolor="Purple")
    generate_text_label(button.cget('text'))
    display_game_img(img)


def move_focus_up():
    global current_index
    global emulator_clicked
    remove_text_label()
    display_game_img("")
    button = window.winfo_children()[current_index]
    button.configure(bg="Black", highlightbackground='Black', highlightthickness=0)
    if current_index <= 1:
        if window.title() != "UltraRetro" and len(roms) > 20:
            access_emulator(emulator_clicked, final_index - 40)
            current_index = len(window.winfo_children())
        else:
            current_index = len(window.winfo_children()) - 1
    else:
        current_index -= 1
    button = window.winfo_children()[current_index]
    # noinspection PyBroadException
    try:
        button.focus_force()
        button_text = button.cget('text')
        button_text_formatted = format_image_file_name(button_text)
        image1 = Image.open(f"{button_text_formatted}")
        img = ImageTk.PhotoImage(image1)
    except Exception:
        pass
        img = ""
    button.configure(bg="Red", highlightbackground='Yellow', highlightthickness=5, highlightcolor="Purple")
    generate_text_label(button.cget('text'))
    display_game_img(img)


def format_image_file_name(image_text):
    global ROMS_FOLDER
    global emulator_clicked
    image_name_formatted = f"{ROMS_FOLDER}/{emulator_clicked}/images/"
    button_text_list = image_text.split(".")
    for word in range(len(button_text_list) - 1):
        if word != button_text_list[len(button_text_list) - 1]:
            image_name_formatted += button_text_list[word] + "."
    return image_name_formatted + "png"


def display_game_img(image):
    global label_images
    global window
    global emulator_clicked
    global final_index
    for values in label_images.values():
        values.destroy()

    if image == '':
        for values in label_images.values():
            values.destroy()
        return

    label_image = Label(image=image)
    label_image.place(x=600, y=200)
    label_images[image] = label_image
    joystick.update_root(window)
    window.mainloop()


def remove_widgets(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def back_to_menu():
    global DEFAULT_BG
    global current_index
    global emulator_current_focus
    current_index = 0
    remove_widgets(window)
    initial_screen(window)
    label1 = Label(window, image=DEFAULT_BG)
    label1.place(x=0, y=0, relwidth=1, relheight=1)
    create_emulators_list()
    generate_exit_button()
    generate_text_label(emulator_current_focus)
    joystick.update_root(window)
    update_application()
    window.mainloop()


def generate_exit_button():
    row = len(EMULATOR_LIST)
    exit_button = Button(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=window.destroy)
    exit_button.grid(row=row, column=0, columnspan=2, pady=10)
