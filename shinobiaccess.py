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
        self.encoding = None

    def get_encoding(self):
        r = requests.get('http://www.shinobi.fr/')
        soup = BeautifulSoup(r.text, "html.parser")
        self.encoding = re.search('charset=(.*)', soup.head.meta["content"]).group(1)

    def connect(self, login, password):
        self.session.get('http://www.shinobi.fr/index.php?page=deconnexion')
        login_params = {'login': login, 'pass': password}
        r = self.session.post('http://www.shinobi.fr/index.php?page=connexion', login_params)
        connected = r.text.find("<a href='index.php?page=jeu'> Jouer </a>") != -1
        if connected:
            self.login = login
        return connected

    def deconnect(self):
        self.session.get('http://www.shinobi.fr/index.php?page=deconnexion')
        self.login = None

    # PMer
    def send_message(self, receiver, title, message_content):
        """Needs connection"""
        # print("Starting at " + time.strftime("%H:%M:%S"))
        try:
            title = title.replace("%pseudo%", receiver)
            message_content = message_content.replace("%pseudo%", receiver)

            if self.encoding is None:
                self.get_encoding()
            self.session.get('http://www.shinobi.fr/index.php?page=menu-messagerie-nouveau')
            payload = {'destinataire': receiver.encode(self.encoding, "xmlcharrefreplace"),
                       'sujet': title.encode(self.encoding, "xmlcharrefreplace"),
                       'message': message_content.encode(self.encoding, "xmlcharrefreplace"), 'envoi': 1}
            self.session.post('http://www.shinobi.fr/index.php?page=menu-messagerie', payload)
        except Exception as error:
            print("Problème à l'envoi au destinataire " + receiver + ".\nErreur : " + str(error))
        # print("Finished at " + time.strftime("%H:%M:%S"))
        print(time.strftime("%H:%M:%S") + " > " + receiver + " ok")

    # Ranking search
    def get_shinobis(self, ranking, min_page, max_page, min_lvl, max_lvl, village, classe, min_evo, max_evo, min_points):
        print("Starting at " + time.strftime("%H:%M:%S"))
        link = "http://www.shinobi.fr/index.php?page=classement&type=classement_joueurs"
        if ranking == "weekly":
            link += "_hebdomadaire"
        if village is not None:
            link += '&village=' + village.lower()
        link += "&p="

        time1 = time.time()
        partial_search = partial(self.search_ranking_page, ranking_link=link, min_lvl=min_lvl, max_lvl=max_lvl,
                                 village=village, classe=classe, min_evo=min_evo, max_evo=max_evo, min_points=min_points)
        pool = ThreadPool()
        shinoobs = pool.map(partial_search, range(min_page, max_page + 1))
        pool.close()
        pool.join()
        shinoobs = [item for sublist in shinoobs for item in sublist]
        time2 = time.time()
        print("Temps de recherche (secondes) : " + str(time2 - time1))
        print("Finished at " + time.strftime("%H:%M:%S"))

        return shinoobs

    def search_ranking_page(self, page_number, ranking_link, min_lvl, max_lvl, village, classe, min_evo, max_evo, min_points):
        shinoobs = []
        page = self.session.get(ranking_link + str(page_number))
        soup = BeautifulSoup(page.text, "html.parser")
        table = soup.find(id="classement_general")
        for tr in table.find_all("tr")[1:]:
            try:
                name = tr.find(class_="nom").a.text
                # team = tr.find(class_="equipe").a.text
                lvl = int(tr.find(class_="equipe").next_sibling.text)
                clazz_img = tr.find(class_="village").previous_sibling.img
                clazz = None if clazz_img is None else clazz_img["alt"]
                sVillage = tr.find(class_="village").a.span.text
                evo = int(tr.find(class_="evolution").text[1:].replace(",", ""))
                points = float(tr.find(class_="points").text.replace(",", ""))
                if min_lvl <= lvl <= max_lvl and (village is None or sVillage == village.lower()) and (classe is None or clazz == classe) and min_evo <= evo <= max_evo and points >= min_points:
                    shinoobs.append(name)
            except Exception as ec:
                # print("Problem at page " + str(page_number))
                print(ec)
        print("Page " + str(page_number) + " ok")
        return shinoobs

    # Delete PMs
    def wipe_pms(self, nbToDelete):
        nbPages = nbToDelete // 20
        nbMessagesLastPage = nbToDelete % 20

        for page in range(nbPages):
            self.delete_message(20)
            print("Page " + str(page+1) + "/" + str(nbPages) + " deleted")
        self.delete_message(nbMessagesLastPage)
        print(str(nbMessagesLastPage) + " messages from last page deleted. " + str(nbToDelete) + " total pages deleted.")

    def delete_message(self, nbToDelete):
        page = self.session.get("http://www.shinobi.fr/index.php?page=menu-messagerie")
        soup = BeautifulSoup(page.text, "html.parser")
        table = soup.find(id="messagerie")
        for tr in table.find_all("tr")[1:nb_to_delete + 1]:
            suppr = tr.find_all(class_="icon")[1].a["href"]
            # print(suppr)
            self.session.get("http://www.shinobi.fr/" + suppr)

    # Shop
    def is_in_shop(self):
        page = self.session.get("http://www.shinobi.fr/index.php?page=moteur_boutique&categorie=normaux")
        soup = BeautifulSoup(page.text, "html.parser")
        state = soup.find(id="etatmsg").text
        return not ("Vous n'êtes pas au bon endroit pour effectuer cette action." in state or "Vous n'êtes pas aux Commerces !" in state)
