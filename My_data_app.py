
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from scraping_auto import scraping_generique 


st.markdown("""
    <h1 style='text-align: center; color: #1cb771ff; font-family: "Trebuchet MS", sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 10px;margin-top: -50px;'>
        DAKAR AUTO INSIGHTS
    </h1>
    """, unsafe_allow_html=True)            
st.markdown("""
     <div style="
        background-color: #1E2129; 
        padding: 10px; 
        border-radius: 10px; 
        border-left: 8px solid #1cb771ff; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;">
        <h3 style="color: #1cb771ff; margin-top: 0;"> À propos de DAKAR AUTO INSIGHTS</h3>
        <p style="color: #FAFAFA; font-size: 15px; line-height: 1.6;">
           Cette application développée avec Streamlit permet de scraper, charger, visualiser et exporter des données
           d'annonces de ventes et locations de voitures, motos et scooters sur le site Dakar-Auto.
           Elle s'adresse aux utilisateurs souhaitant collecter et analyser des données du marché d'Automobile au Sénégal.
        </p>
        <hr style="border: 0.5px solid #d1d3d8; margin: 20px 0;">
        <p style="font-weight: bold; color: #FAFAFA; margin-bottom: 10px;"> Sources des données (Dakar-Auto) :</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <a href="https://dakar-auto.com/senegal/voitures-4" target="_blank" style="text-decoration: none; background: #1cb771ff; color: white; padding: 8px 15px; border-radius: 20px; font-size: 0.9em;"> Voitures</a>
            <a href="https://dakar-auto.com/senegal/motos-and-scooters-3" target="_blank" style="text-decoration: none; background: #1cb771ff; color: white; padding: 8px 15px; border-radius: 20px; font-size: 0.9em;"> Motos</a>
            <a href="https://dakar-auto.com/senegal/location-de-voitures-19" target="_blank" style="text-decoration: none; background: #1cb771ff; color: white; padding: 8px 15px; border-radius: 20px; font-size: 0.9em;"> Locations</a>
        </div>

    </div>
    """, unsafe_allow_html=True)

# Web scraping de données des véhicules sur Dakar Auto
@st.cache_data

def conversion_df(df):
    # Mettre la conversion en cache pour éviter de relancer le calcul à chaque rafraîchissement
    return df.to_csv().encode('utf-8')

