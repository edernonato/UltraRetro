import json
from threading import Thread
from functools import partial
import os
import time

"""In order to configure the mednafen emulator controls, we need to get same information about the hardware information
# of the joysticks connected, so we can create the mednafen GUID inside the mednafen.cfg
#
# The structure of the ID is:
# 0x0003054c05c481110008000d00000000
#
# The first two digits are default 0x
# The next 4 digits are related to the device Bus
# The next 4 digits are related to the device Vendor
# The next 4 digits are related to the device Product
# The next 4 digits are related to the device Version
# The next 4 digits are related to the device Axes Count
# The next 4 digits are related to the device Button Count
# The next 8 digits are related to the device Index. It is the index the mednafen create, its 0000000 for default.
#
# Bus, vendor, product and version information were extracted from the system file: /proc/bus/input/devices
# The Axes and Button count were extracted from pygame.Joystick"""


class Mednafen:
    def __init__(self, device_dict, device_name, controller_number, emulator_instance):
        self.start_time = time.time()
        self.device_file = None
        self.device_dict = device_dict
        self.device_name = device_name
        self.controller_number = controller_number
        self.emulator_instance = emulator_instance
        self.devices_file_lines = None
        self.read_device_file()
        self.device_uid = None
        self.buttons_mednafen = {}
        self.mednafen_controller_config()

    def read_device_file(self):
        with open("/proc/bus/input/devices", "r") as f:
            devices_file = f.read()  # read everything in the file
            f.seek(0)  # rewind
        self.devices_file_lines = devices_file.split("\n\n")

