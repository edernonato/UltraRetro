from emulator import move_focus_down, move_focus_up, back_to_menu


def on_key_press(event):
    # print(event)
    if event.char.lower() == "s":
        move_focus_down()
    elif event.char.lower() == "w":
        move_focus_up()
    elif event.char.lower() == "b":
        back_to_menu()


