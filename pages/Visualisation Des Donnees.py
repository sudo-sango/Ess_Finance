######################## ################################################################################################################################################################################
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import pyarrow.lib as _lib
import pyarrow.lib as _lib
import plotly.graph_objects as go
import io
import base64
import streamlit as st
import os
import pandas as pd
import streamlit as st
#from fpdf import FPDF
#from PyPDF2 import PdfMerger

######################## ################################################################################################################################################################################

st.set_page_config(layout="wide", page_title = "Visualisation", page_icon="https://images.pexels.com/photos/36487/above-adventure-aerial-air.jpg?auto=compress&cs=tinysrgb&w=600", initial_sidebar_state="expanded")  #expanded, auto, collapsed

#st.set_page_config(layout="centered", wide)

######################## ################################################################################################################################################################################


hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

st.markdown("""
    <link rel="stylesheet" href=https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    """, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    
    body {
        background-color: #ffffff; /* Couleur de fond par défaut */
        color: #000000; /* Couleur de texte par défaut */
        font-family: Arial, sans-serif;
        padding: 1rem;
    }

    .video-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 500px; /* Ajustez la hauteur de la vidéo selon vos besoins */
    }
    
    
   .stApp {
        /* Utilisez l'URL de votre image comme valeur de background-image */
      
        background-image: url('https://images.pexels.com/photos/36487/above-adventure-aerial-air.jpg?auto=compress&cs=tinysrgb&w=600');
        background-size: cover; /* Ajuste la taille de l'image pour couvrir tout l'arrière-plan */
        background-repeat: no-repeat; /* Empêche la répétition de l'image */
        background-position: center center; /* Centre l'image horizontalement et verticalement */
        color: #ffffff;
        font-family: Arial, sans-serif;
        padding: 1rem;
        
        background-attachment: scroll; # doesn't work;
        
    }
    .stButton button {
        background-color:#5f9ea0;
        color:white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color:#D3F7F4;
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


######################## ################################################################################################################################################################################

# Fonction pour charger les données avec st.cache_data
@st.cache_data
def load_data(dataset_name):
    data = pd.read_csv(dataset_name)
    data['Date'] = pd.to_datetime(data['Date']) #convertir la colonne date en datetime
    data.set_index('Date', inplace=True) #Definir la colonne de date index
    return data

######################## ################################################################################################################################################################################

# Fonction pour afficher les cours de clôture
def display_closing_prices(data):
    st.subheader(' Affichage Des Données')
    st.write(data)
    #return data

 #####################################################################################################################################################################################################################################################


def create_download_link(data):
    # Convertir les données en fichier Excel
    data = display_closing_prices(data)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="donnees.xlsx">Téléchargez le fichier Excel</a>'


 #####################################################################################################################################################################################################################################################

def create_download_link_pdf(data):
    pdf = FPDF()
    #pdf = FPDF(orientation = 'L') pour le format paysage
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    # Ajout du titre
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, "Resumes des fichiers Données filtrees ", 0, 1, 'C') # Ajustement de la largeur pour le format paysage
    pdf.ln(10)
    
    # Ajout du contenu du DataFrame
    #for col in filtered_data.columns:
    for col in data.columns:
        pdf.cell(0, 10, str(col), 0, 1)
        for index, row in data.iterrows():
            pdf.cell(0, 10, str(row[col]), 0, 1)
        pdf.ln(5)
    # Nom a changer il doit etre le nom choisis en bas 
    output_filename = "donnees.pdf"
    pdf.output(output_filename)
    
    merger = PdfMerger()
    merger.append(output_filename)
    merger.write(output_filename)
    merger.close()

    with open(output_filename, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    b64 = base64.b64encode(pdf_content).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{output_filename}">Téléchargez le fichier PDF</a>'

    return href

 #####################################################################################################################################################################################################################################################

def get_color_two_figure():
    diagram_color_two = st.color_picker("Choisir la couleur pour la série de prix", "#62C5BD", key = "diagram_color_two")
    color_ema = st.color_picker("Choisir la couleur pour EMA", "#FFFFFF", key = "color_ema")
    color_sma = st.color_picker("Choisir la couleur pour SMA", "#0DC0E8", key = "color_sma")
    # Obtenir la couleur de fond choisie par l'utilisateur
    background_color_two= st.color_picker("Choisir la couleur de fond", "#000000", key= "background_color_two")
    return diagram_color_two, color_ema, color_sma,background_color_two


 #####################################################################################################################################################################################################################################################

def get_color_one_figure():
    # Obtenir la couleur de fond choisie par l'utilisateur
    background_color_one = st.color_picker("Choisir la couleur de fond", "#000000")
    # Obtenir la couleur des diagrammes choisie par l'utilisateur
    diagram_color_one = st.color_picker("Choisir la couleur des diagrammes", "#62C5BD")

    return background_color_one, diagram_color_one


 #####################################################################################################################################################################################################################################################

def display_price_evolution_ba1r(filtered_data, selected_column, start_date, end_date, background_color_one, diagram_color_one):
    fig = go.Figure()

    # Tracer la série de prix
    fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data[selected_column], name=selected_column, marker_color=diagram_color_one))

    # Mise en forme du graphique
    fig.update_layout(
       title=f'Évolution des prix de {selected_column} entre {start_date} et {end_date}',
       xaxis_title="Date",
       yaxis_title=f'{selected_column} price $',
       width=800,  # Largeur de la figure en pixels
       height=600,  # Hauteur de la figure en pixels
       plot_bgcolor=background_color_one  # Couleur de fond du graphique
    )

    # Utilisation de st.plotly_chart pour afficher le graphique dans Streamlit
    st.plotly_chart(fig)

 #####################################################################################################################################################################################################################################################


