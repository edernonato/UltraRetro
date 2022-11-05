import pygame
from emulator import move_focus_down, move_focus_up, back_to_menu, access_emulator, DEFAULT_ULTRA_RETRO_PATH
from mednafen_controller import mednafen_controller_config
import tkinter
import time
import json


class JoystickControllers:
    def __init__(self, root):
        self.menu = True
        self.controllers_data_loaded = False
        self.controller1 = None
        self.button_list = None
        self.data_read = False
        self.joy_axis_x = None
        self.joy_axis_y = None
        self.joy_a = None
        self.joy_b = None
        self.joy_x = None
        self.joy_y = None
        self.joy_lb = None
        self.joy_rb = None
        self.joy_lt = None
        self.joy_rt = None
        self.assigned_keys = []
        self.window = root
        self.controllers = []
        self.configured_controllers = []
        # self.get_controllers()
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
                    print(device_dict)
                    print(device_name)
                    mednafen_controller_config(device_dict, device_name)
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
            print(f"Press {key}")
            exit_loop = False
            while not exit_loop:
                self.menu = False
                self.find_events()
                controller_index = 0
                for controller in self.controllers:
                    controller_index += 1
                    controller.quit()
                    controller.init()
                    for button in range(controller.get_numbuttons()):
                        key_label = tkinter.Label(text=f"Press {key}", fg="white", width=100, height=5,
                                                  font=("Arial", 12, "italic"), highlightcolor="Black",
                                                  highlightthickness=5,
                                                  bg="Brown",
                                                  highlightbackground="Purple")
                        key_label.place(x=550, y=900)
                        # self.window.update()
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
        joysticks_to_write = {}
        joysticks = self.assigned_keys

        for joystick in joysticks:

            print(f"JOYSTICK IN self.assigned_keys {joystick}")
            # joystick["controller"] = joystick["controller"].get_name()
            joysticks_to_write["controllers"] = [joystick]

        with open("/usr/games/UltraRetro/controllers.cfg", "r+") as f:
            json_data = json.loads(str(joysticks_to_write).replace("'", '"'))
            print(json_data)
            json.dump(json_data, f, indent=4)
        self.read_controller_data()

    def read_controller_data(self):
        # noinspection PyBroadException
        try:
            f = open(f"{DEFAULT_ULTRA_RETRO_PATH}/controllers.cfg")
            data = json.load(f)
            self.button_list = data['controllers']
            for ctr in self.controllers:
                if ctr.get_name() == data['controllers'][0]["controller"]:
                    self.controller1 = ctr
        except Exception:
            pass

    def read_button_list(self):
        # noinspection PyBroadException
        try:
            for controller_data in self.button_list:
                for button in controller_data:
                    if button == 'a':
                        self.joy_a = self.controller1.get_button(controller_data[button])
                    if button == 'b':
                        self.joy_b = self.controller1.get_button(controller_data[button])
                    if button == 'x':
                        self.joy_x = self.controller1.get_button(controller_data[button])
                    if button == 'y':
                        self.joy_y = self.controller1.get_button(controller_data[button])
                    if button == 'l':
                        self.joy_lb = self.controller1.get_button(controller_data[button])
                    if button == 'r':
                        self.joy_rb = self.controller1.get_button(controller_data[button])
                    if button == 'lt':
                        self.joy_lt = self.controller1.get_button(controller_data[button])
                    if button == 'rt':
                        self.joy_rt = self.controller1.get_button(controller_data[button])
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
                                if self.joy_a == 1:
                                    print(self.joy_a)
                                    self.window.focus_get().invoke()
                                if self.joy_b == 1:
                                    back_to_menu()
                                if self.joy_y == 1:
                                    print(self.assigned_keys)
                                if self.joy_lt == 1:
                                    self.window.event_generate('<<LT>>')
                                if self.joy_rt == 1:
                                    self.window.event_generate('<<RT>>')
                                    # print(self.assigned_keys)
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
