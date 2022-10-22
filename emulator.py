import os
from tkinter import *
from functools import partial
from start_window import initial_screen
from PIL import Image, ImageTk
from pynput import keyboard
from pynput.keyboard import Key


# def on_press(key):
#     pass
#
#
# def on_release(key):
#     if(key==Key.s):
#         move_focus_down()
#
#
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()


# keyboard.add_hotkey('s', lambda: move_focus_down())

DEFAULT_ULTRA_RETRO_PATH = "/home/Eder/Desktop/UltraRetro/UltraRetro"
ROMS_FOLDER = "/Usr/games/roms"
EMULATOR_LIST = os.listdir(ROMS_FOLDER)
global window
global buttons
global label_images
global current_index
global roms
global current_rom

current_rom_focus = None
current_focus = None
# global roms
DEFAULT_BG = "Images/bg_img.png"


def window_type(janela):
    global window
    global DEFAULT_BG
    global label_images
    global current_index
    window = janela
    label_images = {}
    current_index = 0
    DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")


def access_emulator(emulator, index):
    global roms
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
    global current_index
    current_index = 0
    access = partial(access_emulator, name, 0)
    emulator_button = Button(fg="white", width=30, height=5, text=name, font=("Arial", 12, "italic"),
                             highlightcolor="White", highlightthickness=0, bg="Black", command=access)
    emulator_button.grid(row=index, column=0, columnspan=2, pady=10)


def open_rom(emulator, rom):
    os.system(f"/usr/games/mednafen {ROMS_FOLDER}/{emulator}/'{rom}'")


def generate_roms(roms, index, final_index, emulator):
    global buttons
    global current_rom_focus
    if final_index > len(roms):
        final_index = len(roms)

    buttons = {}
    for i in range(index, final_index):
        if i <= len(roms):
            chosen_rom = partial(open_rom, emulator, roms[i])
            buttons[roms[i]] = Button(fg="white", width=50, height=2, text=roms[i], font=("Arial", 10, "italic"),
                                    highlightcolor="White", highlightthickness=0, bg="Black",
                                    command=chosen_rom, activeforeground="Red", cursor="man", takefocus=1)
            buttons[roms[i]].grid(row=i - index, column=0, columnspan=3, padx=10, pady=5)

    buttons[roms[index]].focus()
    current_rom_focus = buttons[roms[index]]


def move_focus_down():
    global current_rom_focus
    print(current_rom_focus)
    focus = False
    for key in buttons.keys():
        if focus:
            buttons[key].focus()
            buttons[key].flash()
            current_rom_focus = buttons[key]
            print(key)
            try:
                key = key.replace(".smc", ".png")
                print(key)
                image1 = Image.open(f"Images/Games/{key}.png")
                img = ImageTk.PhotoImage(image1)
            except:
                img = ""
            return display_game_img(img)
        if current_rom_focus == buttons[key]:
            focus = True

    # Implementation using global variable current_index
    # global current_index
    # if current_index >= len(window.winfo_children()):
    #     return
    # for widget_index in range(len(window.winfo_children()) - 4):
    #     if widget_index == current_index + 1:
    #         current_index += 1
    #         window.winfo_children()[widget_index].focus()
    #         window.winfo_children()[widget_index].flash()

    # display_game_img()


def move_focus_up():
    global current_rom_focus
    focus = False
    reverse_buttons = reversed(sorted(buttons.keys()))
    for key in reverse_buttons:
        if focus:
            buttons[key].focus()
            buttons[key].flash()
            current_rom_focus = buttons[key]
            print(key)
            try:
                key = key.replace(".smc", ".png")
                image1 = Image.open(f"Images/Games/{key}.png")
                img = ImageTk.PhotoImage(image1)
            except:
                img = ""
            return display_game_img(img)
        if current_rom_focus == buttons[key]:
            focus = True

    # global current_index
    # print(current_index)
    # if current_index <= 0:
    #     return
    # for widget_index in range(len(window.winfo_children()) - 4):
    #     if widget_index == current_index - 1:
    #         current_index -= 1
    #         window.winfo_children()[widget_index].focus()
    #         window.winfo_children()[widget_index].flash()
    # display_game_img()





# def display_game_img():
#     global label_images
#     global roms
#     rom = roms[current_index]
#     print(rom)
#     try:
#         image1 = Image.open(f"Images/Games/{rom}.png")
#         img = ImageTk.PhotoImage(image1)
#     except:
#         for values in label_images.values():
#             values.destroy()
#         return
#
#     global window
#     label_image = Label(image=img)
#     label_image.place(x=800, y=250)
#     label_images[img] = label_image
#     window.mainloop()


def display_game_img(image):
    global label_images
    if image == '':
        for values in label_images.values():
            values.destroy()
        return
    global window
    label_image = Label(image=image)
    label_image.place(x=800, y=250)
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


def create_emulators_list():
    for emulator in EMULATOR_LIST:
        create_emulators(emulator, EMULATOR_LIST.index(emulator))


def generate_exit_button():
    row = len(EMULATOR_LIST)
    exit_button = Button(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=window.destroy)
    exit_button.grid(row=row, column=0, columnspan=2, pady=10)