def display_price_evolution_with_ema_and_smaa(filtered_data, selected_column, start_date, end_date, ema_span, sma_span,diagram_color_two, color_ema, color_sma,background_color_two):
    #diagram_color_two, color_ema, color_sma = get_colors()

    fig = go.Figure()

    # Tracer la série de prix
    fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data[selected_column], name=selected_column, marker_color=diagram_color_two))
    
    # Calcul de la moyenne mobile exponentielle
    ema_values = filtered_data[selected_column].ewm(span=ema_span, adjust=False).mean()

    # Calcul de la moyenne mobile simple
    sma_values = filtered_data[selected_column].rolling(window=sma_span).mean()

    # Tracer les moyennes mobiles
    fig.add_trace(go.Scatter(x=filtered_data.index, y=ema_values, mode='lines', name=f'EMA ({ema_span})', line=dict(color=color_ema)))
    fig.add_trace(go.Scatter(x=filtered_data.index, y=sma_values, mode='lines', name=f'SMA ({sma_span})', line=dict(color=color_sma)))

    # Mise en forme du graphique
    fig.update_layout(
       title=f'Évolution des prix de {selected_column} avec MME ({ema_span}) et MMS ({sma_span}) entre {start_date} et {end_date}',
       xaxis_title="Date",
       yaxis_title=f'{selected_column} price $',
       width=800,  # Largeur de la figure en pixels
       height=600,  # Hauteur de la figure en pixels
       plot_bgcolor=background_color_two  # Couleur de fond du graphique
    )

    # Utilisation de st.plotly_chart pour afficher le graphique dans Streamlit
    st.plotly_chart(fig)

######################## #####################################################################################################################################################################################################################################################


    
# Fonction de traitement des données
def process_data(selected_data, selected_column, start_date, end_date):
    #filtered_data = selected_data[(selected_data['Date'] >= str(start_date)) & (selected_data['Date'] <= str(end_date))]
    end_date = pd.to_datetime(end_date)
    start_date = pd.to_datetime(start_date)
    #filtered_data = selected_data[(selected_data['Date'] >= str(start_date)) & (selected_data['Date'] <= str(end_date))]
    filtered_data = selected_data.loc[(selected_data.index >= start_date) & (selected_data.index <= end_date)]
    return filtered_data

def get_csv_files():
    csv_files = []
    for file in os.listdir():
        if file.endswith('.csv'):
            csv_files.append(file)
    return csv_files


def load_data(file_path):
    return pd.read_csv(file_path)


def process_data(data, selected_column, start_date, end_date):
    # Logique de traitement des données
    filtered_data = data  # Exemple: données non traitées
    return filtered_data



######################## #####################################################################################################################################################################################################################################################
def main():
    html_titre = """ 
    <div style="padding: 13px; background-color: #5f9ea0; border: 5px solid #e5e5e5; border-radius: 10px;">
    <h1 style="color:white; text-align: center;">🤖 Affichage Interactif Des Données 🤖<small><br> Powered by EMERALD SECURITIES SERVICES </small></h1></h1>
    </div> <br><br><br>"""
    
    st.markdown(html_titre, unsafe_allow_html=True)

    csv_files = get_csv_files()  # Obtient la liste des fichiers CSV disponibles

    selected_dataset = st.selectbox('Sélectionner le dataset à afficher', csv_files)

    selected_data = load_data(selected_dataset)

    selected_column = st.selectbox('Sélectionner une colonne', selected_data.columns)
    start_date = st.date_input('Date de début')
    end_date = st.date_input('Date de fin')

    filtered_data = process_data(selected_data, selected_column, start_date, end_date)

    display_closing_prices(filtered_data)



