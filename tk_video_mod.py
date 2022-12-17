""" tkVideo: Python module for playing videos (without sound) inside tkinter Label widget using Pillow and imageio

Copyright © 2020 Xenofon Konitsas <konitsasx@gmail.com>
Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md

Edited by Eder Nonato <https://github.com/edernonato>

Added play_list function, to run a list of videos in sequence. Several changes made to handle some bugs in UltraRetro
 project
"""

try:
    import Tkinter as tk  # for Python2 (although it has already reached EOL)
except ImportError:
    import tkinter as tk  # for Python3
import threading
import imageio
from PIL import Image, ImageTk
import random


class tkvideo():
    """
        Main class of tkVideo. Handles loading and playing
        the video inside the selected label.

        :keyword path:
            Path of video file
        :keyword label:
            Name of label that will house the player
        :param loop:
            If equal to 0, the video only plays once,
            if not it plays in an infinite loop (default 0)
        :param size:
            Changes the video's dimensions (2-tuple,
            default is 640x360)


        IF using a list of videos:
        path = the path of the folder with the videos,
        video_list = is a list of STRINGS with the name of the videos files in that path
        Example =
            path = /home/videos
            rom_list = ["video1.mp4, "video2.mp4"]
            In this case instead of run tkvideo.play(), you should run tkvideo.play_list()

        FYI: "self.frames_to_display" is the number of frames that are going to be displayed before skipping to the next
        video in the list, if you want to display the entire video change the value to None
        e.g : if the frames_to_display is set to 300, there will be display only 300 frames of that video before
        skipping to the next

    """

    def __init__(self, path, label, loop=0, size=(640, 360), video_list=None, frames_to_display=None):
        self.path = path
        self.label = label
        self.loop = loop
        self.size = size
        self.frame_data = None
        self.should_return = False
        self.video_list = video_list
        self.frames_to_display = frames_to_display

    def load(self, path, label, loop):
        """
            Loads the video's frames recursively onto the selected label widget's image parameter.
            Loop parameter controls whether the function will run in an infinite loop
            or once.
        """
        frame_data = self.frame_data
        frame_data = imageio.get_reader(path)
        while not self.should_return:
            if loop == 1:
                while True:
                    for image in frame_data.iter_data():
                        frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(self.size))
                        label.config(image=frame_image)
                        label.image = frame_image
                    if self.should_return:
                        return
            else:
                for image in frame_data.iter_data():
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(self.size))
                    label.config(image=frame_image)
                    label.image = frame_image
                    if self.should_return:
                        return

    def play(self):
        """
            Creates and starts a thread as a daemon that plays the video by rapidly going through
            the video's frames.
        """
        thread = threading.Thread(target=self.load, args=(self.path, self.label, self.loop))
        thread.daemon = 1
        thread.start()

    def stop(self):
        self.should_return = True
        self.frame_data = None

    def play_list(self):
        """
                Example =
                    path = /home/videos
                    rom_list = ["video1.mp4, "video2.mp4"]
                    In this case instead of run tkvideo.play(), you should run tkvideo.play_list()
        """
        thread = threading.Thread(target=self.load_list, args=(self.path, self.video_list, self.label))
        thread.daemon = 1
        thread.start()

    def load_list(self, path, video_list, label):
        while not self.should_return:
            game_index = random.randint(0, len(video_list) - 1)
            reproduce = f"{path}/{video_list[game_index]}"
            frame_data = imageio.get_reader(reproduce)
            game_name = video_list[game_index].replace(".mp4", "").replace("-video", "")
            count = 0
            for image in frame_data.iter_data():
                count += 1
                frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(self.size))
                label.config(text=game_name, image=frame_image, compound='bottom', bg='black', fg='white')
                label.image = frame_image
                if self.frames_to_display is not None:
                    if count > self.frames_to_display:
                        self.load_list(path, video_list, label)
                if self.should_return:
                    return