def load(dataframe, title, key, key1) :    
    
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #1E2129;
        color: white;
        font-size: 15px;
        width: 100%;
        height: 10px;
        border-radius: 13px;
        display: block;
        margin: auto;
    }
    /* 2. État au survol (HOVER) */
    div.stButton > button:hover {
        background-color: #1cb771ff; 
        color: #ffffff;
        cursor: pointer;           
        transform: translateY(-2px); 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
          
    </style>
    """, unsafe_allow_html=True)
    
    # Création de 3 colonnes avec celle du milieu plus large
    col1, col2, col3 = st.columns([1, 5, 1])
    
    with col2:
        if st.button(title, key1):
            st.subheader('Dimensions des données')
            st.write('Dimensions : ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)

            csv = conversion_df(dataframe)

            st.download_button(
                label="Télécharger les données en format CSV",
                data=csv,
                file_name='Data.csv',
                mime='text/csv',
                key = key)
            


# Menu principal
nbr_page = st.sidebar.slider('nombre de page à scraper', 1, 300)
choix = st.sidebar.selectbox('Options', ["Scraper avec BeautifulSoup", "Charger données (Web Scraper)", "visualiser des données", "formulaire d'evaluation"])

# Scraper les données

if choix == "Scraper avec BeautifulSoup":
    st.subheader("Scraper les données")
    
    type_vehicule = st.selectbox("Choisir le type de véhicule", ["voiture", "moto", "location"])
    
    url_dict = {
        "voiture": "https://dakar-auto.com/senegal/voitures-4",
        "moto": "https://dakar-auto.com/senegal/motos-and-scooters-3",
        "location": "https://dakar-auto.com/senegal/location-de-voitures-19"
    }
    
    if st.button("Démarrer le scraping"):
        with st.spinner("Scraping en cours..."):
            df = scraping_generique(url_dict[type_vehicule], nbr_page, type_vehicule)
            st.success(f"Scraping terminé pour {type_vehicule} !")
            st.dataframe(df)
            # Sauvegarde automatique
            df.to_csv(f"{type_vehicule}_nettoye.csv", index=False)
            st.write(f"Données sauvegardées dans {type_vehicule}_nettoye.csv")

            # utilisation directe de load()
            load(
                dataframe=df,
                title=f"Afficher les {type_vehicule}s",
                key=f"dl_{type_vehicule}",
                key1=f"btn_{type_vehicule}"
            )


# Télécharger CSV non nettoyé

elif choix == "Charger données (Web Scraper)":
    voitures = pd.read_csv('data/dakar_Auto_ voitures.csv')
    Motocycles = pd.read_csv('data/dakar_motos_scooters.csv') 
    location = pd.read_csv('data/dakar_location_voiture.csv')

    # Supprimer les colonnes automatiques de l'outil Web Scraper
    colonnes_a_supprimer = ['web_scraper_order', 'web_scraper_start_url', 'containers_urls', 'container_urls']
    
    voitures = voitures.drop(columns=colonnes_a_supprimer, errors='ignore')
    Motocycles = Motocycles.drop(columns=colonnes_a_supprimer, errors='ignore')
    location = location.drop(columns=colonnes_a_supprimer, errors='ignore')

    load(voitures, 'dakar_Auto_ voitures', '1', '101')
    load(Motocycles, 'dakar_motos_scooters', '2', '102')
    load(location , 'dakar_location_voiture', '3', '103')


# Dashboard des données nettoyées

elif choix == "visualiser des données":
    st.markdown("<h2 style='text-align: center; color: #4A90E2;'>Tableau de Bord des données</h2>", unsafe_allow_html=True)
    
    # Récupération du choix de l'utilisateur
    type_dash = st.selectbox("Sélectionnez la catégorie ", ["voiture", "moto", "location"])
    
    # Configuration du style sombre
    plt.style.use('dark_background')
    
    try:
        # Chargement du fichier correspondant au choix 
        # Si l'utilisateur choisit "moto", il chargera "moto_nettoye.csv"
        df = pd.read_csv(f"{type_dash}_nettoye.csv")
        
        # Nettoyage et conversion
        df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
        df['annee'] = pd.to_numeric(df['annee'], errors='coerce')
        df = df.dropna(subset=['prix', 'annee', 'marque'])

        # Calculs statistiques rapides
        marque_populaire = df['marque'].mode()[0]
        prix_moyen = df['prix'].mean()

        st.info(f"""
        **Analyse rapide du marché :**
        * La marque la plus présente est **{marque_populaire}**.
        * Le prix moyen d'un véhicule sur cette sélection est de **{prix_moyen:,.0f} CFA**.
        """)

        # --- Colonnes pour les deux premiers graphiques ---
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"<h4 style='text-align: center; color: #D4AF37;'>Top 5 des Marques ({type_dash})</h4>", unsafe_allow_html=True)
            top_5 = df['marque'].value_counts().head(5)
            fig1, ax1 = plt.subplots(figsize=(10, 7))
            sns.barplot(x=top_5.index, y=top_5.values, palette="Blues_r", ax=ax1)
            plt.title(f'Marques les plus présentes en {type_dash}')
            sns.despine()
            st.pyplot(fig1)

        with col2:
            st.markdown(f"<h4 style='text-align: center; color: #D4AF37;'> Évolution des Prix ({type_dash})</h4>", unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(10, 7))
            df_filt = df[df['annee'] > 2000]
            # On vérifie si la colonne 'etat' existe pour éviter une erreur
            hue_col = "etat" if "etat" in df.columns else None
            sns.lineplot(data=df_filt, x="annee", y="prix", hue=hue_col, marker="o", linewidth=2.5, palette="flare")
            plt.title('Variation du prix selon l\'année')
            ax2.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig2)

        # --- Container pour le graphique du bas (Prix Moyen) ---
        st.write("---")
        with st.container():
            st.markdown(f"<h4 style='text-align: center; color: #D4AF37;'> Prix Moyen par Marque : {type_dash}</h4>", unsafe_allow_html=True)
            fig5, ax5 = plt.subplots(figsize=(12, 6))
            
            top_10_names = df['marque'].value_counts().head(10).index
            df_top10 = df[df['marque'].isin(top_10_names)]
            avg_price = df_top10.groupby('marque')['prix'].mean().sort_values(ascending=False)
            
            sns.barplot(x=avg_price.index, y=avg_price.values, palette="YlOrBr_r", ax=ax5)
            plt.xticks(rotation=45)
            plt.ylabel("Prix Moyen (CFA)")
            st.pyplot(fig5)

    except FileNotFoundError:
        st.error(f" Le fichier '{type_dash}_nettoye.csv' est introuvable. Veuillez d'abord scraper ou nettoyer les données pour cette catégorie.")
    

# 4. Formulaire d'évaluation
else :
    # components.html("""
    # <iframe src="https://ee.kobotoolbox.org/x/iVerXHuo" width="800" height="1100"></iframe>
    # """,height=1100,width=800)

    st.markdown("""
    <h3 style='text-align: center; color: #1cb771ff; font-family: "Trebuchet MS", sans-serif; font-weight: 500; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 10px;'>
        Donnez votre avis sur notre application
    </h3><br></br>
    """, unsafe_allow_html=True) 
    # centrer les deux boutons
    col1, col2 = st.columns(2)
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #1E2129;
        color: white;
        font-size: 15px;
        width: 100%;
        height: 10px;
        border-radius: 13px;
        display: block;
        margin: auto;
    }
    /* 2. État au survol (HOVER) */
    div.stButton > button:hover {
        background-color: #1cb771ff; /* Change en vert au survol */
        color: #ffffff;
        cursor: pointer;           /* Change le curseur en main */
        transform: translateY(-2px); /* Petit effet de soulèvement */
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2); /* Ajoute une ombre */
    }
          
    </style>
    """, unsafe_allow_html=True)
    with col1:
        if st.button("Kobo Evaluation Form"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://ee.kobotoolbox.org/x/iVerXHuo">',
                unsafe_allow_html=True
            )

    with col2:
        if st.button("Google Forms Evaluation"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://docs.google.com/forms/d/e/1FAIpQLSeOdziUM7r3-NA5NL_WONxK8vtrehTAr5ed1oNlDDjtx8mW1A/viewform?usp=sharing&ouid=103092445923488631461">',
                unsafe_allow_html=True
            )