######################## #####################################################################################################################################################################################################################################################

    if st.button("Télécharger les données filtres sous forme Excel"):
        link = create_download_link(filtered_data)
        if link :
            st.markdown(link, unsafe_allow_html=True)
            st.success("Vous avez reussi le telechargement du fichier excel  🎉!!")
            st.snow()
        else:
            st.error("Oups !! Une erreur s'est produite 😞!! Veuillez essayez a nouveau!!!")

######################## #####################################################################################################################################################################################################################################################
            
    if st.button("Télécharger les données sous forme PDF"):
        pdf_link = create_download_link_pdf(filtered_data)
        
        if pdf_link:
            st.markdown(pdf_link, unsafe_allow_html=True)
            st.success("Vous avez reussi le telechargement")
            st.snow()
        else:
            st.error("Oups !! Une erreur s'est produite 😞!! Veuillez essayez a nouveau!!!")


######################## #####################################################################################################################################################################################################################################################

    if st.checkbox('Afficher l\'évolution des cours'):
         background_color_one, diagram_color_one = get_color_one_figure()
         display_price_evolution_ba1r(filtered_data, selected_column, start_date, end_date, background_color_one, diagram_color_one)


######################## #####################################################################################################################################################################################################################################################

    if st.checkbox('Afficher l\'évolution des cours avec les indicateurs'):

        ema_span = st.slider('Période de la moyenne mobile exponentielle (EMA)', min_value=5, max_value=50, value=20)
        sma_span = st.slider('Période de la moyenne mobile simple (SMA)', min_value=5, max_value=50, value=20)
        diagram_color_two, color_ema, color_sma, background_color_two= get_color_two_figure()
        display_price_evolution_with_ema_and_smaa(filtered_data, selected_column, start_date, end_date, ema_span, sma_span,diagram_color_two, color_ema, color_sma, background_color_two)
    
    
if __name__ == "__main__":
    main()


    








 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#####################  FONCTION POUR FAIRE L'AFFICHAGE DE 'EVOLUTION DES PRODUITS FINACIER  ##############################################################

#def display_price_evolution(filtered_data, selected_column, start_date, end_date):
#    fig, ax = plt.subplots(figsize=(7,7))
#    ax.plot(filtered_data.index, filtered_data[selected_column], label = selected_column)
#    ax.set_title('Evolution des prix de clôture')
#    ax.set_xlabel("Date", fontsize=10)
#    ax.set_ylabel('Close price $', fontsize=10)
#    ax.legend(loc='upper left')
#    st.pyplot(fig)


#####################  FONCTION POUR FAIRE L'AFFICHAGE DE 'EVOLUTION DES PRODUITS FINACIER  ##############################################################


#def display_price_evolution(filtered_data, selected_column, start_date, end_date):
#    plt.figure(figsize=(7, 7))
    
    # Utiliser seaborn.lineplot pour créer le graphique
#    sns.lineplot(data=filtered_data, x=filtered_data.index, y=selected_column, label=selected_column, color='b')
    
#    plt.title(f'Évolution des prix de {selected_column} entre {start_date} et {end_date}')
#    plt.xlabel("Date", fontsize=10)
#    plt.ylabel(f'{selected_column} price $', fontsize=10)
#    plt.legend(loc='upper left')
    
    # Utiliser st.pyplot pour afficher le graphique dans Streamlit
#   st.pyplot()



######################## ################################################################################################################################################################

#def display_price_evolution(filtered_data, selected_column, start_date, end_date):
#    fig = go.Figure()

    # Ajouter une trace de ligne pour la colonne spécifiée
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[selected_column], mode='lines', name=selected_column, line=dict(color='blue')))

    # Mise en forme du graphique
#    fig.update_layout(
#       title=f'Évolution des prix de {selected_column} entre {start_date} et {end_date}',
#       xaxis_title="Date",
#        yaxis_title=f'{selected_column} price $',
#        legend=dict(x=0, y=1, traceorder='normal'),
#    )

    # Utiliser st.plotly_chart pour afficher le graphique dans Streamlit
