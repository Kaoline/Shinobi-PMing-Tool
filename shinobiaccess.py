# file --shinobiaccess.py--
import requests
from multiprocessing import Queue  # Resolves Import errors
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from tkinter import *
from bs4 import BeautifulSoup
import time


# -----------------------------------------
# Model
# -----------------------------------------
class ShinobiAccess:
    """Interface with Shinobi.fr, to connect, send messages and do some ranking searches"""

    # Connection block
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

    # PMer
    def send_message(self, receiver, title, message_content):
        """Needs connection"""
        print("Starting at " + time.strftime("%H:%M:%S"))
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
        print("Finished at " + time.strftime("%H:%M:%S"))

    def get_shinobis(self, min_page, max_page, min_lvl, max_lvl, village, min_score, max_score, min_points):
    # Ranking search
        print("Starting at " + time.strftime("%H:%M:%S"))
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
        print("Finished at " + time.strftime("%H:%M:%S"))

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
                    # print("Page " + str(page_number) + " ok")
        except Exception as ec:
            print(name.encode("UTF-8"))
            print(ec)
        return shinoobs
