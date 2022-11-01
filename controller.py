import pygame
from emulator import move_focus_down, move_focus_up, back_to_menu, access_emulator
from mednafen_controller import mednafen_controller_config
import tkinter


class JoystickControllers:
    def __init__(self, root):
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
        self.button_list = ["a", "b", "c",  "start", "l", "r", "x", "y", "select"]

    def update_root(self, root):
        self.window = root
        pygame.init()
        self.controllers = []
        self.configured_controllers = []
        self.get_controllers()
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
            device_dict = {"numaxis": device_num_axis, "numbuttons": hex(device_num_buttons).replace("x", "00")}
            if device_dict:
                if device_name == "Xbox One S Controller":
                    device_name = "Microsoft X-Box One S pad"
                # mednafen_controller_config(device_dict, device_name)
            # for button in range(device_num_buttons):
            #     button_state = pygame.joystick.Joystick(joy).get_button(button)
            #     if button_state == 1:
            #         print(pygame.joystick.Joystick(joy).get_name())

    def assign_buttons(self, key_list, controller_number):
        new_dict = {}
        for key in key_list:
            print(f"Press {key}")
            exit = False
            while not exit:
                for controller in self.controllers:
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
                            if button > -1:
                                new_dict["controller"] = controller
                                new_dict["Controller_number"] = controller_number
                                new_dict[key] = button
                                # print(f"Assigned === {new_dict}")
                                # print(self.assigned_keys)
                                exit = True

        self.assigned_keys.append(new_dict)
    def find_events(self):
        events = pygame.event.get()
        if pygame.joystick.get_count() < 1:
            return
        if self.assigned_keys:
        #     # print(self.assigned_keys)
            for controller in self.assigned_keys:
        #         # print(controller)
                control = controller["controller"]

                # controller["controller"].init()
                # joy_axis_x = joystick.get_axis(2)
                # joy_axis_y = joystick.get_axis(3)
                joy_a = control.get_button(controller["a"])
                joy_b = control.get_button(controller["b"])
                joy_x = control.get_button(controller["x"])
                joy_y = control.get_button(controller["y"])
                joy_lb = control.get_button(controller["l"])
                joy_rb = control.get_button(controller["r"])
                # joy_lt = controller.get_button(controller["lt"])
                # joy_rt = controller.get_button(controller["rt"])

        for joystick in self.controllers:
            # joystick.init()
            joy_axis_x = joystick.get_axis(2)
            joy_axis_y = joystick.get_axis(3)
            # joy_a = joystick.get_button(0)
            # joy_b = joystick.get_button(1)
            # joy_x = joystick.get_button(2)
            # joy_y = joystick.get_button(3)
            # joy_lb = joystick.get_button(4)
            # joy_rb = joystick.get_button(5)
            # joy_lt = joystick.get_button(6)
            # joy_rt = joystick.get_button(7)

            # noinspection PyBroadException
            try:
                if self.window.focus_get():
                    for event in events:
                        if event.type == pygame.JOYBUTTONDOWN:
                            if joy_a == 1:
                                self.window.focus_get().invoke()
                            if joy_b == 1:
                                back_to_menu()
                            if joy_y == 1:
                                print(self.assigned_keys)
                            if joy_lt == 1:
                                self.window.event_generate('<<LT>>')
                            if joy_rt == 1:
                                self.window.event_generate('<<RT>>')
                                print(self.assigned_keys)
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

