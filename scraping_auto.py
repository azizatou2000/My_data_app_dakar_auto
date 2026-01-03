<<<<<<< HEAD
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs

def scraping_generique(url_base, nbr_page, type_vehicule="voiture"):
    """
    Scraping multi-page générique et nettoyage des données.
    """
    df = pd.DataFrame()
    
    for index_page in range(1, int(nbr_page)+1):
        url = f"{url_base}?&page={index_page}"
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item mb-md-3 mb-3')
        liste = []

        for container in containers:
            try:
                # Parsing commun
                info_header = container.find('h2', class_='listing-card__header__title mb-md-2 mb-0').text.strip().split()
                marque = info_header[0] if len(info_header) > 0 else None
                annee = info_header[-1] if len(info_header) > 1 else None

                prix = container.find('h3', class_='listing-card__header__price font-weight-bold text-uppercase mb-0')
                if prix:
                    prix = prix.text.strip().replace('\u202f', '').replace(' F CFA', '').replace(',', '')
                    try:
                        prix = int(prix)
                    except:
                        prix = None
                else:
                    prix = None

                adress_div = container.find('div','col-12 entry-zone-address')
                adresse = adress_div.text.strip().replace("\n", "") if adress_div else None
                
                proprietaire_p = container.find('p', 'time-author m-0')
                proprietaire = proprietaire_p.text.strip() if proprietaire_p else None

                dic = {"marque": marque, 
                       "annee": annee, 
                       "prix": prix, 
                       "adress": adresse, 
                       "proprietaire": proprietaire}

                # Parsing spécifique
                if type_vehicule == "voiture":
                    info_km_carb_vit = container.find_all('li', class_='listing-card__attribute list-inline-item')
                    # Kilométrage
                    if len(info_km_carb_vit) > 1:
                        km = info_km_carb_vit[1].text.strip().replace(' km', '').replace(' ', '')
                        try:
                            dic["kilometrage"] = int(km)
                        except:
                            dic["kilometrage"] = None
                    else:
                        dic["kilometrage"] = None
                    # Boîte vitesse
                    dic["boite_vitesse"] = info_km_carb_vit[2].text.strip() if len(info_km_carb_vit) > 2 else None
                    # Carburant
                    dic["carburant"] = info_km_carb_vit[3].text.strip() if len(info_km_carb_vit) > 3 else None

                elif type_vehicule == "moto":
                    info_km = container.find_all('li', class_='listing-card__attribute list-inline-item')
                    if len(info_km) > 1:
                        km = info_km[1].text.strip().replace(' km', '').replace(' ', '')
                        try:
                            dic["kilometrage"] = int(km)
                        except:
                            dic["kilometrage"] = None
                    else:
                        dic["kilometrage"] = None

                # location : les champs communs suffisent

                liste.append(dic)

            except:
                continue

        DF = pd.DataFrame(liste)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)

    return df

=======
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs

def scraping_generique(url_base, nbr_page, type_vehicule="voiture"):
    """
    Scraping multi-page générique et nettoyage des données.
    """
    df = pd.DataFrame()
    
    for index_page in range(1, int(nbr_page)+1):
        url = f"{url_base}?&page={index_page}"
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item mb-md-3 mb-3')
        liste = []

        for container in containers:
            try:
                # Parsing commun
                info_header = container.find('h2', class_='listing-card__header__title mb-md-2 mb-0').text.strip().split()
                marque = info_header[0] if len(info_header) > 0 else None
                annee = info_header[-1] if len(info_header) > 1 else None

                prix = container.find('h3', class_='listing-card__header__price font-weight-bold text-uppercase mb-0')
                if prix:
                    prix = prix.text.strip().replace('\u202f', '').replace(' F CFA', '').replace(',', '')
                    try:
                        prix = int(prix)
                    except:
                        prix = None
                else:
                    prix = None

                adress_div = container.find('div','col-12 entry-zone-address')
                adresse = adress_div.text.strip().replace("\n", "") if adress_div else None
                
                proprietaire_p = container.find('p', 'time-author m-0')
                proprietaire = proprietaire_p.text.strip() if proprietaire_p else None

                dic = {"marque": marque, 
                       "annee": annee, 
                       "prix": prix, 
                       "adress": adresse, 
                       "proprietaire": proprietaire}

                # Parsing spécifique
                if type_vehicule == "voiture":
                    info_km_carb_vit = container.find_all('li', class_='listing-card__attribute list-inline-item')
                    # Kilométrage
                    if len(info_km_carb_vit) > 1:
                        km = info_km_carb_vit[1].text.strip().replace(' km', '').replace(' ', '')
                        try:
                            dic["kilometrage"] = int(km)
                        except:
                            dic["kilometrage"] = None
                    else:
                        dic["kilometrage"] = None
                    # Boîte vitesse
                    dic["boite_vitesse"] = info_km_carb_vit[2].text.strip() if len(info_km_carb_vit) > 2 else None
                    # Carburant
                    dic["carburant"] = info_km_carb_vit[3].text.strip() if len(info_km_carb_vit) > 3 else None

                elif type_vehicule == "moto":
                    info_km = container.find_all('li', class_='listing-card__attribute list-inline-item')
                    if len(info_km) > 1:
                        km = info_km[1].text.strip().replace(' km', '').replace(' ', '')
                        try:
                            dic["kilometrage"] = int(km)
                        except:
                            dic["kilometrage"] = None
                    else:
                        dic["kilometrage"] = None

                # location : les champs communs suffisent

                liste.append(dic)

            except:
                continue

        DF = pd.DataFrame(liste)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)

    return df

>>>>>>> 7d92aa7 (update)
