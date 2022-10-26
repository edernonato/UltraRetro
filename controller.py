import pygame
from emulator import move_focus_down, move_focus_up, back_to_menu


class JoystickControllers:
    def __init__(self, root):
        self.window = root
        self.controllers = []
        self.update_root(self.window)

    def update_root(self, root):
        self.window = root
        self.controllers = []
        self.get_controllers()
        self.find_events()

    def get_controllers(self):
        pygame.init()
        for joy in range(pygame.joystick.get_count()):
            self.controllers.append(pygame.joystick.Joystick(joy))

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

                        if event.type == pygame.JOYHATMOTION:
                            hats = joystick.get_numhats()
                            for i in range(hats):
                                hat = joystick.get_hat(i)
                                if hat == (0, -1):
                                    move_focus_down()
                                elif hat == (0, 1):
                                    move_focus_up()
            except Exception:
                pass
        self.window.after(1, self.find_events)

