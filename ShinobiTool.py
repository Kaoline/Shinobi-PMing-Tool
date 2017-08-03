import sys
import os
import requests
from multiprocessing import Queue # Resolves Import errors
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
    def __init__(self, master, controller):
        self.controller = controller

        self.root = master
        self.root.title("Un MP, deux MPs, trois MPs...")

        self.build_frame()
        self.load_receivers()
        self.load_message()

        self.root.mainloop()

    def build_frame(self):
        # Receivers frame
        receiversFrame = Frame(self.root)
        receiversFrame.grid(row=0, column=0, padx=20)

        receiversLabel = Label(receiversFrame, text="Destinataires")
        receiversLabel.pack()

        self.receiversText = Text(receiversFrame, width=20)
        self.receiversText.pack()

        # Message frame
        messageFrame = Frame(self.root)
        messageFrame.grid(row=0, column=1, padx=20, pady=10)

        titleLabel = Label(messageFrame, text="Sujet")
        titleLabel.pack()

        self.titleEntry = Entry(messageFrame, width=50)
        self.titleEntry.pack()

        messageLabel = Label(messageFrame, text="Message")
        messageLabel.pack()

        self.messageText = Text(messageFrame, width=50)
        self.messageText.pack()

        # Buttons
        buttonsFrame = Frame(self.root)
        buttonsFrame.grid(row=1, column=0, columnspan=2, pady=20)

        saveButton = Button(buttonsFrame, text="Sauvegarder", command=self.save_everything)
        saveButton.grid(row=0, column=0, padx=20)

        sendButton = Button(buttonsFrame, text="Envoyer", command=self.send_pm)
        sendButton.grid(row=0, column=1, padx=20)

    def load_receivers(self):
        namesList = self.controller.load_receivers()
        self.receiversText.insert(CURRENT, namesList)

    def load_message(self):
        (title, message) = self.controller.load_message()
        self.titleEntry.insert(INSERT, title)
        self.messageText.insert(CURRENT, message)

    def save_everything(self):
        namesList = self.receiversText.get(1.0, END).rstrip("\n")
        title = self.titleEntry.get()
        message = self.messageText.get(1.0, END).strip("\n")

        self.controller.save_receivers(namesList)
        self.controller.save_message(title, message)

        messagebox.showinfo("C'est dans la boîte !", message="Sauvegarde effectuée")
        
    def send_pm(self):
        namesList = self.receiversText.get(1.0, END).rstrip("\n")
        title = self.titleEntry.get()
        message = self.messageText.get(1.0, END).rstrip("\n")
        self.controller.send_pm(namesList, title, message)

class LoginFrame(Frame):
    def __init__(self, master, controller):
        self.controller = controller

        self.root = master
        self.root.title("Qui êtes-vous ?")

        self.build_frame()

        self.root.mainloop()

    def build_frame(self):
        mainFrame = Frame(self.root)
        mainFrame.grid(padx=20, pady=10)

        loginLabel = Label(mainFrame, text="Login :")
        loginLabel.grid(row=0, column=0, padx=10, stick="E")

        self.loginEntry = Entry(mainFrame)
        self.loginEntry.grid(row=0, column=1)

        passwordLabel = Label(mainFrame, text="Mot de passe :")
        passwordLabel.grid(row=1, column=0, padx=10, pady=10, stick="E")

        self.passwordEntry = Entry(mainFrame, show="*")
        self.passwordEntry.grid(row=1, column=1, pady=10)

        okButton = Button(mainFrame, text="Connection", command=self.connect)
        okButton.grid(row=2, columnspan=2)

        self.errorLabel = Label(mainFrame, fg="red")
        self.errorLabel.grid(row=3, columnspan=2)

    def connect(self):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()

        connected = self.controller.connect(login, password)
        if connected:
            self.root.quit()
        else:
            self.errorLabel.configure(text="Problème d'identifiants, veuillez réessayer.")

