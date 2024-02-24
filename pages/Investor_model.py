'''
J'ai divisé le script en plusieurs fonctions qui servent chacune un but spécifique :

- afficher_titre() : Affiche le titre de la plateforme.

- recueillir_informations_utilisateur() : Récupère les réponses de l'utilisateur à travers les champs de saisie et les select box.

- calculer_profil_investisseur(reponses) : Effectue les calculs pour déterminer le profil de l'investisseur en fonction des réponses et ajoute le profil au dictionnaire reponses.
- afficher_resultats(reponses) : Affiche les réponses de l'utilisateur dans un tableau et permet de télécharger les réponses au format Excel.

J'ai également ajouté une condition if __name__ == "__main__": pour exécuter la fonction main() seulement lorsque le script est exécuté directement et non lorsqu'il est importé en tant que module.

'''

################################ PARTIE DU CODE POUR L'IMPORTATION DES BIBLIOTHEQUES  ########################
#https://media.istockphoto.com/id/1455965102/photo/beautiful-sunrise-bursting-through-the-eucalyptus-trees-as-it-rises-over-a-mountain-beside-a.jpg?s=2048x2048&w=is&k=20&c=pqm6SLczvaDQVCO3BGGAzyx605GlZqkXO8l8frFFRq0=

import streamlit as st
import mysql.connector
import pandas as pd
import time as t
import base64
from jinja2 import Environment, FileSystemLoader
import mysql.connector
from mysql.connector import Error 
from PIL import Image
import os
import time
import base64




######################## ################################################################################################################################################################################

st.set_page_config(layout="wide", page_title = "Investor Model", page_icon='https://media.istockphoto.com/id/1455965102/photo/beautiful-sunrise-bursting-through-the-eucalyptus-trees-as-it-rises-over-a-mountain-beside-a.jpg?s=2048x2048&w=is&k=20&c=pqm6SLczvaDQVCO3BGGAzyx605GlZqkXO8l8frFFRq0=', initial_sidebar_state="expanded") 


############################### PARTIE DU CODE POUR LA BEAUTE DE L'AFFICHAGE ########################

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
############################## PARTIE DU CODE POUR PRENDRE LES DONNEES DE L'UTILISATEUR ########################



st.markdown("""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    """, unsafe_allow_html=True)



############################## PARTIE DU CODE POUR PRENDRE LES DONNEES DE L'UTILISATEUR ########################

st.markdown(
    """
    <style>
   .stApp {
        /* Utilisez l'URL de votre image comme valeur de background-image */
       
        background-image: url('https://media.istockphoto.com/id/1455965102/photo/beautiful-sunrise-bursting-through-the-eucalyptus-trees-as-it-rises-over-a-mountain-beside-a.jpg?s=2048x2048&w=is&k=20&c=pqm6SLczvaDQVCO3BGGAzyx605GlZqkXO8l8frFFRq0=');
        background-size: cover; /* Ajuste la taille de l'image pour couvrir tout l'arrière-plan */
        background-repeat: no-repeat; /* Empêche la répétition de l'image */
        background-position: center center; /* Centre l'image horizontalement et verticalement */
        color: #ffffff;
        font-family: Arial, sans-serif;
        padding: 1rem;
        
        background-attachment: scroll; # doesn't work;
        
    }
    .stButton button {
        background-color:#0080ff;
        color:white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out;
    }

    .stRadio radio {
        background-color:#8D03FF;
        color:white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out;
    }

    .stButton button:hover {
        background-color:#4733ae;
    }

    .stHeader {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    
    </style>
    """,
    unsafe_allow_html=True
)




############################## PARTIE DU CODE POUR PRENDRE LES DONNEES DE L'UTILISATEUR ########################


# Définition des colonnes du dataframe
columns = ["Nom_Utilisateur", "Phone_Utilisateur", "Votre_Age", "Vos_Charges", "Horizon_Investi", "Objectif_Investi_0", "Objectif_Investi_1", "Periode_Retrait", "Intention_Retrait", "Experience", "Evual_Risque_0", "Evual_Risque_1","Profil_Investisseur"]


df = pd.DataFrame(columns=columns)


################################ PARTIE DU CODE POUR LA BEAUTE DE L'AFFICHAGE DU TITRE DE LA PAGE  ########################
def afficher_titre():

    html_titre = """ 
    <div style="padding: 13px; background-color: #5f9ea0; border: 5px solid #e5e5e5; border-radius: 10px;">
    <h1 style="color: #f8f8f8; text-align: center;"><bold>🤖 PREDICATEUR DE PROFIL INVESTISSEUR 🤖<small><br> Powered by EMERALD SECURITIES SERVICES </bold> </small></h1></h1>
    
    <h3 style="color: white; text-align: center;">Cette Plateforme permet de determiner le profil investisseur pour lui proposer des actifs plus productif</bold></h3>
    </div></br></br>
    """
    st.markdown(html_titre, unsafe_allow_html = True) 
    



################################ PARTIE DU CODE POUR PRENDRE LES DONNEES DE L'UTILISATEUR ########################


