from tkinter import *


def initial_screen(window):
    window.title("UltraRetro")
    window.geometry("1920x1080")
    window.config(padx=0, pady=0, background="White")


def generate_exit_button(window):
    exit_button = Button(fg="white", width=30, height=5, text="Exit", font=("Arial", 8, "italic"),
                         highlightcolor="White", highlightthickness=0, bg="Black",
                         command=window.destroy)
    exit_button.grid(row=3, column=0, columnspan=2, pady=10)
