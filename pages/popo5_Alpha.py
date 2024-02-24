import streamlit as st
import pandas as pd
import os
import base64
import pyarrow.lib as _lib
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage


import numpy as np
from pypfopt import EfficientFrontier, expected_returns, risk_models 

#Ce script Python réalise une analyse de l'évolution des cours financiers et l'optimisation d'un portefeuille selon le ratio de Sharpe ou le modèle de Markowitz. Voici les fonctions principales du script:

#- `telecharger_donnees_historiques(symboles, date_debut, date_fin)`: Cette fonction permet de télécharger les données historiques des cours de plusieurs symboles. Elle renvoie un dictionnaire contenant les symboles en clé et les cours de clôture en valeur.

#- `afficher_graphique_evolution_cours(data)`: Cette fonction affiche un graphique de l'évolution des prix de clôture pour chaque symbole dans les données fournies.

#- `choisir_produits_financiers(symboles)`: Cette fonction permet à l'utilisateur de choisir les produits financiers à inclure dans le portefeuille en utilisant des boutons de sélection. Elle renvoie une liste des produits sélectionnés ainsi que les poids correspondants.

#- `choisir_dates()`: Cette fonction permet à l'utilisateur de choisir les dates de début et de fin pour l'analyse des cours financiers. Elle renvoie les dates sélectionnées.

#- `calcul_variable(data)`: Cette fonction calcule les rendements et la covariance des cours financiers à partir des données fournies. Elle renvoie les rendements et la matrice de covariance.

#- `reduce_dimensionality(tolerance_level, tolerance_range, min_volatility, max_volatility)`: Cette fonction permet de réduire la dimensionnalité des portefeuilles en fonction d'un niveau de tolérance et d'une plage de volatilité. Elle renvoie le niveau de tolérance réduit.

#- `calculate_volatility_range(poids, data)`: Cette fonction calcule la volatilité minimale et maximale des portefeuilles en utilisant des poids aléatoires pour chaque actif financier.

#- `optimize_portfolio(data, total_portfolio_value)`: Cette fonction optimise le portefeuille en maximisant le ratio de Sharpe en utilisant les données fournies. Elle renvoie les poids du portefeuille optimisé.

#- `calculate_portfolio_metrics(poids, cov_matrix_annual, returns)`: Cette fonction calcule les métriques du portefeuille, telles que le rendement annuel, la volatilité et la variance.

#- `main()`: Cette fonction lance l'ensemble de l'application, permettant à l'utilisateur de choisir les produits financiers, les dates et d'effectuer l'optimisation du portefeuille.








#https://media.istockphoto.com/id/1047735224/fr/photo/le-flux-de-nuage-au-dessus-des-montagnes-avec-des-%C3%A9toiles-soir%C3%A9e-nocturne.jpg?s=612x612&w=0&k=20&c=JRXTp7Ut-4zf-K6ftbiU0GbUncGUI2mi1oKwhm-3OTM=
#https://cdn.pixabay.com/photo/2015/04/19/08/33/flower-729513_1280.jpg
st.set_page_config(layout="wide")

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

st.markdown("""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    """, unsafe_allow_html=True)