def recueillir_informations_utilisateur():
    nom_utilisateur = st.text_input("Entrez votre nom complet:")

    phone_utilisateur = st.text_input("Entrez votre numéro de téléphone:")

    votre_age = st.selectbox("Dans quelle fourchette se situe votre âge",  ["Moins de 30 ans", "Entre 30 et 39 ans", "Entre 40 et 49 ans", "Entre 50 et 59 ans", "Entre 60 et 69 ans", "Entre 70 et 79 ans", "Plus de 79 ans"])
    
    vos_charges = st.selectbox("Dans quelle fourchette se situent vos charges familiales",  ["Moins d'un 1 Million", "Entre 1 Million et 2 Millions", "Entre 2 Millions et 4 Millions", "Plus de 5 Millions"])

    horizon_investi = st.selectbox("Quel est votre horizon d'investissement ?",  ["= ou inferieur a 6Mois", "Entre 1an et 3ans", "3 ans et Plus"])


    objectif_investi_0 = st.selectbox("Quelle est la raison d\'être de votre portefeuille?",  ["Générer des revenus immédiatement","Générer des revenus pour plus tard","Subvenir aux besoins futurs des personnes à ma charge","Financer un achat important ultérieurement"])

    objectif_investi_1 = st.selectbox("Quel est l\'objectif le plus important à l\'égard de votre portefeuille?",  ["M\'assurer que les placements de mon portefeuille sont sûrs","Voir fructifier les placements de mon portefeuille sans que leur rendement ne fluctue","vObtenir un équilibre entre la croissance des placements et la sécurité, et suivre le rythme de l\'inflation","Obtenir une plus-value potentielle de mon portefeuille en contrepartie d\'une certaine volatilité des placements","Satisfaire mon seul critère, soit la croissance potentielle des placements à long terme"
])

    
    periode_retrait = st.selectbox("Lorsque vous aurez besoin des fonds, sur quelle période prévoyez-vous les retirer? ?",  ["En un seul retrait forfaitaire", "Sur une période de moins de deux ans", "Sur une période de deux à cinq ans"])

    
    intention_retrait = st.selectbox("Avez-vous l\'intention de faire des retraits ou de verser des cotisations dans vos placements aujourd\'hui et durant les cinq prochaines années? ?",  ["a. Je prévois retirer de l\'argent à des intervalles réguliers, mais je ne prévois pas verser de cotisations", "Je vais certainement verser des cotisations régulières,mais je ne ferai pas de retrait", "Je vais sans doute verser des cotisations supplémentaires, mais je ne ferai pas de retrait.", "Je ferai probablement un retrait forfaitaire, mais je ne prévois pas verser de cotisations", "Je vais probablement verser des cotisations et effectuer des retraits"])
    
    
    experience = st.selectbox("Avez vous deja eu a prendre un produit financier?",  ["Debutant", "Intermediaire", "Expert"])

    
    evual_risque0 = st.selectbox("Supposons que vous investissiez 100 000 $ à long terme. Quelle est la baisse annuelle maximale de votre portefeuille que vous seriez prêt à assumer?",  ["Je ne serais pas prêt à subir des pertes","Je serais prêt à assumer une baisse de 5 000","Je pourrais tolérer une baisse de 10 000","Je serais prêt à subir une baisse maximale de 15 000","Je crois que ma limite se situerait à 20 000","Je pourrais me remettre d’une baisse de plus de 20 000"
])

    
    evual_risque1 = st.selectbox("En tenant compte du fait que les fluctuations du marché sont inévitables, dans l\'éventualité où vous subiriez une baisse considérable, pendant combien de temps êtes-vous prêt à conserver vos placements existants en vue de récupérer leur valeur?",  ["Moins de trois mois","De trois à six mois","De six mois à un an 10","De un à deux ans 15","De deux à trois ans 20","Plus de trois ans 25"])
    
    
    
    questions = {
        "Avez-vous connaissance des produits auxquels vous sollicitez ?": ["OUI", "NON"]
    }

    reponses = {
        "Nom_Utilisateur": nom_utilisateur,
        "Phone_Utilisateur": phone_utilisateur,
        "Votre_Age": votre_age,
        "Vos_Charges": vos_charges,
        "Horizon_Investi": horizon_investi,
        "Objectif_Investi_0": objectif_investi_0,
        
        "Objectif_Investi_1":objectif_investi_1,
        "Periode_Retrait":periode_retrait,
        
        "Intention_Retrait":intention_retrait,
        "Experience": experience,
        "Evual_Risque_0":evual_risque0,
        "Evual_Risque_1":evual_risque1,
        "Profil_Investisseur": ""
    }

    for question, choix in questions.items():
        reponses[question] = st.radio(question, choix, key=question)
    
    return reponses

