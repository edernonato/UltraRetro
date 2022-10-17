from tkinter import *

import os
BACKGROUND_COLOR = "Black"


def access_emulator():
    print(f"Opening ")
    os.system('mednafen /home/eder/roms/mega/SOR.zip')


window = Tk()
window.title("UltraRetro")
window.attributes("-fullscreen", True)
window.config(padx=0, pady=0, background=BACKGROUND_COLOR)

bg = PhotoImage(file="images/bg_img.png")
label1 = Label(window, image=bg)
label1.place(x=0, y=0)

# mega_drive = Canvas(width=200, height=100, highlightthickness=0, border=0, background="Black")
# mega_drive.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
# mega_drive.create_text(100, 50, fill='white')
mega_drive_button = Button(fg="white", width=30, height=5, text="MEGA DRIVE", font=("Arial", 12, "italic"), highlightcolor="White", highlightthickness=0, bg="Black", command=access_emulator)
mega_drive_button.grid(row=0, column=0, columnspan=2)

snes_button = Button(fg="white", width=30, height=5, text="SUPER NINTENDO", font=("Arial", 12, "italic"), highlightcolor="White", highlightthickness=0, bg="Black", command=access_emulator)
snes_button.grid(row=1, column=0, columnspan=2)

# snes = Canvas(width=200, height=100, highlightthickness=0, border=0, background="Black")
# snes.create_text(100, 50, text="SUPER NINTENDO", font=("Arial", 16, "italic"), fill='white')
# snes.grid(row=1, column=0, columnspan=2, padx=10, pady=10)





window.mainloop()

