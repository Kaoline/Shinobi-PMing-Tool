# file --framelogin.py--
from tkinter import *

from config import *


class FrameLogin(Frame):
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.connect_account = StringVar()
        self.connect_account.set("-1")
        self.save_account = BooleanVar(False)

        self.master.title("Qui êtes-vous ?")

        self.build_frame()

        self.master.mainloop()

    def build_frame(self):
        main_frame = Frame(self.master)
        main_frame.grid(padx=20, pady=10)

        radio_frame = Frame(main_frame)
        radio_frame.grid(row=0, columnspan=2)
        for login in Config.accounts:
            b = Radiobutton(radio_frame, text=login, variable=self.connect_account, value=login)
            b.pack(anchor=W)
        Radiobutton(radio_frame, text="Autre compte", variable=self.connect_account, value="-1").pack(anchor=W)

        login_label = Label(main_frame, text="Login :")
        login_label.grid(row=1, column=0, padx=10, stick="E")

        self.login_entry = Entry(main_frame)
        self.login_entry.grid(row=1, column=1)

        password_label = Label(main_frame, text="Mot de passe :")
        password_label.grid(row=2, column=0, padx=10, pady=10, stick="E")

        self.password_entry = Entry(main_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)

        save_account_cb = Checkbutton(main_frame, text="Garder cet autre compte en mémoire", variable=self.save_account)
        save_account_cb.grid(row=3, columnspan=2)

        ok_button = Button(main_frame, text="Connexion", command=self.connect)
        ok_button.grid(row=5, columnspan=2)

        self.error_label = Label(main_frame, fg="red")
        self.error_label.grid(row=4, columnspan=2)

    def connect(self):
        login = self.connect_account.get()
        new_acc = login == "-1"
        if not new_acc:
            password = Config.accounts[login]
        else:
            login = self.login_entry.get()
            password = self.password_entry.get()

        connected = self.controller.connect(login, password)
        if connected:
            if new_acc and self.save_account.get():
                Config.add_account(login, password)
            self.master.quit()
        else:
            self.error_label.configure(text="Problème d'identifiants, veuillez réessayer.")