from functools import partial
import tkinter as tk
class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        for row in range(0, 20):
            for column in range(0, 40):
                new_button = tk.Button(self, text="")
                new_button.grid(row=row, column=column)
                new_button["command"] = partial(self.press, new_button)
    def press(self, btn):
        btn.configure(bg="gold")
        btn.configure(activebackground="gold")
if __name__ == "__main__":
    root = tk.Tk()
    MainFrame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()