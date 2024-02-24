import streamlit as st
import pandas as pd
import os
import base64
import pyarrow.lib as _lib
import pyarrow.lib as _lib

    
######################## ################################################################################################################################################################################

st.set_page_config(layout="wide", page_title = "Home Ess Bourse", page_icon="https://cdn.pixabay.com/photo/2016/07/19/04/40/moon-1527501_1280.jpg", initial_sidebar_state="expanded")  #expanded, auto, collapsed


######################## ################################################################################################################################################################################

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
######################## ################################################################################################################################################################################


st.markdown("""
    <link rel="stylesheet" href="https://cdn.pixabay.com/photo/2017/06/13/19/42/snow-2399850_640.jpg"> 
    """, unsafe_allow_html=True)




st.markdown(
    """
    <style>

    body {
    
        background-image: url (one.jpg);
        backround-size: cover;
    }
   .stApp {
        /* Utilisez l'URL de votre image comme valeur de background-image */
      
        background-image: url('https://cdn.pixabay.com/photo/2016/07/19/04/40/moon-1527501_1280.jpg');
        background-size: cover; /* Ajuste la taille de l'image pour couvrir tout l'arrière-plan */
        background-repeat: no-repeat; /* Empêche la répétition de l'image */
        background-position: center; /* Centre l'image horizontalement et verticalement */
        color: #ffffff;
        font-family: Arial, sans-serif;
        padding: 1rem;
        display: flex;
        justify-content: center;
        align-items: center;
        background-attachment: scroll; # doesn't work;
        
    }
    .stButton button {
        background-color:#8D03FF;
        color:white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color:#8D03FF;
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




# Ajoutez le code HTML et CSS pour personnaliser votre navbar
#navbar_style = """
#    <style>
#    .navbar {
#        background-image: url('https://images.pexels.com/photos/1366919/pexels-photo-1366919.jpeg?auto=compress&cs=tinysrgb&w=600');
#        background-size: cover;
#        background-repeat: no-repeat;
#        background-position: center;
#        height: 100px;
#        display: flex;
#        justify-content: center;
#        align-items: center;
#        color: white;
#        font-size: 24px;
#    }
#    </style>
#"""

#background-color : Vous pouvez spécifier une couleur de fond pour votre navbar en utilisant une valeur hexadécimale (#RRGGBB) ou un nom de couleur prédéfini.
#color : Cette propriété permet de définir la couleur du texte dans votre navbar.
#font-size : Vous pouvez ajuster la taille de la police du texte en spécifiant une valeur en pixels (px), points (pt), em (em), ou en pourcentage (%).
#padding : Cette propriété contrôle l'espacement à l'intérieur de votre navbar. Vous pouvez spécifier des valeurs pour le padding supérieur (top), droit (right), inférieur (bottom), et gauche (left).
#border : Vous pouvez ajouter une bordure à votre navbar en spécifiant les propriétés de la bordure, telles que la couleur, l'épaisseur et le style.
#text-align : Cette propriété permet de spécifier l'alignement horizontal du texte dans votre navbar. Vous pouvez utiliser les valeurs left, center ou right.



######################## ################################################################################################################################################################################


def main():
    
    ##### 1-MISE EN PLACE DES ELEMENTS DE LA PAGE PRINCIPALE ####

   # <div style="padding: 13px; background-color: #5f9ea0; border: 5px solid #e5e5e5; border-radius: 10px;">
    
    html_titre = """ 
    <div style="padding: 13px; background-color: #D3F7F4; border: 5px solid #0d0c0c; border-radius: 10px;">
    <h1 style="color:#0d0c0c; text-align: center; background: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));">🤖OUTIL D\'AIDE A LA DECISION POUR DETERMINER LE PROFIL INVESTISSEUR ET OPTIMISER LE PORTE FEUILLE CLIENT🤖<small><br> Powered by EMERALD SECURITIES SERVICES </h3></h1></h1>
    </div> 
    </div> 
    """


    
    st.markdown(html_titre, unsafe_allow_html = True)
    st.markdown('<br><br><br><br><br><br><br><br><br><p style="text-align: center;font-size:15px;" > <bold><center><h1 style="color:#D3F7F4">Cette Plateforme permet de determiner le profil investisseur pour lui proposer des actifs plus productif <h1></bold><p>', unsafe_allow_html=True)

    # Affichez votre navbar personnalisée
    #st.markdown(navbar_style, unsafe_allow_html=True)
    #st.markdown('<div class="navbar">Mon Navbar</div>', unsafe_allow_html=True)
    
    st.markdown('<p style="text-align: center;font-size:15px;" > <bold><center><h1 style="color:#D3F7F4"> Cette Plateforme permet d\'optimiser le portefeuille d\'Emerald <h1></bold><p>', unsafe_allow_html=True)
    
    st.markdown('<p style="text-align: center;font-size:15px;" > <bold><center><h1 style="color:#D3F7F4"> <bold>Pour commencer cliquez sur l\'onglet PROFIL INVESTOR ESS BOURSE <h1></bold><p>', unsafe_allow_html=True)
    
    st.markdown(hide_st_style, unsafe_allow_html=True)


if __name__ =='__main__':
    
    main()

######################## ################################################################################################################################################################################


