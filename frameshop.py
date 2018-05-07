# file --framesearching.py--
from tkinter import *
from tkinter import messagebox

import constants


class FrameShop(Frame):
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.time_estimation = StringVar()
        self.shop_state = StringVar()
        self.quantity = IntVar()
        self.price = IntVar()
        self.can_buy = StringVar()

        self.master.title("J'achète tout !")
        self.build_frame()

        self.master.mainloop()

    def build_frame(self):
        Label(self.master, text="Objet :").grid(row=0, column=0, padx=20)
        Label(self.master, text="Quantité").grid(row=0, column=1, padx=20)

        # Items frame
        items_frame = Frame(self.master)
        items_frame.grid(row=1, column=0, padx=20, pady=10)
        self.build_items(items_frame)

        # Quantity
        Entry(self.master, textvariable=self.quantity, width=5).grid(row=1, column=1)

        # Results frame
        result_frame = Frame(self.master)
        result_frame.grid(row=2, column=0, columnspan=2)
        self.build_results(result_frame)

    def build_items(self, items_frame):
        #TODO
        Label(items_frame, text="du vide").pack()
        # for login in Config.accounts:
        #     b = Radiobutton(radio_frame, text=login, variable=self.connect_account, value=login)
        #     b.pack(anchor=W)
        # Radiobutton(radio_frame, text="Autre compte", variable=self.connect_account, value="-1").pack(anchor=W)
        #
        # # Label
        # Label(items_frame, text="Options de recherche").pack()
        #
        # # Border
        # options_sub_frame = Frame(items_frame, width=20)
        # options_sub_frame.pack()
        #
        # # Pages
        # pages_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        # pages_frame.pack(padx=padding, pady=padding, fill=X)
        #
        # Label(pages_frame, text="Pages ").pack(side=LEFT, anchor=CENTER)
        #
        # self.start_page_value = StringVar()
        # self.start_page_value.trace("w", lambda *args: self.estimate_time())
        # Entry(pages_frame, textvariable=self.start_page_value, width=5).pack(side=LEFT)
        #
        # Label(pages_frame, text=" à ").pack(side=LEFT)
        #
        # self.end_page_value = StringVar()
        # self.end_page_value.trace("w", lambda *args: self.estimate_time())
        # Entry(pages_frame, textvariable=self.end_page_value, width=5).pack(side=LEFT)
        #
        # self.start_page_value.set("1")
        # self.end_page_value.set("100")
        #
        # # Ranking
        # ranking_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        # ranking_frame.pack(padx=padding, pady=padding, fill=X)
        #
        # Label(ranking_frame, text="Classement").pack(side="left")
        #
        # self.ranking_choice = StringVar()
        # self.ranking_choice.set("general")
        # Radiobutton(ranking_frame, text="Général", variable=self.ranking_choice, value="general").pack(anchor=W)
        # Radiobutton(ranking_frame, text="Hebdomadaire", variable=self.ranking_choice, value="weekly").pack(anchor=W)
        #
        # # Level
        # level_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        # level_frame.pack(padx=padding, pady=padding, fill=X)
        #
        # Label(level_frame, text="Niveau ").pack(side=LEFT)
        #
        # self.start_level_entry = Entry(level_frame, width=5)
        # self.start_level_entry.pack(side=LEFT)
        # self.start_level_entry.insert(0, 1)
        #
        # Label(level_frame, text=" à ").pack(side=LEFT)
        #
        # self.end_level_entry = Entry(level_frame, width=5)
        # self.end_level_entry.pack(side=LEFT)
        # self.end_level_entry.insert(0, 100)
        #
        # # Village
        # village_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        # village_frame.pack(padx=padding, pady=padding, fill=X)
        #
        # Label(village_frame, text="Classement\nvillage").pack(side="left")
        #
        # self.village_choice = StringVar()
        # self.village_choice.set("all")
        # Radiobutton(village_frame, text="Tous", variable=self.village_choice, value="all").pack(anchor=W)
        # Radiobutton(village_frame, text="Chikara", variable=self.village_choice, value="chikara").pack(anchor=W)
        # Radiobutton(village_frame, text="Mahou", variable=self.village_choice, value="mahou").pack(anchor=W)
        # Radiobutton(village_frame, text="Gensou", variable=self.village_choice, value="gensou").pack(anchor=W)
        #
        # # Score
        # score_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        # score_frame.pack(padx=padding, pady=padding, fill=X)
        #
        # Label(score_frame, text="Points minimum : ").pack(side=LEFT)
        #
        # self.start_score_entry = Entry(score_frame, width=7)
        # self.start_score_entry.pack(side=LEFT)
        # self.start_score_entry.insert(0, 0)
        #
        # # Evo
        # evo_frame = Frame(options_sub_frame, padx=margin, pady=margin, highlightbackground=border_color, highlightthickness=border_width)
        # evo_frame.pack(padx=padding, pady=padding, fill=X)
        #
        # Label(evo_frame, text="Evo de ").pack(side=LEFT)
        #
        # self.start_evo_entry = Entry(evo_frame, width=7)
        # self.start_evo_entry.pack(side=LEFT)
        # self.start_evo_entry.insert(0, 0)
        #
        # Label(evo_frame, text=" à ").pack(side=LEFT)
        #
        # self.end_evo_entry = Entry(evo_frame, width=7)
        # self.end_evo_entry.pack(side=LEFT)
        # self.end_evo_entry.insert(0, 99999)

    def build_results(self, result_frame):
        Label(result_frame, text="Prix : ").pack()
        Label(result_frame, textvariable=self.price).pack()
        Label(result_frame, textvariable=self.can_buy).pack()

        # Buttons frame
        buttons_frame = Frame(result_frame)
        buttons_frame.pack()

        Label(buttons_frame, text="Temps estimé à la grosse louche (secondes) :").pack()
        Label(buttons_frame, textvariable=self.time_estimation).pack()

        Button(buttons_frame, text="Acheter", command=self.buy).pack()

        Label(buttons_frame, textvariable=self.shop_state).pack()

    def estimate_time(self):
        time = self.quantity.get()
        self.time_estimation.set(str(time))

    def buy(self):
        def callback():
            result = self.controller.shop_buy(
            )
            self.shop_state.set("")
            messagebox.showinfo("Fini !", "Achats effectués.")

        self.shop_state.set(constants.waiting_message)
        self.after(10, callback)