#    st.plotly_chart(fig)
    
    
######################## SCRIPT POUR AFFICHER  L'EVOLUTION DES COURS EN COURBE SANS LES BANDE DE BOLLINGER A SUPPRIMER ################################################################################################################################################################################


#def display_price_evolution(filtered_data, selected_column, start_date, end_date):
#    fig = go.Figure(data=[go.Candlestick(x=filtered_data.index,
#                    open=filtered_data[selected_column],  # Utilisation du prix sélectionné comme ouverture
#                    high=filtered_data[selected_column],  # Utilisation du prix sélectionné comme plus haut
#                    low=filtered_data[selected_column],   # Utilisation du prix sélectionné comme plus bas
#                    close=filtered_data[selected_column])])  # Utilisation du prix sélectionné comme fermeture

    # Mise en forme du graphique
#    fig.update_layout(
#       title=f'Évolution des prix de {selected_column} entre {start_date} et {end_date}',
#       xaxis_title="Date",
#       yaxis_title=f'{selected_column} price $',
#    )

    # Utilisation de st.plotly_chart pour afficher le graphique dans Streamlit
#    st.plotly_chart(fig)


    
######################## SCRIPT POUR AFFICHER  L'EVOLUTION DES COURS EN COURBE AVEC LES BANDE DE BOLLINGER A SUPPRIMER ################################################################################################################################################################################


#def display_price_evolution_with_bollinger_bands(filtered_data, selected_column, start_date, end_date):
#    fig = go.Figure()

    # Tracer la série de prix
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[selected_column], mode='lines', name=selected_column, line=dict(color='gold')))

    # Calcul des moyennes mobiles et des bandes de Bollinger
#    rolling_mean = filtered_data[selected_column].rolling(window=20).mean()
#    rolling_std = filtered_data[selected_column].rolling(window=20).std()
#    upper_band = rolling_mean + (rolling_std * 2)
#    lower_band = rolling_mean - (rolling_std * 2)

    # Tracer les bandes de Bollinger
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=upper_band, mode='lines', name='Upper Bollinger Band', line=dict(color='red')))
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=rolling_mean, mode='lines', name='Moving Average', line=dict(color='white')))
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=lower_band, mode='lines', name='Lower Bollinger Band', line=dict(color='red')))

    # Mise en forme du graphique
#    fig.update_layout(
#       title=f'Évolution des prix de {selected_column} avec bandes de Bollinger entre {start_date} et {end_date}',
#       xaxis_title="Date",
#       yaxis_title=f'{selected_column} price $',
#        width = 800,
#        height = 600,
#    )

    # Utilisation de st.plotly_chart pour afficher le graphique dans Streamlit
#    st.plotly_chart(fig)



######################## ############################################################################################# PUR PUR avec bande+bolinge MAIS A SUPPPRIMER ########################################################################################################################################################
    


#def display_price_evolution_with_custom_bollinger_bands(filtered_data, selected_column, start_date, end_date, rolling_window, num_std_dev):
#    fig = go.Figure()

    # Tracer la série de prix
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data[selected_column], mode='lines', name=selected_column, line=dict(color='gold')))

    # Calcul des moyennes mobiles et des bandes de Bollinger en utilisant les paramètres choisis par l'utilisateur
#    rolling_mean = filtered_data[selected_column].rolling(window=rolling_window).mean()
#    rolling_std = filtered_data[selected_column].rolling(window=rolling_window).std()
#    upper_band = rolling_mean + (rolling_std * num_std_dev)
#    lower_band = rolling_mean - (rolling_std * num_std_dev)

    # Tracer les bandes de Bollinger
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=upper_band, mode='lines', name='Upper Bollinger Band', line=dict(color='white')))
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=rolling_mean, mode='lines', name='Moving Average', line=dict(color='red')))
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=lower_band, mode='lines', name='Lower Bollinger Band', line=dict(color='white')))

    # Mise en forme du graphique
#    fig.update_layout(
#       title=f'Évolution des prix de {selected_column} avec bandes de Bollinger entre {start_date} et {end_date}',
#       xaxis_title="Date",
#       yaxis_title=f'{selected_column} price $',
#       width=800,  # Largeur de la figure en pixels
#       height=600,  # Hauteur de la figure en pixels
#    )

    # Utilisation de st.plotly_chart pour afficher le graphique dans Streamlit
#    st.plotly_chart(fig)
    