#https://cdn.pixabay.com/photo/2016/06/25/12/52/laptop-1478822_640.jpg
#https://cdn.pixabay.com/photo/2015/04/19/08/33/flower-729512_640.jpg
st.markdown(
    """
    <style>
   .stApp {
        /* Utilisez l'URL de votre image comme valeur de background-image */
      
        background-image: url('https://cdn.pixabay.com/photo/2016/06/25/12/52/laptop-1478822_640.jpg');
        background-size: cover; /* Ajuste la taille de l'image pour couvrir tout l'arrière-plan */
        background-repeat: no-repeat; /* Empêche la répétition de l'image */
        background-position: center center; /* Centre l'image horizontalement et verticalement */
        color: #ffffff;
        font-family: Arial, sans-serif;
        padding: 1rem;
        
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


def main():
    
######## 1-MISE EN PLACE DES ELEMENTS DE LA PAGE PRINCIPALE ###############################################

    
    html_titre = """ 
    <div style="padding: 13px; background-color: #5f9ea0; border: 5px solid #e5e5e5; border-radius: 10px;">
    <h1 style="color:white; text-align: center;">🤖 PLATEFORME DE DETERMINATION DU PORTE FEUILLE CLIENT LE PLUS EFFICIENT 🤖<small><br> Powered by EMERALD SECURITIES SERVICES </small></h1></h1>
    </div> 
    """
    st.markdown(html_titre, unsafe_allow_html = True) 
    
    st.markdown(hide_st_style, unsafe_allow_html=True)


if __name__ =='__main__':
    
    main()


##################### declaratio des variables ##############################################################


tolerance_range = [28, 135] # intervalle du nombre de choix des mots

    # Widget pour entrer la valeur de tolerance_level
tolerance_level = st.number_input("Valeur de tolerance_level", value=25)


    # Widget pour entrer la valeur a investir
portfolio_value = st.number_input("Entre la valeur a investir ", value=2500000)

portfolio_value = float(portfolio_value)


##################### FONCTION POUR TELECHARGER HISTORIQUEMENT LES PRODUITS FINACIER  ##############################################################

def telecharger_donnees_historiques(symboles, date_debut, date_fin):
    data = {}
    for symbole in symboles:
        stock = yf.Ticker(symbole)
        history = stock.history(start=date_debut, end=date_fin)
        data[symbole] = history["Close"]
      
    return data

#####################  FONCTION POUR FAIRE L'AFFICHAGE DE 'EVOLUTION DES PRODUITS FINACIER  ##############################################################



def afficher_graphique_evolution_cours(data):
    fig, ax = plt.subplots(figsize=(7,7))
    for symbole, close_prices in data.items():
        ax.plot(close_prices, label=symbole)
    ax.set_title('Evolution des prix de clôture')
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel('Close price $', fontsize=10)
    ax.legend(loc='upper left')
    st.pyplot(fig)


##################### FONCTION POUR CHOISIR LES PRODUITS FINANCIER S ##############################################################


def choisir_produits_financiers(symboles):
    produits = []
    poids = []
    choix_max = min(4, len(symboles))
    
    # Ajouter une valeur spéciale à la liste symboles
    #symboles.append("Aucun choix")
    
    for i in range(choix_max):
        produit = st.selectbox(f"Produit financier {i+1}", symboles)
        
        # Vérifier si l'utilisateur a choisi la valeur spéciale
        if produit == "Aucun choix":
            break
        
        poids_produit = st.slider(f"Poids pour {produit} (%)", min_value=3, max_value=100, value=20)
        produits.append(produit)
        poids.append(poids_produit/100)
        symboles = [symbole for symbole in symboles if symbole != produit]
    
    # Si aucun produit n'a été choisi, supprimer les poids
    if len(produits) == 0:
        poids = []
    
    return produits, poids


##################### FONCTION POUR AFFICHER LA DATE ###########################################################################

def choisir_dates():
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")
    return date_debut, date_fin



##################### FONCTION POUR CALCULER LE RETURNS ET LA COVARIANCE ##############################################################

def calcul_variable (data):
    data = pd.DataFrame(data)
    returns = data.pct_change()
    cov_matrix_annual = returns.cov() * 252
    return returns, cov_matrix_annual


##################### FONCTION MAIN POUR LANCER TOUTE L'APPLICATION ET LES BOUTONS #############################################################

#portfolios.append((portfolio_return, portfolio_volatility)) ajouter à l'intérieur de la boucle #for permet d'ajouter les rendements et les volatilités de chaque portefeuille à la liste portfolios. #Ensuite, la fonction zip(*portfolios) 

# pour séparer les rendements et les volatilités dans deux listes #distinctes portfolio_returns et portfolio_volatilities. 

# Cette fonction permet de calculer l'intervalle de volatilite de tous les produits financier choisis q

def calculate_volatility_range(poids, data):
    
    #data = pd.DataFrame(data)
    n_portfolios = 1000
    mu = expected_returns.mean_historical_return(data)
    s = risk_models.sample_cov(data)
    portfolios = []
    portfolio_returns = []
    
    for _ in range(n_portfolios):
        poids = poids / np.sum(poids)
        portfolio_return = np.dot(mu, poids)
        portfolio_volatility = np.sqrt(np.dot(poids.T, np.dot(s, poids)))
        portfolios.append((portfolio_return, portfolio_volatility))

    portfolio_returns, portfolio_volatilities = zip(*portfolios)
    min_volatility = min(portfolio_volatilities)
    max_volatility = max(portfolio_volatilities)

    return min_volatility, max_volatility


##################### FONCTION POUR REALISER LA REDUCTION DE DIMENSINNALITE ##############################################################




def reduce_dimensionality(tolerance_level, tolerance_range, min_volatility, max_volatility):
    # Remappage linéaire du niveau de tolérance dans l'intervalle de volatilité
     tol_min, tol_max = tolerance_range
     vol_min, vol_max = min_volatility, max_volatility
     reduced_tolerance = (tolerance_level - tol_min) * (vol_max - vol_min) / (tol_max - tol_min) + vol_min

     return reduced_tolerance
#reduced_tolerance = (tolerance_level - tolerance_range[0][0]) * (max_volatility - min_volatility) / (tolerance_range[1] - tolerance_range[0]) + min_volatility

################ FONCTION MAXIMISANT LE RATION DE SHARPE QUI FAIT RESSORTIR LE RATIO DE SHARPE ############################################################################

#from pypfopt import EfficientFrontier, DiscreteAllocation

################ FONCTION MAXIMISANT LE RATION DE SHARPE ############################################################################

#J'ai apporté les modifications suivantes:

#1. J'ai ajouté l'importation de la bibliothèque NumPy (numpy) pour utiliser ses fonctions mathématiques.

#2. J'ai modifié la fonction `calcul_variable` pour appeler correctement la fonction `cov()` pour calculer 
#la matrice de covariance annuelle.

#3. J'ai ajouté une conversion de la liste `poids` en un tableau numpy `poids_array` pour effectuer les calculs
#de variance.

#4. J'ai modifié le calcul des pourcentages pour multiplier les valeurs par 100 avant de les arrondir.


def calculer_ratio_sharpe(produits, poids, data):
    # Calculer les rendements logarithmiques
    log_returns = np.log(data.pct_change() + 1)
    
    # Générer les poids de rééquilibrage
    rebalance_weights = poids / np.sum(poids)
    
    # Calculer les rendements attendus, annualisés par un facteur de 252
    expected_returns = np.sum((log_returns.mean() * rebalance_weights) * 252)
    
    # Calculer la volatilité attendue, annualisée par un facteur de 252
    expected_volatility = np.sqrt(np.dot(rebalance_weights.T, np.dot(log_returns.cov() * 252, rebalance_weights)))
    
    # Calculer le ratio de Sharpe
    sharpe_ratio = expected_returns / expected_volatility
    
    return sharpe_ratio, expected_returns, expected_volatility, rebalance_weights



###################### APPLIQUEMENT DE LA FONCTION DE MONTE CARLO ###############################################################################



def run_monte_carlo_simulation(produits, data):
    number_of_symbols = len(produits)
    log_return = np.log(data.pct_change() +1 )
    

    # Initialize the components, to run a Monte Carlo Simulation.
    num_of_portfolios = 5000
    all_weights = np.zeros((num_of_portfolios, number_of_symbols))
    ret_arr = np.zeros(num_of_portfolios)
    vol_arr = np.zeros(num_of_portfolios)
    sharpe_arr = np.zeros(num_of_portfolios)

    # Start the simulations.
    for ind in range(num_of_portfolios):
        weights = np.array(np.random.random(number_of_symbols))
        weights = weights / np.sum(weights)
        all_weights[ind, :] = weights
        ret_arr[ind] = np.sum((log_return.mean() * weights) * 252)
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_return.cov() * 252, weights)))
        sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]

    simulations_data = [ret_arr, vol_arr, sharpe_arr, all_weights]
    simulations_df = pd.DataFrame(data=simulations_data).T
    simulations_df.columns = ['Returns', 'Volatility', 'Sharpe Ratio', 'Portfolio Weights']
    simulations_df = simulations_df.infer_objects()
        # Return the Max Sharpe Ratio from the run.
    max_sharpe_ratio = simulations_df.loc[simulations_df['Sharpe Ratio'].idxmax()]

    # Return the Min Volatility from the run.
    min_volatility = simulations_df.loc[simulations_df['Volatility'].idxmin()]

    return simulations_df, min_volatility, max_sharpe_ratio


################################### FONCTION POUR AFFICHER 
#import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt
#import streamlit as st

def plot_portfolio(simulations_df):
    # Return the Max Sharpe Ratio from the run.
    max_sharpe_ratio = simulations_df.loc[simulations_df['Sharpe Ratio'].idxmax()]

    # Return the Min Volatility from the run.
    min_volatility = simulations_df.loc[simulations_df['Volatility'].idxmin()]

    # Create the figure and axes with desired size.
    fig, ax = plt.subplots(figsize=(7, 7))

    # Plot the data on a Scatter plot.
    scatter = ax.scatter(
        y=simulations_df['Returns'],
        x=simulations_df['Volatility'],
        c=simulations_df['Sharpe Ratio'],
        cmap='RdYlBu'
    )

    # Give the Plot some labels, and titles.
    ax.set_title('Portfolio Returns Vs. Risk')
    plt.colorbar(scatter, ax=ax, label='Sharpe Ratio')
    ax.set_xlabel('Standard Deviation')
    ax.set_ylabel('Returns')

    # Plot the Max Sharpe Ratio, using a `Red Star`.
    ax.scatter(
        max_sharpe_ratio[1],
        max_sharpe_ratio[0],
        marker=(5, 1, 0),
        color='r',
        s=600
    )

    # Plot the Min Volatility, using a `Blue Star`.
    ax.scatter(
        min_volatility[1],
        min_volatility[0],
        marker=(5, 1, 0),
        color='b',
        s=600
    )

    # Show the plot using streamlit.
    st.pyplot(fig)


##################### FONCTION MAIN POUR LANCER TOUTE L'APPLICATION ET LES BOUTONS #############################################################


#La fonction `telecharger_donnees_historiques(symboles, date_debut, date_fin)` doit renvoyer un dictionnaire contenant les données historiques. Vous devez donc le modifier pour qu'il renvoie le dictionnaire contenant les données historiques.


#`telecharger_donnees_historiques(symboles, date_debut, date_fin)` doit renvoyer un dictionnaire contenant les données historiques. Vous devez donc le modifier pour qu'il renvoie le dictionnaire contenant les données historiques.


import warnings
import pandas as pd
import streamlit as st
#from my_module import choisir_produits_financiers, choisir_dates, telecharger_donnees_historiques, afficher_graphique_evolution_cours, calculer_ratio_sharpe, run_monte_carlo_simulation, plot_portfolio

def main():
    symboles = ['Aucun choix', 'EN.PA', 'LR.PA', 'ML.PA', 'ACA.PA', 'AI.PA', 'VIE.PA', 'ATO.PA', 'DG.PA', 'VIV.PA', 'BN.PA', 'AIR.PA', 'SW.PA', 'HOs.PA', 'MC.PA', 'SGO.PA', 'ORA.PA', 'CA.PA', 'SAN.PA', 'MC.PA']
    produits, poids = choisir_produits_financiers(symboles)
    date_debut, date_fin = choisir_dates()

    if st.button("Télécharger les données historiques"):
        if not any(produits):
            st.info("Veuillez choisir un produit financier car vous n'avez choisis aucun !!!")
            
            #st.warning("Aucun produit financier sélectionné.")
            #st.error("Aucun produit financier sélectionné.")
            return

        with st.spinner('Téléchargement des données en cours...'):
            data = telecharger_donnees_historiques(produits, date_debut, date_fin)
            data = pd.DataFrame(data)

        st.write("Données historiques :")
        st.write(data)

        st.write("Graphique d'évolution des cours :")
        afficher_graphique_evolution_cours(data)

        sharpe_ratio, expected_returns, expected_volatility, rebalance_weights = calculer_ratio_sharpe(produits, poids, data)

        # Exécution de la simulation
        simulations_df, max_sharpe_ratio, min_volatility = run_monte_carlo_simulation(produits, data)

        st.write("Résultats de l'analyse :")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rendement Annuel (%)", expected_returns * 100)
        col2.metric("Volatilité Annuelle (%)", expected_volatility * 100)
        col3.metric("Variance Annuelle (%)", expected_volatility ** 100)
        col4.metric("Ratio de Sharpe Annuel", sharpe_ratio)

        coll1, coll2, coll3 = st.columns(3)
        coll1.metric("Rendement Max Annuel (%)", max_sharpe_ratio["Returns"] * 100)
        coll2.metric("Volatilité Max Annuelle", max_sharpe_ratio["Volatility"] * 100)
        coll3.metric("Valeur Max du Ratio de Sharpe", max_sharpe_ratio["Sharpe Ratio"])

        coll4, coll5, coll6 = st.columns(3)
        coll4.metric("Rendement Min Annuel (%)", min_volatility["Returns"] * 100)
        coll5.metric("Volatilité Min Annuelle", min_volatility["Volatility"] * 100)
        coll6.metric("Valeur Min du Ratio de Sharpe", min_volatility["Sharpe Ratio"])

        coll7, coll8, coll9 = st.columns(3)
        coll7.metric(label="Rendement Moyen Annuel", value=simulations_df['Returns'].mean() * 100)
        coll8.metric(label="Volatilité Moyenne", value=simulations_df['Volatility'].mean() * 100)
        coll9.metric(label="Moyenne du Ratio de Sharpe", value=simulations_df['Sharpe Ratio'].mean())

        st.write("Weights de rééquilibrage :", rebalance_weights.tolist())
        st.dataframe(min_volatility)
        st.dataframe(max_sharpe_ratio)

       # if st.button("Afficher le diagramme"):
            
        st.write("Graphique d'évolution des cours :")
        plot_portfolio(simulations_df)

    #else:
    #    st.warning("Aucun produit financier sélectionné.")




if __name__ == "__main__":
    main()

#- InvestProfilOptimizer
#- ProfilAdvisor
#- PortefolioOptimum
#- DeciWealthOptimizer
#- InvestDecisionProdef main():
