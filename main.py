import matplotlib
from tkinter import *
from emulator import create_emulators_list, window_type, generate_exit_button, DEFAULT_ULTRA_RETRO_PATH, move_focus_down, move_focus_up, back_to_menu
from start_window import initial_screen
# import pygame
# from controller import find_events

matplotlib.use('Agg')
BACKGROUND_COLOR = "Black"
window = Tk()
DEFAULT_BG = PhotoImage(file=f"{DEFAULT_ULTRA_RETRO_PATH}/Images/bg_img.png")
bg = DEFAULT_BG
label1 = Label(window, image=bg)
label1.place(x=0, y=0, relwidth=1, relheight=1)


def start():
    initial_screen(window)
    window_type(window)
    window.update()
    create_emulators_list()
    generate_exit_button()
    window.mainloop()
    # window.bind('<KeyPress>', on_key_press)
    # app = Find_Joystick(window)
    # window.bind('<KeyPress>', find_events)



# class Find_Joystick:
#     def __init__(self, root):
#         self.root = root
#
#         ## initialize pygame and joystick
#         pygame.init()
#         if(pygame.joystick.get_count() < 1):
#             # no joysticks found
#             print("Please connect a joystick.\n")
#             self.quit()
#         else:
#             # create a new joystick object from
#             # ---the first joystick in the list of joysticks
#             joystick = pygame.joystick.Joystick(0)
#             # tell pygame to record joystick events
#             joystick.init()
#
# def find_events():
#     global window
#
#     pygame.init()
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
#     pygame.init()
#     events = pygame.event.get()
#     joystick = pygame.joystick.Joystick(0)
#     axisX = joystick.get_axis(2)
#     axisY = joystick.get_axis(3)
#
#     A = joystick.get_button(0)
#     B = joystick.get_button(1)
#     X = joystick.get_button(2)
#     Y = joystick.get_button(3)
#     LB = joystick.get_button(4)
#     RB = joystick.get_button(5)
#     LT = joystick.get_button(6)
#     RT = joystick.get_button(7)
#
#     for event in events:
#         print(event)
#         # event type for pressing any of the joystick buttons down
#         if event.type == pygame.JOYBUTTONDOWN:
#             if A == 1:
#                 window.focus_get().invoke()
#             if LT == 1:
#                 window.event_generate('<<LT>>')
#             if RT == 1:
#                 window.event_generate('<<RT>>')
#
#         if event.type == pygame.JOYHATMOTION:
#             hats = joystick.get_numhats()
#             for i in range(hats):
#                 hat = joystick.get_hat(i)
#                 print(f"HAT ======= {hat}")
#                 if hat == (0, -1):
#                     move_focus_down()
#                 elif hat == (0, 1):
#                     move_focus_up()
#     window.after(1, find_events)


start()

