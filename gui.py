# file --gui.py--
from tkinter import *
from tkinter import messagebox

import filesystem as fs


# -----------------------------------------
# GUI
# -----------------------------------------
class ConfigMessageFrame(Frame):
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.master.title("Un MP, deux MPs, trois MPs...")

        self.build_frame()
        self.load_receivers()
        self.load_message()

        self.master.mainloop()

    def build_frame(self):
        # Receivers frame
        receivers_frame = Frame(self.master)
        receivers_frame.grid(row=0, column=0, padx=20)

        receivers_label = Label(receivers_frame, text="Destinataires")
        receivers_label.pack()

        self.receivers_Text = Text(receivers_frame, width=20)
        self.receivers_Text.pack()

        # Message frame
        message_frame = Frame(self.master)
        message_frame.grid(row=0, column=1, padx=20, pady=10)

        title_label = Label(message_frame, text="Sujet")
        title_label.pack()

        self.title_entry = Entry(message_frame, width=50)
        self.title_entry.pack()

        message_label = Label(message_frame, text="Message")
        message_label.pack()

        self.message_text = Text(message_frame, width=50)
        self.message_text.pack()

        # Buttons
        buttons_frame = Frame(self.master)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)

        save_button = Button(buttons_frame, text="Sauvegarder", command=self.save_everything)
        save_button.grid(row=0, column=0, padx=20)

        send_button = Button(buttons_frame, text="Envoyer", command=self.send_pm)
        send_button.grid(row=0, column=1, padx=20)

    def load_receivers(self):
        names_list = fs.load_receivers()
        self.receivers_Text.insert(CURRENT, names_list)

    def load_message(self):
        (title, message) = fs.load_message()
        self.title_entry.insert(INSERT, title)
        self.message_text.insert(CURRENT, message)

    def save_everything(self):
        names_list = self.receivers_Text.get(1.0, END).rstrip("\n")
        title = self.title_entry.get()
        message = self.message_text.get(1.0, END).strip("\n")

        fs.save_receivers(names_list)
        fs.save_message(title, message)

        messagebox.showinfo("C'est dans la boîte !", message="Sauvegarde effectuée")

    def send_pm(self):
        names_list = self.receivers_Text.get(1.0, END).rstrip("\n")
        title = self.title_entry.get()
        message = self.message_text.get(1.0, END).rstrip("\n")
        self.controller.send_pm(names_list, title, message)


class LoginFrame(Frame):
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

        ok_button = Button(main_frame, text="Connection", command=self.connect)
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