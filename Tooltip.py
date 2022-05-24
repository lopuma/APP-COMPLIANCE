import tkinter as tk

class CustomHovertip(tk.Toplevel):
    def __init__(self, boton, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text.split()
        self.wm_overrideredirect(1)
        self.position_window(boton)

    def showcontents(self):
        label = tk.Label(
            self, 
            text=self.text, 
            bg="#151515", 
            fg="#ffffff",             
            font=("conforta", 13)
            )
        label.pack(expand=1, fill=tk.BOTH)

    def position_window(self, boton):
        x, y = self.get_position(boton)
        root_x = boton.winfo_rootx() + x
        root_y = boton.winfo_rooty() + y
        self.wm_geometry("+%d+%d" % (root_x, root_y))
        self.showcontents()

    def get_position(self, boton):
        return 20, boton.winfo_height() + 1
