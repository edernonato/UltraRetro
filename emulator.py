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
global video_frame
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
global buttons_frame
global emulators_list_index
global exit_button


DEFAULT_ULTRA_RETRO_PATH = pathlib.Path(__file__).parent.resolve()
ROMS_FOLDER = "/usr/games/roms"
# ROMS_FOLDER = "G:/roms/UltraRetro"

Applications = {"Mednafen": ["Mega Drive", "Nintendo", "Game Boy Advance", "Game Boy Color", "Super Nintendo",
                             "Playstation", "Master System", "Atari Lynx", "Sega Game Gear", "WonderSwan",
                             "Sega Saturn"], "PCSXR": "Playstation", "Snes9x EX": "Super Nintendo"}

mednafen_emulators_name = {"Playstation": ["psx", ".yscale 4.6", ".xscale 4.65"],
                           "Mega Drive": ["md", ".yscale 4.85", ".xscale 5.09"],
                           "Nintendo": ["nes", ".yscale 4.85", ".xscale 5.75"],
                           "Game Boy Advance": ["gba", ".yscale 6.75", ".xscale 6.75"],
                           "Game Boy Color": ["gb", ".yscale 7.5", ".xscale 10.15"],
                           "Super Nintendo": ["snes", ".yscale 4.85", ".xscale 5.79"],
                           "Master System": ["ss", ".yscale 10.75", ".xscale 10.75"],
                           "Atari Lynx": ["lynx", ".yscale 9.9", ".xscale 10.0"],
                           "Sega Game Gear": ["gg", ".yscale 7.3", ".xscale 9.0"],
                           "WonderSwan": ["wswan", ".yscale 7.3", ".xscale 9.0"],
                           "Sega Saturn": ["ss", ".yscale 7.3", ".xscale 9.0"]}

emulator_rom_extensions = {"Playstation": ["cue"], "Mega Drive": ["zip"], "Nintendo": ["zip", "nes"],
                           "Game Boy Advance": ["zip", "gba"], "Game Boy Color": ["zip"],
                           "Super Nintendo": ["zip"], "Master System": ["zip"], "Atari Lynx": ["zip"],
                           "Sega Game Gear": ["zip"], "WonderSwan": ["zip"], "Sega Saturn": ["chd"]}
EMULATOR_LIST = os.listdir(ROMS_FOLDER)
EMULATOR_LIST.sort()
current_rom_focus = None
current_focus = None


def controller_config(controller_number):
    global joystick
    global window
    joystick.assign_buttons(joystick.button_list_to_assign, controller_number)
    back_to_menu()


def window_type(janela, control):
    global window
    global DEFAULT_BG
    global label_images
    global current_index
    global joystick
    global buttons_frame
    joystick = control
    window = janela
    DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")
    buttons_frame_start()
    label_images = {}
    current_index = 1


def buttons_frame_start():
    global buttons_frame
    global DEFAULT_BG
    # noinspection PyBroadException
    try:
        remove_widgets(buttons_frame)
        # buttons_frame.destroy()
    except Exception:
        pass
    buttons_frame = Frame(window)
    bg = DEFAULT_BG
    frame_label_image = Label(buttons_frame, image=bg)
    frame_label_image.place(x=0, y=0, relwidth=1, relheight=1)


def update_application():
    cmd = partial(os.system, f"echo LOGINPASSWD | sudo -S {DEFAULT_ULTRA_RETRO_PATH}/gitpull.sh")
    button_img = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/update_button.png")
    update_button = Button(fg="Red", width=270, height=100, text="Update", highlightcolor="White",
                           bg="Black", image=button_img, borderwidth=0, command=cmd, compound=LEFT)
    # update_button.grid(row=0, column=4, columnspan=2, padx=10, pady=10)
    update_button.place(x=1600, y=20)
    window.mainloop()


def create_emulators_list(index):
    global emulators_list_index
    global buttons_frame
    max_index = len(EMULATOR_LIST) - 1
    buttons_frame_start()
    if index < -8:
        index = index + 11

    emulators_list_index = index + 8
    counter = 0
    for emulator in range(index, emulators_list_index):
        if counter >= 8:
            print("COUNTER > 7")
        else:
            if emulator <= max_index:
                create_emulators(EMULATOR_LIST[emulator], counter)
            else:
                emulators_list_index = (emulator - 1) - max_index
                create_emulators(EMULATOR_LIST[emulators_list_index], counter)
                emulators_list_index = emulator - max_index
                # generate_exit_button()
        counter += 1
        # for emulator in EMULATOR_LIST:
        #     create_emulators(emulator, EMULATOR_LIST.index(emulator))


