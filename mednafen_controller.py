from emulator import DEFAULT_ULTRA_RETRO_PATH
import json

# In order to configure the mednafen emulator controls, we need to get same information about the hardware information
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
# The Axes and Button count were extracted from pygame.Joystick


global controller_mednafen_guid
with open("/proc/bus/input/devices", "r") as f:
    devices_file = f.read()  # read everything in the file
    f.seek(0)  # rewind

devices_file_lines = devices_file.split("\n\n")


# Function used to generate the mednafen GUID String. Variable named 'device'.
def mednafen_controller_config(device_dict, device_name):
    global controller_mednafen_guid
    controller_mednafen_guid = []
    for line in range(len(devices_file_lines)):
        device_name = device_name.replace(" ", "")
        if device_name in devices_file_lines[line].replace(" ", ""):
            device_info = devices_file_lines[line].split("\n")
            bus_vendor_product = device_info[0]
            new_bus_vendor_product = bus_vendor_product.split(" ")
            bus = new_bus_vendor_product[1].replace("Bus=", "")
            vendor = new_bus_vendor_product[2].replace("Vendor=", "")
            product = new_bus_vendor_product[3].replace("Product=", "")
            version = new_bus_vendor_product[4].replace("Version=", "")
            name = device_info[1].replace("N: Name=", "")
            device_dict["name"] = name
            device_dict["bus"] = bus
            device_dict["vendor"] = vendor
            device_dict["product"] = product
            device_dict["version"] = version
            device_dict["index"] = "00000000"
            if device_dict:
                device = f'0x{device_dict["bus"]}{device_dict["vendor"]}{device_dict["product"]}' \
                         f'{device_dict["version"]}000{device_dict["numaxis"]}' \
                         f'{device_dict["numbuttons"]}{device_dict["index"]}'
                controller_mednafen_guid.append(device)
            else:
                device = ''
            for device in controller_mednafen_guid:
                print(device)

            # The code verifies if there is some control information on controllers.cfg, if there is, the control
            # information is set into the mednafen.cfg file for each emulator and the keys are set to default inside
            # UltraRetro

            buttons_mednafen = {}
            # noinspection PyBroadException
            try:
                controllers_file = open(f"{DEFAULT_ULTRA_RETRO_PATH}/controllers.cfg")
                data = json.load(controllers_file)
                for i in data['controllers']:
                    if device_name == data['controllers'][0]["controller"].replace(" ", ""):
                        for button in i:
                            if button == 'a':
                                joy_a = i[button]
                                buttons_mednafen["a"] = f"button_{joy_a}"
                                buttons_mednafen["rapid_a"] = f"button_{joy_a}"
                                buttons_mednafen["circle"] = f"button_{joy_a}"
                                buttons_mednafen["fire1"] = f"button_{joy_a}"
                            if button == 'b':
                                joy_b = i[button]
                                buttons_mednafen["b"] = f"button_{joy_b}"
                                buttons_mednafen["rapid_b"] = f"button_{joy_b}"
                                buttons_mednafen["cross"] = f"button_{joy_b}"
                                buttons_mednafen["fire2"] = f"button_{joy_b}"

                            if button == 'x':
                                joy_x = i[button]
                                buttons_mednafen["x"] = f"button_{joy_x}"
                                buttons_mednafen["rapid_x"] = f"button_{joy_x}"
                                buttons_mednafen["triangle"] = f"button_{joy_x}"
                                joy_c = i[button]
                                buttons_mednafen["c"] = f"button_{joy_c}"
                                buttons_mednafen["rapid_c"] = f"button_{joy_c}"
                            if button == 'y':
                                joy_y = i[button]
                                buttons_mednafen["y"] = f"button_{joy_y}"
                                buttons_mednafen["square"] = f"button_{joy_y}"
                                buttons_mednafen["rapid_y"] = f"button_{joy_y}"
                            if button == 'l':
                                joy_lb = i[button]
                                buttons_mednafen["l"] = f"button_{joy_lb}"
                                buttons_mednafen["l1"] = f"button_{joy_lb}"
                                buttons_mednafen["shoulder_l"] = f"button_{joy_lb}"
                            if button == 'r':
                                joy_rb = i[button]
                                buttons_mednafen["r"] = f"button_{joy_rb}"
                                buttons_mednafen["r1"] = f"button_{joy_rb}"
                                buttons_mednafen["shoulder_r"] = f"button_{joy_rb}"
                            if button == 'lt':
                                joy_lt = i[button]
                                buttons_mednafen["lt"] = f"button_{joy_lt}"
                                buttons_mednafen["l2"] = f"button_{joy_lt}"
                            if button == 'rt':
                                joy_rt = i[button]
                                buttons_mednafen["rt"] = f"button_{joy_rt}"
                                buttons_mednafen["r2"] = f"button_{joy_rt}"
                            if button == 'start':
                                joy_start = i[button]
                                buttons_mednafen["start"] = f"button_{joy_start}"
                                buttons_mednafen["pause"] = f"button_{joy_start}"
                            if button == 'select':
                                joy_select = i[button]
                                buttons_mednafen["select"] = f"button_{joy_select}"
                            buttons_mednafen["up"] = "abs_6-"
                            buttons_mednafen["down"] = "abs_6+"
                            buttons_mednafen["left"] = "abs_5-"
                            buttons_mednafen["right"] = "abs_5+"
                print(buttons_mednafen)

                with open("/root/.mednafen/mednafen.cfg", "r+") as file:
                    old = file.read()
                emulator_list = ["md", "snes", "psx", "gba", "nes", "sms", "lynx", "ss", "wswan", "gb", "gg"]
                # button_list = ["a", "b", "c", "down", "left", "right", "up", "start", "l", "r", "x", "y", "select"]
                old_list = old.split("\n")
                for mednafen_line in old_list:
                    words = mednafen_line.split(" ")
                    for word in range(len(words)):
                        for button in buttons_mednafen:
                            for emulator in emulator_list:
                                switch_button = False
                                new_button = ""
                                if words[word] == f"{emulator}.input.port1.gamepad.{button}":
                                    new_button = f"{emulator}.input.port1.gamepad.{button} joystick {device} " \
                                                 f"{buttons_mednafen[button]}"
                                    switch_button = True
                                elif words[word] == f"{emulator}.input.builtin.gamepad.{button}":
                                    new_button = f"{emulator}.input.builtin.gamepad.{button} joystick {device}" \
                                                 f" {buttons_mednafen[button]}"
                                    switch_button = True
                                if switch_button:
                                    with open("/root/.mednafen/mednafen.cfg", "r+") as file_write:
                                        old_file = file_write.read()  # read everything in the file
                                        file_write.seek(0)  # rewind
                                        new_mednafen_file = old_file.replace(mednafen_line, new_button)
                                        file_write.write(new_mednafen_file)

            except Exception:
                pass
