# file --gui.py--
from tkinter import *
from tkinter import messagebox

import filesystem as fs


# -----------------------------------------
# GUI
# -----------------------------------------
waiting_message = "Opération en cours... Ça peut être long, et ça bloque la fenêtre."


class OpeningFrame(Frame):
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

        pm_button = Button(main_frame, text="Envoyer un MP", command=self.controller.show_pmer)
        pm_button.grid(row=1, column=0, padx=20, pady=20)


class SearchingFrame(Frame):
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.time_estimation = StringVar()
        self.search_state = StringVar()

        self.master.title("Où sont les shinobis ?")
        self.build_frame()

        self.master.mainloop()

    def build_frame(self):
        # Options frame
        options_frame = Frame(self.master)
        options_frame.grid(row=0, rowspan=2, column=0, padx=20)

        self.build_options(options_frame)

        # File frame
        file_frame = Frame(self.master)
        file_frame.grid(row=0, column=1, padx=20, pady=10)

        Label(file_frame, text="Nom du fichier de sauvegarde : ").pack(side=LEFT)

        self.file_entry = Entry(file_frame, width=20)
        self.file_entry.pack(side=LEFT)
        self.file_entry.insert(0, "Shinobis.txt")

        # Results frame
        result_frame = Frame(self.master)
        result_frame.grid(row=1, column=1, padx=20, pady=10)

        Label(result_frame, text="Résultats").pack()

        self.result_text = Text(result_frame, width=30)
        self.result_text.pack()

        # Buttons frame
        buttons_frame = Frame(self.master)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)

        Label(buttons_frame, text="Temps estimé à la grosse louche (secondes) :").pack()
        Label(buttons_frame, textvariable=self.time_estimation).pack()

        Button(buttons_frame, text="Rechercher", command=self.search).pack()

        Label(buttons_frame, textvariable=self.search_state).pack()

    def build_options(self, options_frame):
        padding=5
        margin=5
        border_color="black"
        border_width=1

        # Label
        Label(options_frame, text="Options de recherche").pack()

        # Border
        options_sub_frame = Frame(options_frame, width=20)
        options_sub_frame.pack()

        # Pages
        pages_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        pages_frame.pack(padx=padding, pady=padding, fill=X)

        Label(pages_frame, text="Pages ").pack(side=LEFT, anchor=CENTER)

        self.start_page_value = StringVar()
        self.start_page_value.trace("w", lambda *args: self.estimate_time())
        Entry(pages_frame, textvariable=self.start_page_value, width=5).pack(side=LEFT)

        Label(pages_frame, text=" à ").pack(side=LEFT)

        self.end_page_value = StringVar()
        self.end_page_value.trace("w", lambda *args: self.estimate_time())
        Entry(pages_frame, textvariable=self.end_page_value, width=5).pack(side=LEFT)

        self.start_page_value.set("1")
        self.end_page_value.set("100")

        # Ranking
        ranking_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        ranking_frame.pack(padx=padding, pady=padding, fill=X)

        Label(ranking_frame, text="Classement").pack(side="left")

        self.ranking_choice = StringVar()
        self.ranking_choice.set("general")
        Radiobutton(ranking_frame, text="Général", variable=self.ranking_choice, value="general").pack(anchor=W)
        Radiobutton(ranking_frame, text="Hebdomadaire", variable=self.ranking_choice, value="weekly").pack(anchor=W)

        # Level
        level_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        level_frame.pack(padx=padding, pady=padding, fill=X)

        Label(level_frame, text="Niveau ").pack(side=LEFT)

        self.start_level_entry = Entry(level_frame, width=5)
        self.start_level_entry.pack(side=LEFT)
        self.start_level_entry.insert(0, 1)

        Label(level_frame, text=" à ").pack(side=LEFT)

        self.end_level_entry = Entry(level_frame, width=5)
        self.end_level_entry.pack(side=LEFT)
        self.end_level_entry.insert(0, 100)

        # Village
        village_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        village_frame.pack(padx=padding, pady=padding, fill=X)

        Label(village_frame, text="Classement\nvillage").pack(side="left")

        self.village_choice = StringVar()
        self.village_choice.set("all")
        Radiobutton(village_frame, text="Tous", variable=self.village_choice, value="all").pack(anchor=W)
        Radiobutton(village_frame, text="Chikara", variable=self.village_choice, value="chikara").pack(anchor=W)
        Radiobutton(village_frame, text="Mahou", variable=self.village_choice, value="mahou").pack(anchor=W)
        Radiobutton(village_frame, text="Gensou", variable=self.village_choice, value="gensou").pack(anchor=W)

        # Score
        score_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        score_frame.pack(padx=padding, pady=padding, fill=X)

        Label(score_frame, text="Points minimum : ").pack(side=LEFT)

        self.start_score_entry = Entry(score_frame, width=7)
        self.start_score_entry.pack(side=LEFT)
        self.start_score_entry.insert(0, 0)

        # Evo
        evo_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        evo_frame.pack(padx=padding, pady=padding, fill=X)

        Label(evo_frame, text="Evo de ").pack(side=LEFT)

        self.start_evo_entry = Entry(evo_frame, width=7)
        self.start_evo_entry.pack(side=LEFT)
        self.start_evo_entry.insert(0, 0)

        Label(evo_frame, text=" à ").pack(side=LEFT)

        self.end_evo_entry = Entry(evo_frame, width=7)
        self.end_evo_entry.pack(side=LEFT)
        self.end_evo_entry.insert(0, 99999)

    def estimate_time(self):
        try:
            min_page = int(self.start_page_value.get())
            max_page = int(self.end_page_value.get())
            pages = max_page - min_page + 1
            time = pages / 20 if pages <= 1000 else pages / 10
            self.time_estimation.set(str(time))
        except ValueError:
            print()

    def search(self):
        def callback():
            result = self.controller.search_ranking(
                file=self.file_entry.get(),
                ranking=self.ranking_choice.get(),
                min_page=int(self.start_page_value.get()),
                max_page=int(self.end_page_value.get()),
                min_lvl=int(self.start_level_entry.get()),
                max_lvl=int(self.end_level_entry.get()),
                village=self.village_choice.get() if self.village_choice.get() != "all" else None,
                min_evo=int(self.start_evo_entry.get()),
                max_evo=int(self.end_evo_entry.get()),
                min_points=int(self.start_score_entry.get())
            )
            self.search_state.set("")
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, "\n".join(result))
            messagebox.showinfo("Fini !", "Recherche effectuée.\nJ'ai trouvé " + str(len(result)) + " shinobis !")

        self.search_state.set(waiting_message)
        self.after(10, callback)


class ConfigMessageFrame(Frame):
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

        # Buttons
        buttons_frame = Frame(self.master)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)

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
            self.controller.send_pm(receivers, title, message)
            self.send_state.set("")
            messagebox.showinfo("Fini !", "Message envoyé aux " + str(len(receivers)) + " shinobis.")

        self.send_state.set(waiting_message)
        self.after(10, callback)


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
