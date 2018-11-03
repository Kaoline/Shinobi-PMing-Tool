# file --gui.py--
from tkinter import *
from tkinter import messagebox

import filesystem as fs
import constants


class FrameConfigMessage(Frame):
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller
        self.send_state = StringVar()

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

        pseudo_info = Label(message_frame, text="La variable %pseudo% sera remplacée par le pseudo du destinataire dans le message et/ou le sujet !")
        pseudo_info.pack(pady=20)

        # Buttons
        buttons_frame = Frame(self.master)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=20)

        save_button = Button(buttons_frame, text="Sauvegarder", command=self.save_everything)
        save_button.grid(row=0, column=0, padx=20)

        send_button = Button(buttons_frame, text="Envoyer", command=self.send_pm)
        send_button.grid(row=0, column=1, padx=20)

        Label(buttons_frame, textvariable=self.send_state).grid(columnspan=2)

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
        def callback():
            names_list = self.receivers_Text.get(1.0, END).rstrip("\n")
            title = self.title_entry.get()
            message = self.message_text.get(1.0, END).rstrip("\n")

            receivers = names_list.split("\n")
            moles = fs.load_moles().split("\n")
            receivers = [x for x in receivers if x not in moles]
            success = self.controller.send_pm(receivers, title, message, self)
            self.send_state.set("")
            if success:
                messagebox.showinfo("Fini !", "Message envoyé aux " + str(len(receivers)) + " shinobis.")
            else:
                messagebox.showinfo("Erreur", "Le message n'a pas été envoyé. Est-ce normal ?")

        self.send_state.set(constants.waiting_message)
        self.after(10, callback)