# -----------------------------------------
# Model
# -----------------------------------------
class ShinobiAccess:
    """Interface with Shinobi.fr, to connect, send messages and do some classment searches"""
    def __init__(self):
        self.session = requests.Session()
        self.connected = False
        self.encoding = None
        
    def get_encoding(self):
        r = requests.get('http://www.shinobi.fr/')
        soup = BeautifulSoup(r.text, "html.parser")
        self.encoding = re.search('charset=(.*)', soup.head.meta["content"]).group(1)

    def connect(self, login, password):
        loginParams = {'login': login, 'pass': password}
        r = self.session.post('http://www.shinobi.fr/index.php?page=connexion', loginParams)
        self.connected = r.text.find("<a href='index.php?page=jeu'> Jouer </a>") != -1
        if self.connected:
            self.login = login
        return self.connected

    def send_message(self, receiver, title, messageContent):
        """Needs connection"""
        try:
            if self.encoding == None:
                self.get_encoding()
            r = self.session.get('http://www.shinobi.fr/index.php?page=menu-messagerie-nouveau')
            payload = {'destinataire': receiver.encode(self.encoding, "xmlcharrefreplace"), 'sujet': title.encode(self.encoding, "xmlcharrefreplace"), 'message': messageContent.encode(self.encoding, "xmlcharrefreplace"), 'envoi': 1}
            self.session.post('http://www.shinobi.fr/index.php?page=menu-messagerie', payload)
        except Exception as error:
            print("Problème à l'envoi au destinataire " + receiver + ".\nErreur : " + str(error))

    def get_shinobis(self, minPage, maxPage, minLvl, maxLvl, village, minScore, maxScore):
        link="http://www.shinobi.fr/index.php?page=classement&type=classement_joueurs"
        if not village is None:
            link += '&village='+village.lower()
        link += "&p="

        time1 = time.time()
        partial_search = partial(self.search_classment_page, classmentLink=link, minLvl=minLvl, maxLvl=maxLvl, village=village, minScore=minScore, maxScore=maxScore)
        pool = ThreadPool()
        shinoobs = pool.map(partial_search, range(minPage, maxPage+1))
        pool.close()
        pool.join()
        shinoobs = [item for sublist in shinoobs for item in sublist]
        time2 = time.time()
        print("Temps de recherche (secondes) : " + str(time2 - time1))

        return shinoobs

    def search_classment_page(self, pageNumber, classmentLink, minLvl, maxLvl, village, minScore, maxScore):
        shinoobs = []
        page = self.session.get(classmentLink + str(pageNumber))
        soup = BeautifulSoup(page.text, "html.parser")
        table = soup.find(id="classement_general")
        for tr in table.find_all("tr")[1:]:
            name = tr.find(class_="nom").a.text
            # team = tr.find(class_="equipe").a.text
            lvl = int(tr.find(class_="equipe").next_sibling.text)
            # clazz = tr.find(class_="village").previous_sibling.img["alt"]
            sVillage = tr.find(class_="village").a.span.text
            evo = int(tr.find(class_="evolution").text[1:])
            if lvl >= minLvl and lvl <= maxLvl and (village is None or sVillage == village.lower()) and evo >= minScore and evo <= maxScore:
                shinoobs.append(name)
        # print("Page " + str(pageNumber) + " ok")
        return shinoobs

# -----------------------------------------
# Controller
# -----------------------------------------
class Controller:
    def __init__(self):
        self.shinobiAccess = ShinobiAccess()

    def show_pmer(self):
        root = Tk()
        self.messageFrame = ConfigMessageFrame(root, controller)

    def send_pm(self, namesList, title, message):
        message = message.replace("\n", os.linesep)
        if not self.shinobiAccess.connected:
            LoginFrame(Toplevel(), self)
        confirm = messagebox.askyesno("Vraiment ?", message="Envoyer le message avec le compte " + self.shinobiAccess.login + " ?")
        if confirm:
            receivers = namesList.split("\n")
            print("Envoi du message. Temps prévu : " + str(len(receivers) * 0.075) + " secondes.")

            time1 = time.time()
            pool = ThreadPool()
            pool.map(partial(self.shinobiAccess.send_message, title=title, messageContent=message), receivers)
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
            msgConfig = open("Message.txt", "x", encoding="utf-8")
            msgConfig.write("[Sujet]\n\n[Message]\n")
            msgConfig.close()
        msgConfig = [line.rstrip('\n') for line in open("Message.txt", "r", encoding="utf-8")]
        titleIndex = msgConfig.index("[Sujet]")
        messageIndex = msgConfig.index("[Message]")
        title = msgConfig[titleIndex+1:messageIndex][0]
        message = "\n".join(msgConfig[messageIndex+1:])
        return (title, message)

    def save_receivers(self, namesList):
        open("Destinataires.txt", "w", encoding="utf-8").write(namesList)

    def save_message(self, title, message):
        open("Message.txt", "w", encoding="utf-8").write("[Sujet]\n" + title + "\n[Message]\n" + message.replace("\r", ""))

    def search_classment(self, minPage=1, maxPage=600, minLvl=100, maxLvl=100, village="Chikara", minScore=0, maxScore=99999):
        shinobis = self.shinobiAccess.get_shinobis(minPage, maxPage, minLvl, maxLvl, village, minScore, maxScore)
        open("Shinobis.txt", "w", encoding="utf-8").write("\n".join(shinobis))

# -----------------------------------------
# Main
# -----------------------------------------
controller = Controller()
controller.show_pmer()

# controller.search_classment()

# Run this in cmd to obtain executable
# pyinstaller --clean --onefile ShinobiTool.py
