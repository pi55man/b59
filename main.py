import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog


class App():
    def __init__(self, title="photo editor", color="gray"):
        self.app = tk.Tk()
        self.app.title(title)
        self.app.geometry("800x600")
        self.app.resizable(width=True, height=True)
        self.app.configure(background=color)

    def keybind(self, key, operation):
        self.app.bind(key, operation)

    def run(self):
        self.app.mainloop()

    def close(self):
        self.app.destroy()


app = App()
# close app by pressing escape
app.keybind("<Escape>", app.close())



app.run()
