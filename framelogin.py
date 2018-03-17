# file --framelogin.py--
from tkinter import *


class FrameLogin(Frame):
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.master.title("Qui êtes-vous ?")

        self.build_frame()

        self.master.mainloop()

    def build_frame(self):
        main_frame = Frame(self.master)
        main_frame.grid(padx=20, pady=10)

        login_label = Label(main_frame, text="Login :")
        login_label.grid(row=0, column=0, padx=10, stick="E")

        self.login_entry = Entry(main_frame)
        self.login_entry.grid(row=0, column=1)

        password_label = Label(main_frame, text="Mot de passe :")
        password_label.grid(row=1, column=0, padx=10, pady=10, stick="E")

        self.password_entry = Entry(main_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        ok_button = Button(main_frame, text="Connexion", command=self.connect)
        ok_button.grid(row=2, columnspan=2)

        self.error_label = Label(main_frame, fg="red")
        self.error_label.grid(row=3, columnspan=2)

    def connect(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        connected = self.controller.connect(login, password)
        if connected:
            self.master.quit()
        else:
            self.error_label.configure(text="Problème d'identifiants, veuillez réessayer.")