# Function used to generate the mednafen GUID String. Variable named 'device'.
    def mednafen_controller_config(self):
        self.emulator_instance.generate_controller_configuration_label()
        self.emulator_instance.configuring_controllers = True
        controller_mednafen_guid = []
        for line in range(len(self.devices_file_lines)):
            self.device_name = self.device_name.replace(" ", "")
            if self.device_name in self.devices_file_lines[line].replace(" ", ""):
                device_info = self.devices_file_lines[line].split("\n")
                bus_vendor_product = device_info[0]
                new_bus_vendor_product = bus_vendor_product.split(" ")
                bus = new_bus_vendor_product[1].replace("Bus=", "")
                vendor = new_bus_vendor_product[2].replace("Vendor=", "")
                product = new_bus_vendor_product[3].replace("Product=", "")
                version = new_bus_vendor_product[4].replace("Version=", "")
                name = device_info[1].replace("N: Name=", "")
                self.device_dict["name"] = name
                self.device_dict["bus"] = bus
                self.device_dict["vendor"] = vendor
                self.device_dict["product"] = product
                self.device_dict["version"] = version
                self.device_dict["index"] = "00000000"
                if self.device_dict:
                    self.device_uid = f'0x{self.device_dict["bus"]}{self.device_dict["vendor"]}' \
                                      f'{self.device_dict["product"]}' \
                                      f'{self.device_dict["version"]}000{self.device_dict["numaxis"]}' \
                                      f'{self.device_dict["numbuttons"]}{self.device_dict["index"]}'
                    controller_mednafen_guid.append(self.device_uid)
                else:
                    self.device_uid = ''
                new_thread = Thread(target=self.get_buttons_from_controllers_file)
                new_thread.start()

    # The function verifies if there is some control information on controllers.cfg, if there is, the control
    # information is set into the mednafen.cfg file for each emulator and the keys are set to default inside
    # UltraRetro
    def get_buttons_from_controllers_file(self):
        # noinspection PyBroadException
        try:
            controllers_file = open(f"{self.emulator_instance.DEFAULT_ULTRA_RETRO_PATH}/controllers.cfg")
            data = json.load(controllers_file)
            for i in data['controllers']:
                index = data['controllers'].index(i)
                if self.device_name == data['controllers'][index]["controller"].replace(" ", ""):
                    for button in i:
                        if button == 'a':
                            joy_a = i[button]
                            self.buttons_mednafen["a"] = f"button_{joy_a}"
                            self.buttons_mednafen["rapid_a"] = f"button_{joy_a}"
                            self.buttons_mednafen["circle"] = f"button_{joy_a}"
                            self.buttons_mednafen["fire1"] = f"button_{joy_a}"
                        if button == 'b':
                            joy_b = i[button]
                            self.buttons_mednafen["b"] = f"button_{joy_b}"
                            self.buttons_mednafen["rapid_b"] = f"button_{joy_b}"
                            self.buttons_mednafen["cross"] = f"button_{joy_b}"
                            self.buttons_mednafen["fire2"] = f"button_{joy_b}"

                        if button == 'x':
                            joy_x = i[button]
                            self.buttons_mednafen["x"] = f"button_{joy_x}"
                            self.buttons_mednafen["rapid_x"] = f"button_{joy_x}"
                            self.buttons_mednafen["triangle"] = f"button_{joy_x}"
                            joy_c = i[button]
                            self.buttons_mednafen["c"] = f"button_{joy_c}"
                            self.buttons_mednafen["rapid_c"] = f"button_{joy_c}"
                        if button == 'y':
                            joy_y = i[button]
                            self.buttons_mednafen["y"] = f"button_{joy_y}"
                            self.buttons_mednafen["square"] = f"button_{joy_y}"
                            self.buttons_mednafen["rapid_y"] = f"button_{joy_y}"
                        if button == 'l':
                            joy_lb = i[button]
                            self.buttons_mednafen["l"] = f"button_{joy_lb}"
                            self.buttons_mednafen["l1"] = f"button_{joy_lb}"
                            self.buttons_mednafen["shoulder_l"] = f"button_{joy_lb}"
                        if button == 'r':
                            joy_rb = i[button]
                            self.buttons_mednafen["r"] = f"button_{joy_rb}"
                            self.buttons_mednafen["r1"] = f"button_{joy_rb}"
                            self.buttons_mednafen["shoulder_r"] = f"button_{joy_rb}"
                        if button == 'lt':
                            joy_lt = i[button]
                            self.buttons_mednafen["lt"] = f"button_{joy_lt}"
                            self.buttons_mednafen["l2"] = f"button_{joy_lt}"
                        if button == 'rt':
                            joy_rt = i[button]
                            self.buttons_mednafen["rt"] = f"button_{joy_rt}"
                            self.buttons_mednafen["r2"] = f"button_{joy_rt}"
                        if button == 'start':
                            joy_start = i[button]
                            self.buttons_mednafen["start"] = f"button_{joy_start}"
                            self.buttons_mednafen["pause"] = f"button_{joy_start}"
                        if button == 'select':
                            joy_select = i[button]
                            self.buttons_mednafen["select"] = f"button_{joy_select}"
                        self.buttons_mednafen["up"] = "abs_6-"
                        self.buttons_mednafen["down"] = "abs_6+"
                        self.buttons_mednafen["left"] = "abs_5-"
                        self.buttons_mednafen["right"] = "abs_5+"

            user = os.popen('whoami').read()
            if user.replace("\n", "") == "root":
                mednafen_dir = "/root/.mednafen"
            else:
                mednafen_dir = f"/home/{user}/.mednafen".replace("\n", "")
            with open(f"{mednafen_dir}/mednafen.cfg", "r+") as file:
                print("OPENING FILE")
                old = file.read()
            old_list = old.split("\n")

            for mednafen_line in old_list:
                task = partial(self.save_data_mednafen_file, mednafen_line)
                new_thread = Thread(target=task)
                new_thread.start()

            print("My program took", time.time() - self.start_time, "to run")
            self.emulator_instance.remove_controller_configuration_label()
            self.emulator_instance.configuring_controllers = False

        except Exception:
            print(Exception)
            pass

    def save_data_mednafen_file(self, mednafen_line):
        emulator_list = ["md", "snes", "psx", "gba", "nes", "sms", "lynx", "ss", "wswan", "gb", "gg"]

        # noinspection PyBroadException
        try:
            words = mednafen_line.split(" ")
            for word in range(len(words)):
                for emulator in emulator_list:
                    for button in self.buttons_mednafen:
                        switch_button = False
                        new_button = ""
                        # print(words[word])
                        if words[word] == f"{emulator}.input.port{self.controller_number}.gamepad.{button}":
                            new_button = f"{emulator}.input.port{self.controller_number}.gamepad.{button}" \
                                         f" joystick {self.device_uid} {self.buttons_mednafen[button]}"
                            switch_button = True
                        if self.controller_number == 1:
                            if words[word] == f"{emulator}.input.builtin.gamepad.{button}":
                                new_button = f"{emulator}.input.builtin.gamepad.{button} joystick {self.device_uid}" \
                                             f" {self.buttons_mednafen[button]}"
                                switch_button = True
                        if switch_button:
                            user = os.popen('whoami').read()
                            user = user.replace("\n", "")
                            if user == "root":
                                mednafen_dir = "/root/.mednafen"
                            else:
                                mednafen_dir = f"/home/{user}/.mednafen".replace("\n", "")
                            with open(f"{mednafen_dir}/mednafen.cfg", "r+") as file_write:
                                old_file = file_write.read()  # read everything in the file
                                file_write.seek(0)  # rewind
                                new_mednafen_file = old_file.replace(mednafen_line, new_button)
                                file_write.write(new_mednafen_file)
                                # print(new_button)
        except Exception:
            print("ERROR")
            pass