def create_emulators(name, index):
    global current_index
    global emulator_clicked
    global emulator_current_focus
    global window
    global buttons_frame
    emulator_clicked = name
    current_index = -1
    access = partial(access_emulator, name, 0)
    buttons_frame.grid(row=0, column=0)
    emulator_button = Button(buttons_frame)
    emulator_button.configure(fg="white", width=30, height=5, text=name, font=("Arial", 12, "italic"),
                              highlightcolor="White", highlightthickness=0, bg="Black", command=access)
    emulator_button.grid(row=index, column=0, columnspan=2, pady=10)
    emulator_current_focus = emulator_button
    move_focus_down()


def generate_video_label():
    # return
    global video_frame
    global window
    global ROMS_FOLDER
    global emulator_current_focus
    global video_label
    # noinspection PyBroadException
    try:
        remove_video_label()
    except Exception:
        pass
    # noinspection PyBroadException
    try:
        video_frame = Frame(window)
        video_label = Label(video_frame)
        video_frame.place(x=600, y=200)
        video_label.grid(row=0, column=0)
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
    global video_frame
    # noinspection PyBroadException
    try:
        # video_frame.place_forget()
        # video_label.grid_forget()
        video_frame.destroy()
    except Exception:
        pass


def generate_text_label(emulator_focus):
    global text_label
    global video_label
    global ROMS_FOLDER
    global emulator_current_focus
    emulator_current_focus = emulator_focus
    if window.title() == "UltraRetro":
        # noinspection PyBroadException
        try:
            games = os.listdir(f"{ROMS_FOLDER}/{emulator_focus}")
            text_label = Label(text=f"{emulator_focus}: {len(games)} Games", fg="white", width=100, height=5,
                               font=("Arial", 12, "italic"), highlightcolor="Black", highlightthickness=5, bg="Brown",
                               highlightbackground="Purple")
            text_label.place(x=550, y=900)
        except Exception:
            pass
    generate_video_label()


def remove_text_label():
    global text_label
    global video_label
    # noinspection PyBroadException
    try:
        text_label.destroy()
    except Exception:
        pass
    remove_video_label()


def access_emulator(emulator, index):
    global roms
    global current_index
    global final_index
    global window
    global joystick
    global emulator_clicked
    global buttons_frame
    global emulator_rom_extensions
    emulator_clicked = emulator
    current_index = -1
    remove_widgets(buttons_frame)
    path = f"{ROMS_FOLDER}/{emulator}/"
    roms = os.listdir(path)
    updated_roms = []
    for extension in emulator_rom_extensions[emulator]:
        for rom in roms[:]:
            if rom[-3:] == extension:
                updated_roms.append(rom)
    roms = updated_roms
    roms.sort()
    window.title(f"{emulator.title()} Window")
    window.geometry("1920x1080")
    # window.geometry("1024x768")
    window.config(padx=0, pady=0, background="Black")

    bg_game = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/{emulator}.png")
    label_emulator_image = Label(window, image=bg_game, background="Black")
    label_emulator_image.place(x=0, y=0, relwidth=1, relheight=1)
    final_index = index + 20

    buttons_frame = Frame(window)
    buttons_frame.grid(row=0, column=0)
    bg_game_buttons_frame = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/{emulator}.png")
    label_buttons = Label(buttons_frame, image=bg_game_buttons_frame, background="Black")
    label_buttons.place(x=0, y=0, relwidth=1, relheight=1)

    generate_roms(roms, index, final_index, emulator)

    # Button created for testing
    # cmd = partial(controller_config, 1)
    # user = os.popen('whoami').read()
    # new_button = Button(fg="white", width=30, height=2, text=f"{user}", font=("Arial", 12, "italic"),
    #                     highlightcolor="White", highlightthickness=0, bg="Black", takefocus=0,
    #                     command=cmd)
    # new_button.grid(row=0, column=1)
    # cmd = partial(controller_config, 2)
    # user = os.popen('whoami').read()
    # new_button2 = Button(fg="white", width=30, height=2, text=f"{user}", font=("Arial", 12, "italic"),
    #                      highlightcolor="White", highlightthickness=0, bg="Black", takefocus=0,
    #                      command=cmd)
    # new_button2.grid(row=1, column=5)

    joystick.update_emulator_index(len(roms), emulator, final_index)

    move_focus_down()
    joystick.update_root(window)
    window.mainloop()


def open_rom(emulator, rom):
    global DEFAULT_ULTRA_RETRO_PATH
    if emulator in Applications["Mednafen"]:
        yscale = mednafen_emulators_name[emulator][1]
        xscale = mednafen_emulators_name[emulator][2]
        mednafen_emulator = mednafen_emulators_name[emulator][0]
        os.system(f"pasuspender -- /usr/games/mednafen -{mednafen_emulator}{yscale} "
                  f"-{mednafen_emulator}{xscale} '{ROMS_FOLDER}/{emulator}/{rom}'")
    elif emulator in Applications['PCSXR']:
        os.system(f"/usr/games/pcsxr -nogui -cdfile '{ROMS_FOLDER}/{emulator}/{rom}'")
    elif emulator in Applications['Snes9x EX']:
        os.system(f'"{DEFAULT_ULTRA_RETRO_PATH}/Snes9x EX+/s9xp" "{ROMS_FOLDER}/{emulator}/{rom}"')
    close_overlay()


