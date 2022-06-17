import tkinter as tk
from RadiusButton import CornerRadius

class CustomHovertip(tk.Toplevel):
    y_alto_btn = 45
    x_ancho_btn = 180
    hg_btn = int(y_alto_btn-15)
    wd_btn = int(x_ancho_btn-20)
    def __init__(self, boton, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text.split()
        self.config(borderwidth=2, background="gray77")
        self.wm_overrideredirect(1)
        self.position_window(boton)

    def showcontents(self):
        # self.frame_label = CornerRadius(
        #     self,
        #     alto=self.y_alto_btn,
        #     ancho=self.x_ancho_btn,
        #     radio=25,
        #     width=2,
        #     bg_color="#151515",
        # )
        label = tk.Label(
#            self.frame_label,
            self,
            text=self.text,
            bg="#151515",
            fg="#ffffff",
            font=("Noto Mono", 13)
            )
        label.pack(expand=1, fill=tk.BOTH)
        # label.place(
        #     relx=0.5,
        #     rely=0.5,
        #     anchor=tk.CENTER,
        #     height=self.hg_btn,
        #     width=self.wd_btn,
        # )
        # self.frame_label.pack(expand=1, fill=tk.BOTH)

    def position_window(self, boton):
        x, y = self.get_position(boton)
        root_x = boton.winfo_rootx() + x
        root_y = boton.winfo_rooty() + y
        self.wm_geometry("+%d+%d" % (root_x, root_y))
        self.showcontents()

    def get_position(self, boton):
        return 20, boton.winfo_height() + 1
