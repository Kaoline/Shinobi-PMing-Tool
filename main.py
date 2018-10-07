# file --main.py--
# version 2.1
# python 3.6

import os
from multiprocessing import Queue  # Resolves Import errors
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from tkinter import *
from tkinter import messagebox
import time

import shinobiaccess as sa
from config import *
import frameopening
import framelogin
import framesearching
import frameconfig
import frameshop
import constants


# -----------------------------------------
# Controller
# -----------------------------------------
class Controller:
    def __init__(self):
        self.shinobiAccess = sa.ShinobiAccess()
        Config.load()

    # First frame
    def show_choice(self):
        root = Tk()
        frameopening.FrameOpening(root, controller)

    # Searching
    def show_search(self):
        framesearching.FrameSearching(Toplevel(), controller)

    def search_ranking(self, file=constants.default_search_file, ranking="general", min_page=0, max_page=10, min_lvl=100, max_lvl=100,
                       village="Chikara", classe=None, min_evo=0, max_evo=99999, min_points=0):
        shinobis = self.shinobiAccess.get_shinobis(ranking, min_page, max_page, min_lvl, max_lvl, village, classe, min_evo,
                                                   max_evo, min_points)
        open(file, "w", encoding="utf-8").write("\n".join(shinobis))
        return shinobis

    # PMing
    def show_pmer(self):
        frameconfig.FrameConfigMessage(Toplevel(), controller)

    def send_pm(self, names_list, title, message, waiting_window):
        message = message.replace("\n", os.linesep)
        waiting_window.wait_window(framelogin.FrameLogin(Toplevel(), self))
        try:
            confirm = messagebox.askyesno("Vraiment ?",
                                      message="Envoyer le message avec le compte " + self.shinobiAccess.login + " ?")
        except:
            confirm = False
        if confirm:
            est_time = len(names_list) * 0.075
            print("Envoi du message. Estimation : " + "{0:.2f}".format(est_time) + " secondes (soit "+ "{0:.2f}".format(est_time / 60)+" minutes).")
            print("Starting at " + time.strftime("%H:%M:%S"))

            time1 = time.time()
            pool = ThreadPool()
            pool.map(partial(self.shinobiAccess.send_message, title=title, message_content=message), names_list)
            pool.close()
            time2 = time.time()
            print("Temps d'envoi : " + "{0:.2f}".format(time2 - time1) + "s soit " + "{0:.2f}".format((time2 - time1) / 60) + "min")
            print("Finished at " + time.strftime("%H:%M:%S"))
            return True
        else:
            return False

    # Deleting PMs
    def delete_pms(self, login, password, nbToDelete):
        self.connect(login, password)
        self.shinobiAccess.wipe_pms(nbToDelete)

    # Buy in shop
    def show_shop(self, waiting_window):
        waiting_window.wait_window(framelogin.FrameLogin(Toplevel(), self))
        if self.shinobiAccess.login is None:
            #TODO
            print("Pas connecté")
        elif not self.shinobiAccess.is_in_shop():
            #TODO
            print("Mauvais endroit")
        else:
            frameshop.FrameShop(Toplevel(), controller)

    # Login
    def connect(self, login, password):
        return self.shinobiAccess.connect(login, password)

    def deconnect(self):
        self.shinobiAccess.deconnect()


# -----------------------------------------
# Main
# -----------------------------------------
controller = Controller()
controller.show_choice()
# controller.show_search()
# controller.show_pmer()
# controller.delete_pms("", "", )

# Run this in cmd to obtain executable
# pyinstaller --clean --onefile --name ShinobiTool main.py
