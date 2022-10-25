# # from handle_keys import move_focus_up, move_focus_down, back_to_menu
# import pygame
# from functools import partial
#
#
# global window
#
#
# def find_events(root):
#     global window
#     window = root
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
#     # for i in range(joystick.get_numbuttons()):
#     #     print(i)
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
#     recursive_call = partial(find_events, window)
#     window.after(1, recursive_call)
