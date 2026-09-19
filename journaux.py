# ============================================================
# IMPORTATION DES BIBLIOTHÈQUES
# ============================================================

# sys permet d'interagir avec Python.
# Ici, on l'utilise pour que les accents soient correctement
# affichés dans le terminal.
import sys

sys.stdout.reconfigure(encoding="utf-8")


# requests permet de communiquer avec Internet.
#
# requests.get()  -> récupérer une page
# requests.post() -> envoyer des données
import requests


# BeautifulSoup permet de lire du HTML et du XML
# et de rechercher des éléments à l'intérieur.
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURATION
# ============================================================

# Adresse du flux RSS du Parisien.
url = "https://feeds.leparisien.fr/leparisien/rss"


# Adresse de ton webhook Discord.
#
# ⚠️ Mets ton NOUVEAU webhook ici.
WEBHOOK_URL = "mon_webhook_discord"


# ============================================================
# RÉCUPÉRATION DU RSS
# ============================================================

# requests.get() va récupérer le contenu du flux RSS.
reponse = requests.get(url)


# On donne le contenu récupéré à BeautifulSoup.
#
# "xml" car le flux RSS est en XML.
soup = BeautifulSoup(reponse.content, "xml")


# ============================================================
# CRÉATION DU FICHIER
# ============================================================