#A METTRE DANS MAIN
#        rolling_window = st.slider('Période de la moyenne mobile et des bandes de Bollinger', min_value=5, max_value=50, value=20)
#        num_std_dev = st.slider('Nombre d\'écarts-types pour les bandes de Bollinger', min_value=1, max_value=3, value=2)
    



######################## ############################################################################################# FONCTION POUR REALISER L'AFFICHAGE EN BAR  DE LA COURBE SANS INDICATEURS e########################################################################################################################################################
    

#def display_price_evolution_bar(filtered_data, selected_column, start_date, end_date):
#    fig = go.Figure()

    # Tracer la série de prix
#    fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data[selected_column], name=selected_column, marker_color='gold'))

    # Mise en forme du graphique
#    fig.update_layout(
#       title=f'Évolution des prix de {selected_column} entre {start_date} et {end_date}',
#       xaxis_title="Date",
#       yaxis_title=f'{selected_column} price $',
#       width=800,  # Largeur de la figure en pixels
#       height=600,  # Hauteur de la figure en pixels
#    )

    # Utilisation de st.plotly_chart pour afficher le graphique dans Streamlit
#    st.plotly_chart(fig)

#import altair as alt
#import pandas as pd

#def display_price_evolution_barr(filtered_data, selected_column, start_date, end_date):
#    data = pd.DataFrame({'Date': filtered_data.index, 'Price': filtered_data[selected_column]})
#    chart = alt.Chart(data).mark_bar(color='gold').encode(x='Date', y='Price').properties(
#        title=f'Évolution des prix de {selected_column} entre {start_date} et {end_date}'
#    )
#    st.altair_chart(chart, use_container_width=True)


#from bokeh.plotting import figure, show
#from bokeh.io import output_notebook
#from bokeh.models import ColumnDataSource

#def display_price_evolution_baar(filtered_data, selected_column, start_date, end_date):
#    output_notebook()
#    data = {'x': filtered_data.index, 'y': filtered_data[selected_column]}
#    source = ColumnDataSource(data=data)
#    p = figure(x_axis_type='datetime', title=f'Évolution des prix de {selected_column} entre {start_date} et {end_date}', plot_height=600, plot_width=800)
#    p.vbar(x='x', top='y', width=0.5, source=source, color='gold')
#    p.xaxis.axis_label = 'Date'
#    p.yaxis.axis_label = f'{selected_column} price $'
#    st.bokeh_chart(p, use_container_width=True)


#import plotly.express as px
#import plotly.graph_objects as go

#def display_price_evolution_baaar(filtered_data, selected_column, start_date, end_date):
#    fig = px.bar(x=filtered_data.index, y=filtered_data[selected_column], title=f'Évolution des prix de {selected_column} entre {start_date} et {end_date}')
#    fig.update_traces(marker_color='gold')
#    fig.update_layout(xaxis_title="Date", yaxis_title=f'{selected_column} price $', width=800, height=600)
#    st.plotly_chart(fig)


######################## FONCTION POUR REALISER L'AFFICHAGE EN BAR  DE LA COURBE AVEC INDICATEURS #####################################################################################################################################################################################################################################################

#def display_price_evolution_with_ema_and_sma(filtered_data, selected_column, start_date, end_date, ema_span, sma_span):
#    fig = go.Figure()

    # Tracer la série de prix
#    fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data[selected_column], name=selected_column, marker_color='gold'))
    
    # Calcul de la moyenne mobile exponentielle
#    ema_values = filtered_data[selected_column].ewm(span=ema_span, adjust=False).mean()

    # Calcul de la moyenne mobile simple
#    sma_values = filtered_data[selected_column].rolling(window=sma_span).mean()

    # Tracer les moyennes mobiles
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=ema_values, mode='lines', name=f'EMA ({ema_span})', line=dict(color='white')))
#    fig.add_trace(go.Scatter(x=filtered_data.index, y=sma_values, mode='lines', name=f'SMA ({sma_span})', line=dict(color='red')))

    # Mise en forme du graphique
#    fig.update_layout(
#       title=f'Évolution des prix de {selected_column} avec MME ({ema_span}) et MMS ({sma_span}) entre {start_date} et {end_date}',
#       xaxis_title="Date",
#       yaxis_title=f'{selected_column} price $',
#       width=800,  # Largeur de la figure en pixels
#       height=600,  # Hauteur de la figure en pixels
#    )

#    # Utilisation de st.plotly_chart pour afficher le graphique dans Streamlit
#    st.plotly_chart(fig)
