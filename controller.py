import pygame
from emulator import move_focus_down, move_focus_up, back_to_menu, access_emulator
from mednafen_controller import mednafen_controller_config

# with open("/proc/bus/input/devices", "r") as f:
#     old = f.read()  # read everything in the file
#     f.seek(0)  # rewind
#
#
# new = old.split("\n\n")
# # print(new)
# device_dict = {}
# for line in range(len(new)):
#     # print(new[line])
#     device_name = 'DragonRise Inc. Generic USB Joystick'.replace(" ", "")
#     # device_name = 'Microsoft X-Box One S pad'.replace(" ", "")
#     if device_name in new[line].replace(" ", ""):
#         device_info = new[line].split("\n")
#         # print(device_info)
#         bus_vendor_product = device_info[0]
#         new_bus_vendor_product = bus_vendor_product.split(" ")
#         bus = new_bus_vendor_product[1].replace("Bus=", "")
#         vendor = new_bus_vendor_product[2].replace("Vendor=", "")
#         product = new_bus_vendor_product[3].replace("Product=", "")
#         version = new_bus_vendor_product[4].replace("Version=", "")
#         name = device_info[1].replace("N: Name=", "")
#         device_dict["name"] = name
#         device_dict["bus"] = bus
#         device_dict["vendor"] = vendor
#         device_dict["product"] = product
#         device_dict["version"] = version
# print(device_dict)

class JoystickControllers:
    def __init__(self, root):
        self.window = root
        self.controllers = []
        self.update_root(self.window)
        self.up = None
        self.down = None
        self.emulator = None
        self.index = None
        self.len_roms = None

    def update_root(self, root):
        self.window = root
        pygame.init()
        self.controllers = []
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
                mednafen_controller_config(device_dict, device_name)

    def find_events(self):
        events = pygame.event.get()
        if pygame.joystick.get_count() < 1:
            return

        for joystick in self.controllers:
            joystick.init()
            joy_axis_x = joystick.get_axis(2)
            joy_axis_y = joystick.get_axis(3)
            joy_a = joystick.get_button(0)
            joy_b = joystick.get_button(1)
            joy_x = joystick.get_button(2)
            joy_y = joystick.get_button(3)
            joy_lb = joystick.get_button(4)
            joy_rb = joystick.get_button(5)
            joy_lt = joystick.get_button(6)
            joy_rt = joystick.get_button(7)

            # noinspection PyBroadException
            try:
                if self.window.focus_get():
                    for event in events:
                        if event.type == pygame.JOYBUTTONDOWN:
                            if joy_a == 1:
                                self.window.focus_get().invoke()
                            if joy_b == 1:
                                back_to_menu()
                            if joy_lt == 1:
                                self.window.event_generate('<<LT>>')
                            if joy_rt == 1:
                                self.window.event_generate('<<RT>>')
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

