import pygame
from emulator import move_focus_down, move_focus_up, back_to_menu, access_emulator, DEFAULT_ULTRA_RETRO_PATH
from mednafen_controller import mednafen_controller_config
from tkinter import *
import time
import json
from threading import Thread
from functools import partial


class JoystickControllers:
    def __init__(self, root):
        self.menu = True
        self.controllers_data_loaded = False
        self.controller1 = None
        self.controller1_buttons = {}
        self.controller2 = None
        self.controller2_buttons = {}
        self.button_list = None
        self.data_read = False
        self.assigned_keys = []
        self.window = root
        self.controllers = []
        self.configured_controllers = []
        self.update_root(self.window)
        self.up = None
        self.down = None
        self.emulator = None
        self.index = None
        self.len_roms = None
        self.button_list_to_assign = ["a", "b", "x", "y", "l", "r", "lt", "rt", "start", "select"]

    def update_root(self, root):
        self.window = root
        pygame.init()
        self.controllers = []
        self.configured_controllers = []
        self.get_controllers()
        self.read_controller_data()
        self.find_events()

    def update_emulator_index(self, len_roms, emulator, index):
        self.emulator = emulator
        self.index = index
        self.len_roms = len_roms

    def get_controllers(self):
        pygame.joystick.init()
        for joy in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(joy).init()
            device_name = pygame.joystick.Joystick(joy).get_name()
            device_num_axis = pygame.joystick.Joystick(joy).get_numaxes() + 2
            device_num_buttons = pygame.joystick.Joystick(joy).get_numbuttons()
            self.controllers.append(pygame.joystick.Joystick(joy))
            num_buttons = hex(device_num_buttons)
            if num_buttons == "0x10":
                num_buttons = hex(device_num_buttons).replace("x", "0")
            else:
                num_buttons = hex(device_num_buttons).replace("x", "00")
            device_dict = {"numaxis": device_num_axis, "numbuttons": num_buttons}
            if not self.controllers_data_loaded:
                if device_dict:
                    if device_name == "Xbox One S Controller":
                        device_name = "Microsoft X-Box One S pad"
                    # print(device_dict)
                    # print(device_name)
                    controllers_file = open(f"{DEFAULT_ULTRA_RETRO_PATH}/controllers.cfg")
                    data = json.load(controllers_file)
                    for i in data['controllers']:
                        if i["controller"] == device_name:
                            controller_number = i["Controller_number"]
                            task = partial(mednafen_controller_config, device_dict, device_name, controller_number)
                            thread = Thread(target=task)
                            thread.start()
        self.controllers_data_loaded = True
        """
        Testing button state
        # for button in range(device_num_buttons):
            #     button_state = pygame.joystick.Joystick(joy).get_button(button)
            #     if button_state == 1:
            #         print(pygame.joystick.Joystick(joy).get_name())
        """

    def assign_buttons(self, key_list, controller_number):
        new_dict = {}
        for key in key_list:
            time.sleep(0.5)
            exit_loop = False
            while not exit_loop:
                self.menu = False
                self.find_events()
                controller_index = 0
                for controller in self.controllers:
                    controller_index += 1
                    controller.quit()
                    controller.init()
                    assign_buttons_frame = Frame(self.window)
                    assign_buttons_frame.place(x=530, y=20, width=914, height=108)
                    for button in range(controller.get_numbuttons()):
                        key_label = Label(assign_buttons_frame, text=f"Press {key.upper()}", fg="white", width=100,
                                          height=5, font=("Arial", 12, "italic"), highlightcolor="Black",
                                          highlightthickness=5,
                                          bg="Brown",
                                          highlightbackground="Purple")
                        key_label.place(x=0, y=0)
                        assign_buttons_frame.update()
                        if controller.get_button(button) == 1:
                            print(button)
                            if button > -1:
                                new_dict["controller"] = controller.get_name()
                                new_dict["Controller_number"] = controller_number
                                new_dict[key] = button
                                exit_loop = True
        self.assigned_keys.append(new_dict)
        self.save_controller_data()
        self.menu = True
        self.controllers_data_loaded = False

    def save_controller_data(self):
        joysticks = self.assigned_keys
        is_control_in_list = False
        for joystick in joysticks:
            joysticks_to_write = joystick
            with open("/usr/games/UltraRetro/controllers.cfg", "r+") as f:
                data = json.load(f)
                control_index = 0
                for controller in data["controllers"]:
                    if controller['Controller_number'] == joysticks_to_write['Controller_number']:
                        is_control_in_list = True
                        control_index = data["controllers"].index(controller)
                if is_control_in_list:
                    data["controllers"][control_index] = joysticks_to_write
                else:
                    data["controllers"].append(joysticks_to_write)
                f.seek(0)
                json.dump(data, f, indent=4)
            self.read_controller_data()

    def read_controller_data(self):
        # noinspection PyBroadException
        try:
            f = open(f"{DEFAULT_ULTRA_RETRO_PATH}/controllers.cfg")
            data = json.load(f)
            self.button_list = data['controllers']
            for ctr in self.controllers:
                for control in data['controllers']:
                    if ctr.get_name() == control['controller']:
                        if control["Controller_number"] == 1:
                            self.controller1 = ctr
                        elif control["Controller_number"] == 2:
                            self.controller2 = ctr
        except Exception:
            pass

    def read_button_list(self):
        # noinspection PyBroadException
        try:
            for controller_data in self.button_list:
                for button in controller_data:
                    if button == 'a':
                        self.controller1_buttons['joy_a'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_a'] = self.controller2.get_button(controller_data[button])
                    if button == 'b':
                        self.controller1_buttons['joy_b'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_b'] = self.controller2.get_button(controller_data[button])
                    if button == 'x':
                        self.controller1_buttons['joy_x'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_x'] = self.controller2.get_button(controller_data[button])
                    if button == 'y':
                        self.controller1_buttons['joy_y'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_y'] = self.controller2.get_button(controller_data[button])
                    if button == 'l':
                        self.controller1_buttons['joy_lb'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_lb'] = self.controller2.get_button(controller_data[button])
                    if button == 'r':
                        self.controller1_buttons['joy_rb'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_rb'] = self.controller2.get_button(controller_data[button])
                    if button == 'lt':
                        self.controller1_buttons['joy_lt'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_lt'] = self.controller2.get_button(controller_data[button])
                    if button == 'rt':
                        self.controller1_buttons['joy_rt'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_rt'] = self.controller2.get_button(controller_data[button])
                    if button == 'start':
                        self.controller1_buttons['joy_start'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_start'] = self.controller2.get_button(controller_data[button])
                    if button == 'select':
                        self.controller1_buttons['joy_select'] = self.controller1.get_button(controller_data[button])
                        self.controller2_buttons['joy_select'] = self.controller2.get_button(controller_data[button])

        except Exception:
            pass

    def find_events(self):
        events = pygame.event.get()
        if pygame.joystick.get_count() < 1:
            return
        self.read_button_list()
        if self.menu:
            for joystick in self.controllers:
                # noinspection PyBroadException
                try:
                    if self.window.focus_get():
                        for event in events:
                            if event.type == pygame.JOYBUTTONDOWN:
                                if self.controller1_buttons['joy_a'] == 1 or self.controller2_buttons['joy_a'] == 1:
                                    self.window.focus_get().invoke()
                                if self.controller1_buttons['joy_b'] == 1 or self.controller2_buttons['joy_b'] == 1:
                                    back_to_menu()
                                if self.controller1_buttons['joy_y'] == 1 or self.controller2_buttons['joy_y'] == 1:
                                    print(self.assigned_keys)
                                if self.controller1_buttons['joy_lt'] == 1 or self.controller2_buttons['joy_lt'] == 1:
                                    self.window.event_generate('<<LT>>')
                                if self.controller1_buttons['joy_rt'] == 1 or self.controller2_buttons['joy_rt'] == 1:
                                    self.window.event_generate('<<RT>>')
                                if self.controller1_buttons['joy_start'] == 1 and\
                                        self.controller1_buttons['joy_select'] == 1 or \
                                        self.controller2_buttons['joy_start'] == 1 and \
                                        self.controller2_buttons['joy_select'] == 1:
                                    self.window.destroy()

                            # Adding Controller Event
                            if event.type == 1541:
                                self.controllers = []
                                self.get_controllers()
                            if event.type == pygame.JOYHATMOTION:
                                hats = joystick.get_numhats()
                                for i in range(hats):
                                    hat = joystick.get_hat(i)
                                    if hat == (0, -1):
                                        move_focus_down()
                                    if hat == (0, 1):
                                        move_focus_up()
                                    if self.window.title() != "UltraRetro":
                                        if hat == (-1, 0):
                                            if self.len_roms > 21:
                                                access_emulator(self.emulator, self.index - 40)
                                        if hat == (1, 0):
                                            if self.len_roms > 21:
                                                access_emulator(self.emulator, self.index)
                except Exception:
                    pass
            self.window.after(1, self.find_events)