def open_overlay(emulator, rom):
    global overlay_img
    global DEFAULT_ULTRA_RETRO_PATH
    global window         
    image1 = Image.open(f"{DEFAULT_ULTRA_RETRO_PATH}/Images/Games/overlay/{emulator}.png")
    img = ImageTk.PhotoImage(image1)
    overlay_img = Label(image=img)
    overlay_img.place(x=0, y=0)
    func1 = partial(open_rom, emulator, rom)
    # func1 = partial(print, emulator, rom)
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
    global buttons_frame
    global DEFAULT_ULTRA_RETRO_PATH
    global buttons_frame
    final_index = final_index_roms
    if final_index > len(rom_games):
        final_index = len(rom_games)
    buttons = {}
    for i in range(index, final_index):
        if i <= len(rom_games):
            chosen_rom = partial(open_overlay, emulator, rom_games[i])
            # chosen_rom = partial(print, emulator, rom_games[i])
            buttons[rom_games[i]] = Button(buttons_frame)
            buttons[rom_games[i]].configure(fg="white", width=50, height=2, text=rom_games[i],
                                            font=("Arial", 10, "italic"), highlightcolor="White",
                                            highlightthickness=0, bg="Black", command=chosen_rom,
                                            activeforeground="Red", cursor="man", takefocus=1)
            buttons[rom_games[i]].grid(row=i - index, column=0, columnspan=3, padx=10, pady=5)

    # buttons[rom_games[index]].focus()
    # current_rom_focus = buttons[rom_games[index]]


def move_focus_down():
    global buttons_frame
    global current_index
    global emulator_clicked
    global final_index
    global emulators_list_index
    remove_text_label()
    button = buttons_frame.winfo_children()[current_index]
    button.configure(bg="Black", highlightbackground='Black', highlightthickness=0)
    if current_index >= len(buttons_frame.winfo_children()) - 1:
        if window.title() != "UltraRetro" and len(roms) > 20:
            access_emulator(emulator_clicked, final_index)
        elif window.title() == "UltraRetro":
            create_emulators_list(emulators_list_index)
        current_index = 0
        button = buttons_frame.winfo_children()[current_index]

    else:
        current_index += 1
        button = buttons_frame.winfo_children()[current_index]
    if isinstance(button, Label):
        move_focus_down()
        return
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
    global buttons_frame
    global current_index
    global emulator_clicked
    global emulators_list_index
    remove_text_label()
    display_game_img("")
    button = buttons_frame.winfo_children()[current_index]
    button.configure(bg="Black", highlightbackground='Black', highlightthickness=0)
    if current_index <= 0:
        if window.title() != "UltraRetro" and len(roms) > 20:
            access_emulator(emulator_clicked, final_index - 40)
            current_index = len(buttons_frame.winfo_children())
        elif window.title() == "UltraRetro":
            create_emulators_list(emulators_list_index - 16)
        else:
            current_index = len(buttons_frame.winfo_children()) - 1
    else:
        current_index -= 1
    button = buttons_frame.winfo_children()[current_index]
    if isinstance(button, Label):
        move_focus_up()
        return
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
    janela.destroy()
    # for widget in janela.winfo_children():
    #     print(widget)
    #     widget.destroy()


def back_to_menu():
    global DEFAULT_BG
    global current_index
    global emulator_current_focus
    global buttons_frame
    current_index = 0
    remove_widgets(buttons_frame)
    initial_screen(window)
    label1 = Label(window, image=DEFAULT_BG)
    label1.place(x=0, y=0, relwidth=1, relheight=1)
    buttons_frame = Frame(window)
    label_frame_image = Label(buttons_frame, image=DEFAULT_BG)
    label_frame_image.place(x=0, y=0, relwidth=1, relheight=1)
    create_emulators_list(0)
    generate_exit_button()
    joystick.update_root(window)
    update_application()
    window.mainloop()


def generate_exit_button():
    global exit_button
    global buttons_frame
    # noinspection PyBroadException
    try:
        exit_button.destroy()
    except Exception:
        pass
    exit_button = Button(buttons_frame)
    exit_button.configure(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                          highlightcolor="White", highlightthickness=0, bg="Black",
                          command=window.destroy)
    exit_button.grid(row=7, column=2, columnspan=2, pady=10)
