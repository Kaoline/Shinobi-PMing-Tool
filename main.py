# file --main.py--
import os
from multiprocessing import Queue  # Resolves Import errors
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from tkinter import *
from tkinter import messagebox
import time

import shinobiaccess as sa
import gui


# -----------------------------------------
# Controller
# -----------------------------------------
class Controller:
    def __init__(self):
        self.shinobiAccess = sa.ShinobiAccess()

    def show_pmer(self):
        root = Tk()
        self.message_frame = gui.ConfigMessageFrame(root, controller)
    # Searching
    def search_ranking(self, file="Shinobis.txt", ranking="general", min_page=0, max_page=10, min_lvl=100, max_lvl=100,
                       village="Chikara", min_evo=0, max_evo=99999, min_points=0):
        shinobis = self.shinobiAccess.get_shinobis(ranking, min_page, max_page, min_lvl, max_lvl, village, min_evo,
                                                   max_evo, min_points)
        open(file, "w", encoding="utf-8").write("\n".join(shinobis))
        return shinobis

    # PMing

    def send_pm(self, names_list, title, message):
        message = message.replace("\n", os.linesep)
        if not self.shinobiAccess.connected:
            gui.LoginFrame(Toplevel(), self)
        confirm = messagebox.askyesno("Vraiment ?",
                                      message="Envoyer le message avec le compte " + self.shinobiAccess.login + " ?")
        if confirm:
            print("Envoi du message. Estimation : " + str(len(names_list) * 0.075) + " secondes.")

            time1 = time.time()
            pool = ThreadPool()
            pool.map(partial(self.shinobiAccess.send_message, title=title, message_content=message), names_list)
            pool.close()
            time2 = time.time()
            print("Temps d'envoi : " + str(time2 - time1))

    # Login
    def connect(self, login, password):
        return self.shinobiAccess.connect(login, password)


# -----------------------------------------
# Main
# -----------------------------------------
print("Starting at " + time.strftime("%H:%M:%S"))
controller = Controller()
controller.show_pmer()

# shinobis = controller.search_ranking()
# print(len(shinobis))
# print("Finished at " + time.strftime("%H:%M:%S"))

# Run this in cmd to obtain executable
# pyinstaller --clean main.py
