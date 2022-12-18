import os
from tkinter import *
from functools import partial
from start_window import initial_screen
from PIL import Image, ImageTk
from threading import Thread
import pathlib
from tk_video_mod import tkvideo
import re


def remove_widgets(window_to_destroy):
    # window_to_destroy.destroy()
    for widget in window_to_destroy.winfo_children():
        widget.destroy()
    window_to_destroy.destroy()


class Emulator:
    def __init__(self, window):
        self.ROMS_FOLDER = "/usr/games/roms"
        self.EMULATOR_LIST = os.listdir(self.ROMS_FOLDER)
        self.EMULATOR_LIST.sort()
        self.current_rom_focus = None
        self.current_focus = None
        self.final_index = None
        self.emulators_list_index = None
        self.window = window
        self.video_frame = None
        self.buttons = None
        self.label_images = None
        self.current_index = None
        self.roms = None
        self.overlay_img = None
        self.DEFAULT_BG = None
        self.joystick = None
        self.emulator_clicked = None
        self.text_label = None
        self.video_label = None
        self.emulator_current_focus = None
        self.buttons_frame = None
        self.emulator_list_index = None
        self.exit_button = None
        self.images_dict = None
        self.player = None
        self.DEFAULT_ULTRA_RETRO_PATH = pathlib.Path(__file__).parent.resolve()
        self.Applications = {
            "Mednafen": ["Mega Drive", "Nintendo", "Game Boy Advance", "Game Boy Color", "Super Nintendo",
                         "Playstation", "Master System", "Atari Lynx", "Sega Game Gear", "WonderSwan",
                         "Sega Saturn"], "PCSXR": "Playstation", "Snes9x EX": "Super Nintendo"}
        self.mednafen_emulators_name = {"Playstation": ["psx", ".yscale 4.6", ".xscale 4.65"],
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
        self.emulator_rom_extensions = {"Playstation": ["cue"], "Mega Drive": ["zip"], "Nintendo": ["zip", "nes"],
                                        "Game Boy Advance": ["zip", "gba"], "Game Boy Color": ["zip"],
                                        "Super Nintendo": ["zip"], "Master System": ["zip"], "Atari Lynx": ["zip"],
                                        "Sega Game Gear": ["zip"], "WonderSwan": ["zip"], "Sega Saturn": ["chd"]}

    def controller_config(self, controller_number):
        self.joystick.assign_buttons(self.joystick.button_list_to_assign, controller_number)
        self.back_to_menu()

    def window_type(self, janela, control):
        self.joystick = control
        self.window = janela
        self.DEFAULT_BG = PhotoImage(file=f"{self.DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")
        self.buttons_frame_start()
        self.label_images = {}
        self.current_index = 1

    def buttons_frame_start(self):

        # noinspection PyBroadException
        try:
            remove_widgets(self.buttons_frame)
            # buttons_frame.destroy()
        except Exception:
            pass
        self.buttons_frame = Frame(self.window)
        bg = self.DEFAULT_BG
        frame_label_image = Label(self.buttons_frame, image=bg)
        frame_label_image.place(x=0, y=0, relwidth=1, relheight=1)

    def update_application(self):
        cmd = partial(os.system, f"echo LOGINPASSWD | sudo -S {self.DEFAULT_ULTRA_RETRO_PATH}/gitpull.sh")
        button_img = PhotoImage(file=f"{self.DEFAULT_ULTRA_RETRO_PATH}/Images/update_button.png")
        update_button = Button(fg="Red", width=270, height=100, text="Update", highlightcolor="White",
                               bg="Black", image=button_img, borderwidth=0, command=cmd, compound=LEFT)
        update_button.place(x=1600, y=20)
        self.window.mainloop()

    def create_emulators_list(self, index):
        max_index = len(self.EMULATOR_LIST) - 1
        self.buttons_frame_start()
        if index < -8:
            index = index + 11
        self.emulators_list_index = index + 8
        counter = 0
        for emulator in range(index, self.emulators_list_index):
            if counter >= 8:
                print("COUNTER > 7")
            else:
                if emulator <= max_index:
                    self.create_emulators(self.EMULATOR_LIST[emulator], counter)
                else:
                    self.emulators_list_index = (emulator - 1) - max_index
                    self.create_emulators(self.EMULATOR_LIST[self.emulators_list_index], counter)
                    self.emulators_list_index = emulator - max_index
                    # generate_exit_button()
            counter += 1
            # for emulator in EMULATOR_LIST:
            #     create_emulators(emulator, EMULATOR_LIST.index(emulator))    

    def create_emulators(self, name, index):
        self.emulator_clicked = name
        self.current_index = -1
        access = partial(self.access_emulator, name, 0)
        self.buttons_frame.grid(row=0, column=0)
        emulator_button = Button(self.buttons_frame)
        emulator_button.configure(fg="white", width=30, height=5, text=name, font=("Arial", 12, "italic"),
                                  highlightcolor="White", highlightthickness=0, bg="Black", command=access)
        emulator_button.grid(row=index, column=0, columnspan=2, pady=10)
        self.emulator_current_focus = emulator_button
        self.move_focus_down()

    def generate_preview_emulator_videos(self):
        # return
        # noinspection PyBroadException
        try:
            self.player.stop()
            self.remove_preview_emulator_videos()
        except Exception:
            pass
        # noinspection PyBroadException
        try:
            games = os.listdir(f"{self.ROMS_FOLDER}/{self.emulator_current_focus}/videos")
            self.video_frame = Frame(self.window)
            self.video_label = Label(self.video_frame)
            self.player = tkvideo(f"{self.ROMS_FOLDER}/{self.emulator_current_focus}/videos", self.video_label, loop=0,
                                  size=(800, 600), video_list=games, frames_to_display=300)
            self.video_frame.place(x=600, y=200)
            self.video_label.grid(row=0, column=0)
            self.player.play_list()
        except Exception:
            print("Something Went Wrong with the generate_preview_emulator_videos class!")
            pass

    def remove_preview_emulator_videos(self):
        # noinspection PyBroadException
        try:
            if isinstance(self.video_frame, Frame):
                self.video_frame.place_forget()
            if isinstance(self.video_label, Label):
                self.video_label.grid_forget()
        except Exception:
            pass
        # noinspection PyBroadException
        try:
            self.video_frame = None
            self.video_label = None
        except Exception:
            pass

    def generate_text_label(self, emulator_focus):
        self.emulator_current_focus = emulator_focus
        if self.window.title() == "UltraRetro":
            # noinspection PyBroadException
            try:
                games = os.listdir(f"{self.ROMS_FOLDER}/{emulator_focus}")
                self.text_label = Label(text=f"{emulator_focus}: {len(games)} Games", fg="white", width=100, height=5,
                                        font=("Arial", 12, "italic"), highlightcolor="Black", highlightthickness=5,
                                        bg="Brown", highlightbackground="Purple")
                self.text_label.place(x=550, y=900)
            except Exception:
                pass
        self.generate_preview_emulator_videos()

    def remove_text_label(self):
        # noinspection PyBroadException
        try:
            self.text_label.destroy()
        except Exception:
            pass
        self.remove_preview_emulator_videos()

    def access_emulator(self, emulator, index):
        self.emulator_clicked = emulator
        self.current_index = -1
        remove_widgets(self.buttons_frame)
        path = f"{self.ROMS_FOLDER}/{emulator}/"
        self.roms = os.listdir(path)
        updated_roms = []
        for extension in self.emulator_rom_extensions[emulator]:
            for rom in self.roms[:]:
                if rom[-3:] == extension:
                    updated_roms.append(rom)
        self.roms = updated_roms
        self.roms.sort()
        self.window.title(f"{emulator.title()} Window")
        self.window.geometry("1920x1080")
        # window.geometry("1024x768")
        self.window.config(padx=0, pady=0, background="Black")

        bg_game = PhotoImage(file=f"{self.DEFAULT_ULTRA_RETRO_PATH}/Images/{emulator}.png")
        label_emulator_image = Label(self.window, image=bg_game, background="Black")
        label_emulator_image.place(x=0, y=0, relwidth=1, relheight=1)
        self.final_index = index + 20

        self.buttons_frame = Frame(self.window)
        self.buttons_frame.grid(row=0, column=0)
        bg_game_buttons_frame = PhotoImage(file=f"{self.DEFAULT_ULTRA_RETRO_PATH}/Images/{emulator}.png")
        label_buttons = Label(self.buttons_frame, image=bg_game_buttons_frame, background="Black")
        label_buttons.place(x=0, y=0, relwidth=1, relheight=1)
        self.generate_roms(self.roms, index, self.final_index, emulator)
        # Button created for testing 1
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
        self.joystick.update_emulator_index(len(self.roms), emulator, self.final_index)

        self.move_focus_down()
        self.joystick.update_root(self.window)
        self.window.mainloop()

    def open_rom(self, emulator, rom):
        if emulator in self.Applications["Mednafen"]:
            yscale = self.mednafen_emulators_name[emulator][1]
            xscale = self.mednafen_emulators_name[emulator][2]
            mednafen_emulator = self.mednafen_emulators_name[emulator][0]
            os.system(f"pasuspender -- /usr/games/mednafen -{mednafen_emulator}{yscale} "
                      f"-{mednafen_emulator}{xscale} '{self.ROMS_FOLDER}/{emulator}/{rom}'")
            # os.system(f"/usr/games/mednafen -{mednafen_emulator}{yscale} "
            #           f"-{mednafen_emulator}{xscale} '{self.ROMS_FOLDER}/{emulator}/{rom}'")
        elif emulator in self.Applications['PCSXR']:
            os.system(f"/usr/games/pcsxr -nogui -cdfile '{self.ROMS_FOLDER}/{emulator}/{rom}'")
        elif emulator in self.Applications['Snes9x EX']:
            os.system(f'"{self.DEFAULT_ULTRA_RETRO_PATH}/Snes9x EX+/s9xp" "{self.ROMS_FOLDER}/{emulator}/{rom}"')
        self.close_overlay()

    def open_overlay(self, emulator, rom):
        image1 = Image.open(f"{self.DEFAULT_ULTRA_RETRO_PATH}/Images/Games/overlay/{emulator}.png")
        img = ImageTk.PhotoImage(image1)
        self.overlay_img = Label(image=img)
        self.overlay_img.place(x=0, y=0)
        func1 = partial(self.open_rom, emulator, rom)
        Thread(target=func1).start()
        Thread(target=self.window.mainloop()).start()

    def close_overlay(self):
        self.overlay_img.destroy()
        self.window.focus_force()
        self.joystick.update_root(self.window)

    def generate_roms(self, rom_games, index, final_index_roms, emulator):
        self.final_index = final_index_roms
        if self.final_index > len(rom_games) - 1:
            self.final_index = len(rom_games)
        if index < len(rom_games) * -1:
            index = 0
            self.final_index = 20
        self.buttons = {}
        self.images_dict = {}
        for i in range(index, self.final_index):
            if i <= len(rom_games):
                chosen_rom = partial(self.open_overlay, emulator, rom_games[i])
                original_display_name = rom_games[i]
                display_name = rom_games[i][:-4].strip().replace("_", " ").title()
                display_name = re.sub(r"\[.*?]", "", display_name)
                self.images_dict[display_name] = original_display_name
                self.buttons[rom_games[i]] = Button(self.buttons_frame)
                self.buttons[rom_games[i]].configure(fg="white", width=50, height=2, text=display_name,
                                                     font=("Arial", 10, "italic"), highlightcolor="White",
                                                     highlightthickness=0, bg="Black", command=chosen_rom,
                                                     activeforeground="Red", cursor="man", takefocus=1)
                self.buttons[rom_games[i]].grid(row=i - index, column=0, columnspan=3, padx=10, pady=5)
            self.buttons[rom_games[index]].focus()
            self.current_rom_focus = self.buttons[rom_games[index]]
        if self.final_index + 1 > len(rom_games):
            self.current_index = 0
            self.final_index = 0
        # buttons[rom_games[index]].focus()
        # current_rom_focus = buttons[rom_games[index]]    

    def move_focus_down(self):
        self.remove_text_label()
        button = self.buttons_frame.winfo_children()[self.current_index]
        button.configure(bg="Black", highlightbackground='Black', highlightthickness=0)

        if self.current_index >= len(self.buttons_frame.winfo_children()) - 1:
            if self.window.title() != "UltraRetro" and len(self.roms) > 20:
                button_name = button.cget("text")
                if self.images_dict[button_name] == self.roms[len(self.roms) - 1]:
                    self.access_emulator(self.emulator_clicked, 0)
                else:
                    self.access_emulator(self.emulator_clicked, self.final_index)
            elif self.window.title() == "UltraRetro":
                self.create_emulators_list(self.emulators_list_index)
            self.current_index = 0
            button = self.buttons_frame.winfo_children()[self.current_index]

        else:
            self.current_index += 1
            button = self.buttons_frame.winfo_children()[self.current_index]
        if isinstance(button, Label):
            self.move_focus_down()
            return
        # noinspection PyBroadException
        try:
            button.focus_force()
            button_text = button.cget('text')
            button_text = self.images_dict[button_text]
        except Exception:
            button_text = ""

        button.configure(bg="Red", highlightbackground='Yellow', highlightthickness=5, highlightcolor="Purple")
        self.generate_text_label(button.cget('text'))
        self.display_game_img(button_text)

    def move_focus_up(self):
        self.remove_text_label()
        # display_game_img("")
        button = self.buttons_frame.winfo_children()[self.current_index]
        button.configure(bg="Black", highlightbackground='Black', highlightthickness=0)
        if self.current_index <= 0:
            if self.window.title() != "UltraRetro" and len(self.roms) > 20:
                self.access_emulator(self.emulator_clicked, self.final_index - 40)
                self.current_index = len(self.buttons_frame.winfo_children())
            elif self.window.title() == "UltraRetro":
                self.create_emulators_list(self.emulators_list_index - 16)
            else:
                self.current_index = len(self.buttons_frame.winfo_children()) - 1
        else:
            self.current_index -= 1
        button = self.buttons_frame.winfo_children()[self.current_index]
        if isinstance(button, Label):
            self.move_focus_up()
            return
        # noinspection PyBroadException
        try:
            button.focus_force()
            button_text = button.cget('text')
            button_text = self.images_dict[button_text]
        except Exception:
            pass
            button_text = ""

        button.configure(bg="Red", highlightbackground='Yellow', highlightthickness=5, highlightcolor="Purple")
        self.generate_text_label(button.cget('text'))
        self.display_game_img(button_text)

    def format_image_file_name(self, image_text):
        image_name_formatted = f"{self.ROMS_FOLDER}/{self.emulator_clicked}/images/"
        button_text_list = image_text.split(".")
        for word in range(len(button_text_list) - 1):
            if word != button_text_list[len(button_text_list) - 1]:
                image_name_formatted += button_text_list[word] + "."
        return image_name_formatted + "png"

        # Function try to find an image with the same name of the game,

    # in case it is not found, try to find an image with part of the name of the game
    def display_game_img(self, button_text):
        # return
        game_name = button_text
        for values in self.label_images.values():
            values.destroy()
        if game_name == '':
            return
        img = ''
        # noinspection PyBroadException
        try:
            button_text_formatted = self.format_image_file_name(button_text)
            image1 = Image.open(f"{button_text_formatted}")
            img = ImageTk.PhotoImage(image1)
            label_image = Label(image=img)
            label_image.place(x=600, y=200)
            self.label_images[img] = label_image
            self.joystick.update_root(self.window)
            self.window.mainloop()
            return
        except Exception:
            pass
        # noinspection PyBroadException
        try:
            images_folder = os.listdir(f"{self.ROMS_FOLDER}/{self.emulator_clicked}/images")
            for image in images_folder:
                game_name1 = game_name[:-4].strip()
                image1 = image[:-4].strip()
                image_words = image1.split(' ')
                game_words = game_name1.split(' ')
                if len(game_words) == 1:
                    if game_words[0] in image_words:
                        image1 = Image.open(f"{self.ROMS_FOLDER}/{self.emulator_clicked}/images/{image}")
                        img = ImageTk.PhotoImage(image1)
                        break
                elif len(game_words) == 2:
                    if game_words[0] in image_words and game_words[1] in image_words:
                        image1 = Image.open(f"{self.ROMS_FOLDER}/{self.emulator_clicked}/images/{image}")
                        img = ImageTk.PhotoImage(image1)
                        break
                elif len(game_words) > 2:
                    count = 0
                    for word in game_words:
                        if word in image_words:
                            count += 1
                        elif count >= 2:
                            image1 = Image.open(f"{self.ROMS_FOLDER}/{self.emulator_clicked}/images/{image}")
                            img = ImageTk.PhotoImage(image1)
                            label_image = Label(image=img)
                            label_image.place(x=600, y=200)
                            self.label_images[img] = label_image
                            self.joystick.update_root(self.window)
                            self.window.mainloop()
                            return
        except Exception:
            pass
        # noinspection PyBroadException

        label_image = Label(image=img)
        label_image.place(x=600, y=200)
        self.label_images[img] = label_image
        self.joystick.update_root(self.window)
        self.window.mainloop()

    def back_to_menu(self):
        self.current_index = 0
        remove_widgets(self.buttons_frame)
        # remove_widgets(window)
        initial_screen(self.window)
        label1 = Label(self.window, image=self.DEFAULT_BG)
        label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.buttons_frame = Frame(self.window)
        label_frame_image = Label(self.buttons_frame, image=self.DEFAULT_BG)
        label_frame_image.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_emulators_list(0)
        self.generate_exit_button()
        self.joystick.update_root(self.window)
        self.update_application()
        self.window.mainloop()

    def generate_exit_button(self):
        # noinspection PyBroadException
        try:
            self.exit_button.destroy()
        except Exception:
            pass
        self.exit_button = Button(self.buttons_frame)
        self.exit_button.configure(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                                   highlightcolor="White", highlightthickness=0, bg="Black",
                                   command=self.exit_application)
        self.exit_button.grid(row=7, column=2, columnspan=2, pady=10)

    def exit_application(self):
        # noinspection PyBroadException
        try:
            self.player.stop()
        except Exception:
            print("Error when quiting the application")
        # noinspection PyBroadException
        try:
            self.window.destroy()
        except Exception:
            print("Error when quiting the application")
