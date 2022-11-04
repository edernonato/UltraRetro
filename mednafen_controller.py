
global controller_mednafen_guid
with open("/proc/bus/input/devices", "r") as f:
    old = f.read()  # read everything in the file
    f.seek(0)  # rewind

new = old.split("\n\n")


def mednafen_controller_config(device_dict, device_name):
    global controller_mednafen_guid
    controller_mednafen_guid = []
    for line in range(len(new)):
        device_name = device_name.replace(" ", "")
        if device_name in new[line].replace(" ", ""):
            device_info = new[line].split("\n")
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
            for device in controller_mednafen_guid:
                print(device)