# On ouvre/crée le fichier Journal_Quotidien.txt.
#
# "w" = write = écriture
# encoding="utf-8" = permet d'utiliser les accents.
#
# Le chemin complet est important pour que cron sache
# exactement où créer le fichier.
with open(
    r"C:\Users\Léo\Documents\informatique\python\Journal_Quotidien.txt",
    "w",
    encoding="utf-8"
    ) as f:


    # ========================================================
    # DATE DE MISE À JOUR DU RSS
    # ========================================================

    # .find() cherche UNE balise.
    #
    # Ici :
    # <lastBuildDate>...</lastBuildDate>
    heure = soup.find("lastBuildDate").get_text()


    # On crée le texte qui sera écrit dans le fichier.
    msg = "Dernière mise à jour : " + heure + "\n\n"


    # On écrit le texte dans le fichier.
    f.write(msg)


    # On affiche également le texte dans le terminal.
    print(msg)


    # ========================================================
    # RÉCUPÉRATION DES ARTICLES
    # ========================================================

    # .find_all() cherche TOUTES les balises correspondant
    # à ce qu'on demande.
    #
    # Chaque article du RSS est dans une balise <item>.
    articles = soup.find_all("item")


    # ========================================================
    # MESSAGE D'INTRODUCTION DISCORD
    # ========================================================

    # Ce message est AVANT la boucle for.
    #
    # Il sera donc envoyé UNE SEULE FOIS par lancement
    # du programme.
    message_intro = (
        "Bonjour tout le monde ! "
        "Voici les actus du jour :\n\n"
    )


    # requests.post() permet d'envoyer quelque chose
    # à une adresse Internet.
    #
    # Ici, on envoie le message à Discord.
    requests.post(
        WEBHOOK_URL,

        # Discord attend un JSON.
        #
        # "content" = contenu du message Discord.
        json={"content": message_intro}
    )


    # ========================================================
    # BOUCLE DES ARTICLES
    # ========================================================

    # "for" permet de répéter le code pour chaque article.
    #
    # Exemple :
    #
    # article 1 → exécute le code
    # article 2 → exécute le code
    # article 3 → exécute le code
    #
    # etc.
    for article in articles:


        # ====================================================
        # TITRE ET LIEN DU RSS
        # ====================================================

        # On cherche la balise <title>.
        #
        # .get_text() récupère uniquement le texte
        # contenu dans la balise.
        titre = article.find("title").get_text()


        # On cherche la balise <link>.
        lien = article.find("link").get_text()


        # ====================================================
        # OUVERTURE DE LA PAGE DE L'ARTICLE
        # ====================================================

        # On utilise le lien récupéré dans le RSS
        # pour aller sur la vraie page de l'article.
        page = requests.get(lien)


        # On transforme la page HTML en objet BeautifulSoup.
        #
        # "html.parser" signifie que la page est du HTML.
        page_soup = BeautifulSoup(
            page.content,
            "html.parser"
        )


        # ====================================================
        # RECHERCHE DES INFORMATIONS
        # ====================================================

        # Recherche du titre principal.
        titre_article = page_soup.find(
            "h1",
            class_="title_xl"
        )


        # Recherche du résumé.
        resume = page_soup.find(
            "p",
            class_="subheadline"
        )


        # Recherche de l'auteur.
        auteur = page_soup.find(
            "a",
            class_="author_link"
        )


        # Recherche de la date.
        date = page_soup.find(
            "div",
            class_="timestamp"
        )


        # ====================================================
        # VÉRIFICATION DU RÉSUMÉ
        # ====================================================

        # Si aucun résumé n'a été trouvé,
        # on passe directement à l'article suivant.
        #
        # "continue" = passer à l'itération suivante
        # de la boucle.
        if not resume:
            continue


        # ====================================================
        # RÉCUPÉRATION DU TEXTE DU RÉSUMÉ
        # ====================================================

        # get_text() récupère uniquement le texte.
        #
        # strip=True enlève les espaces inutiles
        # au début et à la fin.
        resume = resume.get_text(strip=True)


        # ====================================================
        # RÉCUPÉRATION DU TITRE DE LA PAGE
        # ====================================================

        # Si on a trouvé le titre sur la page...
        if titre_article:

            # On utilise le titre de la vraie page.
            titre = titre_article.get_text(strip=True)


        # ====================================================
        # RÉCUPÉRATION DE L'AUTEUR
        # ====================================================

        # Si l'auteur existe...
        if auteur:

            # On récupère uniquement son texte.
            auteur = auteur.get_text(" ", strip=True)

        else:

            # Si aucun auteur n'a été trouvé.
            auteur = "Auteur inconnu"


        # ====================================================
        # RÉCUPÉRATION DE LA DATE
        # ====================================================

        # Si une date existe...
        if date:

            # Le " " entre les parenthèses est important.
            #
            # Il demande à BeautifulSoup de mettre un espace
            # entre les différents morceaux de texte.
            #
            # Exemple :
            #
            # "Le" + "10 août 2026" + "à 20h20"
            #
            # devient :
            #
            # "Le 10 août 2026 à 20h20"
            date = date.get_text(" ", strip=True)

        else:

            # Si aucune date n'est trouvée.
            date = "Date inconnue"


        # ====================================================
        # ÉCRITURE DANS LE FICHIER
        # ====================================================

        # Écrit le titre.
        f.write(titre + "\n\n")


        # Écrit le résumé.
        f.write(resume + "\n")


        # Écrit l'auteur.
        f.write("Auteur : " + auteur + "\n")


        # Écrit la date.
        f.write("Date : " + date + "\n")


        # Écrit le lien.
        f.write("Lien : " + lien + "\n\n")


        # ====================================================
        # CRÉATION DU MESSAGE DISCORD
        # ====================================================

        # Le "f" devant les guillemets permet d'insérer
        # des variables directement dans une chaîne.
        #
        # Exemple :
        #
        # nom = "Leo"
        # f"Bonjour {nom}"
        #
        # donne :
        #
        # Bonjour Leo
        #
        # Sur Discord :
        # **texte** = texte en gras
        message = (
            f"**{titre}**\n\n"
            f"{resume}\n\n"
            f"**Auteur :** {auteur}\n"
            f"**Date :** {date}\n"
            f"{lien}"
        )


        # ====================================================
        # ENVOI DE L'ARTICLE SUR DISCORD
        # ====================================================

        # On envoie le message au webhook Discord.
        requests.post(
            WEBHOOK_URL,

            # Discord attend les données sous forme de JSON.
            json={"content": message}
        )


# ============================================================
# FIN DU PROGRAMME
# ============================================================

# Le programme arrive ici une fois que tous les articles
# ont été parcourus.
#
# Comme on utilise "with open()", le fichier est
# automatiquement fermé à la fin du bloc.