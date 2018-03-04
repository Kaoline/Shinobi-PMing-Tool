# file --frameopening.py--
from tkinter import *

from config import *


class FrameOpening(Frame):
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.master.title("Quel est le programme ?")
        self.build_frame()

        self.master.mainloop()

    def build_frame(self):
        main_frame = Frame(self.master)
        main_frame.grid()

        research_button = Button(main_frame, text="Faire une recherche", command=self.controller.show_search)
        research_button.grid(row=0, column=0, padx=20, pady=20)

        if Config.has_pm_access():
            pm_button = Button(main_frame, text="Envoyer un MP", command=self.controller.show_pmer)
            pm_button.grid(row=1, column=0, padx=20, pady=20)