def calculer_profil_investisseur(reponses):
    valeurs = {
        "Moins de 30 ans": 15,
        "Entre 30 et 39 ans": 15,
        "Entre 40 et 49 ans": 15,
        "Entre 50 et 59 ans": 10,
        "Entre 60 et 69 ans": 5,
        "Entre 70 et 79 ans": 3,

        "Plus de 79 ans": 2,
        "Moins d'un 1 Million": 4,
        "Entre 1 Million et 2 Millions": 6,
        "Entre 2 Millions et 4 Millions": 8,
        "Plus de 5 Millions": 10,
        
        "= ou inferieur a 6Mois": 0,
        "Entre 1an et 3ans": 0, 
        "3 ans et Plus":5,

        "Générer des revenus immédiatement": 0,
        "Générer des revenus pour plus tard": 10,
        "Subvenir aux besoins futurs des personnes à ma charge": 15,
        "Financer un achat important ultérieurement": 15,
        
        "M\'assurer que les placements de mon portefeuille sont sûrs": 2,
        "Voir fructifier les placements de mon portefeuille sans que leur rendement ne fluctue": 5,
        "Obtenir un équilibre entre la croissance des placements et la sécurité, et suivre le rythme de l\'inflation": 10,
        "Obtenir une plus-value potentielle de mon portefeuille en contrepartie d\'une certaine volatilité des placements": 15,
        "Satisfaire mon seul critère, soit la croissance potentielle des placements à long terme": 20,

              
        "En un seul retrait forfaitaire": 3, 
        "Sur une période de moins de deux ans": 3, 
        "Sur une période de deux à cinq ans": 5,
        
        "Je prévois retirer de l\'argent à des intervalles réguliers, mais je ne prévois pas verser de cotisations": 5, 
        "Je vais certainement verser des cotisations régulières,mais je ne ferai pas de retrait": 15,
        "Je vais sans doute verser des cotisations supplémentaires, mais je ne ferai pas de retrait.":10, 
        "Je ferai probablement un retrait forfaitaire, mais je ne prévois pas verser de cotisations":7,
        "Je vais probablement verser des cotisations et effectuer des retraits":8,

        "Debutant":5, 
        "Intermediaire":8,
        "Expert":10,

        "Je ne serais pas prêt à subir des pertes":2,
        "Je serais prêt à assumer une baisse de 5 000":5,
        "Je pourrais tolérer une baisse de 10 000":10,
        "Je serais prêt à subir une baisse maximale de 15 000":15,
        "Je crois que ma limite se situerait à 20 000":20,
        "Je pourrais me remettre d\'une baisse de 20000":25,

        "Moins de trois mois":5,
        "De trois à six mois":8,
        "De six mois à un an":10,
        "De un à deux ans":15,
        "De deux à trois ans":20,
        "Plus de trois ans":25
    }

    total = sum(valeurs.get(reponses.get(key), 0) for key in reponses.keys())

    if total <= 55:
        profil_investisseur = 'prudent'
    elif total > 56 and total <= 104:
        profil_investisseur = 'Stable'
    else:
        profil_investisseur = 'Agressif'

    reponses['Profil_Investisseur'] = profil_investisseur
    reponses['Valeur_Risque'] = total

    return profil_investisseur, total




def envoyer_donnees_bdd(reponses):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testoo"
    )

    cursor = cnx.cursor()

    requete = "INSERT INTO testaa (`{}`) VALUES ({})".format(
        "`, `".join(reponses.keys()),
        ", ".join(["%s"] * len(reponses))
    )

    cursor.execute(requete, list(reponses.values()))

    cnx.commit()

    progress_bar = st.progress(0)

    for i in range(101):
        t.sleep(0.01)
        progress_bar.progress(i)

    cursor.close()
    cnx.close()

    st.success("Les données ont été enregistrées avec succès dans la base de données!")






def convertir_en_excel(df, nom_fichier):
    with pd.ExcelWriter(nom_fichier, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)






def main():
    afficher_titre() 
    reponses = recueillir_informations_utilisateur()
    
    submit_button = st.button('Soumettez Vos Données')
    if submit_button:
        profil_investisseur, total = calculer_profil_investisseur(reponses)
        st.write("Profil investisseur :", profil_investisseur)
        st.write("La valeur de risque de Mr/Mme:", reponses["Nom_Utilisateur"], "est", total)


    show_button = st.button('Afficher Vos Informations')
    if show_button:
        reponses['Profil_investisseur'], total = calculer_profil_investisseur(reponses)
        global df
        df = pd.concat([df, pd.DataFrame([reponses])], ignore_index=True)
        st.dataframe(df)

    send_button = st.button('Envoyes Vos Données')
    if send_button:
        nom_fichier = reponses["Nom_Utilisateur"] + ".xlsx"
        profil_investisseur, total = calculer_profil_investisseur(reponses)
        reponses['Profil_Investisseur'] = profil_investisseur
        reponses['Valeur_Risque'] = total
        df.loc[len(df)] = reponses
        with st.spinner("Traitement en cours...."):
                
            envoyer_donnees_bdd(reponses)
            convertir_en_excel(df, nom_fichier)
            t.sleep(3)
        st.success("Les données ont été enregistrées avec succès!")
        st.write("Veuillez trouver le fichier", nom_fichier, "Dans le repertoire local")
        #st.balloons()
        st.snow()
        
  

if __name__ == "__main__":
    main()

