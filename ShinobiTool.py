import os
import requests
from multiprocessing import Queue  # Resolves Import errors
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import time


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
        names_list = self.controller.load_receivers()
        self.receivers_Text.insert(CURRENT, names_list)

    def load_message(self):
        (title, message) = self.controller.load_message()
        self.title_entry.insert(INSERT, title)
        self.message_text.insert(CURRENT, message)

    def save_everything(self):
        names_list = self.receivers_Text.get(1.0, END).rstrip("\n")
        title = self.title_entry.get()
        message = self.message_text.get(1.0, END).strip("\n")

        self.controller.save_receivers(names_list)
        self.controller.save_message(title, message)

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


# -----------------------------------------
# Model
# -----------------------------------------
class ShinobiAccess:
    """Interface with Shinobi.fr, to connect, send messages and do some ranking searches"""

    def __init__(self):
        self.session = requests.Session()
        self.connected = False
        self.encoding = None

    def get_encoding(self):
        r = requests.get('http://www.shinobi.fr/')
        soup = BeautifulSoup(r.text, "html.parser")
        self.encoding = re.search('charset=(.*)', soup.head.meta["content"]).group(1)

    def connect(self, login, password):
        login_params = {'login': login, 'pass': password}
        r = self.session.post('http://www.shinobi.fr/index.php?page=connexion', login_params)
        self.connected = r.text.find("<a href='index.php?page=jeu'> Jouer </a>") != -1
        if self.connected:
            self.login = login
        return self.connected

    def send_message(self, receiver, title, message_content):
        """Needs connection"""
        try:
            if self.encoding is None:
                self.get_encoding()
            self.session.get('http://www.shinobi.fr/index.php?page=menu-messagerie-nouveau')
            payload = {'destinataire': receiver.encode(self.encoding, "xmlcharrefreplace"),
                       'sujet': title.encode(self.encoding, "xmlcharrefreplace"),
                       'message': message_content.encode(self.encoding, "xmlcharrefreplace"), 'envoi': 1}
            self.session.post('http://www.shinobi.fr/index.php?page=menu-messagerie', payload)
        except Exception as error:
            print("Problème à l'envoi au destinataire " + receiver + ".\nErreur : " + str(error))

    def get_shinobis(self, min_page, max_page, min_lvl, max_lvl, village, min_score, max_score, min_points):
        link = "http://www.shinobi.fr/index.php?page=classement&type=classement_joueurs"
        if village is not None:
            link += '&village=' + village.lower()
        link += "&p="

        time1 = time.time()
        partial_search = partial(self.search_ranking_page, ranking_link=link, min_lvl=min_lvl, max_lvl=max_lvl,
                                 village=village, min_score=min_score, max_score=max_score, min_points=min_points)
        pool = ThreadPool()
        shinoobs = pool.map(partial_search, range(min_page, max_page + 1))
        pool.close()
        pool.join()
        shinoobs = [item for sublist in shinoobs for item in sublist]
        time2 = time.time()
        print("Temps de recherche (secondes) : " + str(time2 - time1))

        return shinoobs

    def search_ranking_page(self, page_number, ranking_link, min_lvl, max_lvl, village, min_score, max_score, min_points):
        shinoobs = []
        page = self.session.get(ranking_link + str(page_number))
        soup = BeautifulSoup(page.text, "html.parser")
        table = soup.find(id="classement_general")
        try:
            for tr in table.find_all("tr")[1:]:
                name = tr.find(class_="nom").a.text
                # team = tr.find(class_="equipe").a.text
                lvl = int(tr.find(class_="equipe").next_sibling.text)
                # clazz = tr.find(class_="village").previous_sibling.img["alt"]
                sVillage = tr.find(class_="village").a.span.text
                evo = int(tr.find(class_="evolution").text[1:])
                points = float(tr.find(class_="points").text.replace(",", "."))
                if min_lvl <= lvl <= max_lvl and (village is None or sVillage == village.lower()) and min_score <= evo <= max_score and points >= min_points:
                    shinoobs.append(name)
            #print("Page " + str(page_number) + " ok")
        except Exception as ec:
            print(name.encode("UTF-8"))
            print(ec)
        return shinoobs


# -----------------------------------------
# Controller
# -----------------------------------------
class Controller:
    def __init__(self):
        self.shinobiAccess = ShinobiAccess()

    def show_pmer(self):
        root = Tk()
        self.message_frame = ConfigMessageFrame(root, controller)

    def send_pm(self, names_list, title, message):
        message = message.replace("\n", os.linesep)
        if not self.shinobiAccess.connected:
            LoginFrame(Toplevel(), self)
        confirm = messagebox.askyesno("Vraiment ?",
                                      message="Envoyer le message avec le compte " + self.shinobiAccess.login + " ?")
        if confirm:
            receivers = names_list.split("\n")
            print("Envoi du message. Estimation : " + str(len(receivers) * 0.075) + " secondes.")

            time1 = time.time()
            pool = ThreadPool()
            pool.map(partial(self.shinobiAccess.send_message, title=title, message_content=message), receivers)
            pool.close()
            time2 = time.time()
            print("Temps d'envoi : " + str(time2 - time1))

            messagebox.showinfo("Fini !", "Message envoyé aux " + str(len(receivers)) + " shinobis.")

    def connect(self, login, password):
        return self.shinobiAccess.connect(login, password)

    def load_receivers(self):
        if not os.path.isfile("Destinataires.txt"):
            open("Destinataires.txt", "x", encoding="utf-8").close()
        return open("Destinataires.txt", "r", encoding="utf-8").read()

    def load_message(self):
        if not os.path.isfile("Message.txt"):
            msg_config = open("Message.txt", "x", encoding="utf-8")
            msg_config.write("[Sujet]\n\n[Message]\n")
            msg_config.close()
        msg_config = [line.rstrip('\n') for line in open("Message.txt", "r", encoding="utf-8")]
        title_index = msg_config.index("[Sujet]")
        message_index = msg_config.index("[Message]")
        title = msg_config[title_index + 1:message_index][0]
        message = "\n".join(msg_config[message_index + 1:])
        return title, message

    def save_receivers(self, names_list):
        open("Destinataires.txt", "w", encoding="utf-8").write(names_list)

    def save_message(self, title, message):
        open("Message.txt", "w", encoding="utf-8").write(
            "[Sujet]\n" + title + "\n[Message]\n" + message.replace("\r", ""))

    def search_ranking(self, min_page=0, max_page=1000, min_lvl=100, max_lvl=100, village="Chikara", min_score=0, max_score=99999, min_points=0):
        shinobis = self.shinobiAccess.get_shinobis(min_page, max_page, min_lvl, max_lvl, village, min_score, max_score, min_points)
        open("Shinobis.txt", "w", encoding="utf-8").write("\n".join(shinobis))
        return shinobis


# -----------------------------------------
# Main
# -----------------------------------------
controller = Controller()
controller.show_pmer()

# shinobis = controller.search_ranking()
# print(shinobis)

# Run this in cmd to obtain executable
# pyinstaller --clean --onefile ShinobiTool.py
