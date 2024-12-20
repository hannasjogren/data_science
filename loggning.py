import logging
# Konfigurera loggern
logging.basicConfig(
    filename='testning_log.txt',  # Filen ska skapas här
    format='[%(asctime)s][%(levelname)s] %(message)s',
    level=logging.DEBUG  # Minsta loggnivå är DEBUG
)

# Skapa en logger
logger = logging.getLogger(__name__)
logger.debug("Detta är ett debugmeddelande")
logger.info("Detta är ett informationsmeddelande")
logger.warning("Detta är ett varningsmeddelande")
logger.error("Detta är ett felmeddelande")
logger.critical("Detta är ett kritiskt felmeddelande")

import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.adlibris.com/se/kampanj/manadens-topplista'

# Försök att hämta huvudkampanjsidan
try:
    logger.info(f"Försöker hämta data från: {base_url}")
    response = requests.get(base_url)
    response.raise_for_status()  # Om statuskod inte är 200, kommer det att höja ett undantag
    logger.info(f"Framgångsrikt hämtat data från {base_url}. Statuskod: {response.status_code}")
except requests.exceptions.RequestException as e:
    logger.error(f"Fel vid hämtning av data: {e}")
    response = None

# Om data hämtades, fortsätt bearbetningen
if response and response.status_code == 200:
    logger.info("Bearbetar innehållet från sidan.")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Hitta alla produkter (böcker)
    products = soup.find_all('div', class_='product-panel__product')

    # Lista för att lagra böckerna
    books_data = []

    # Loopa igenom varje bok och extrahera titel, författare och pris
    for product in products:
        try:
            # Extrahera boktitel
            title = product.find('h3', itemprop='name')
            title_text = title.get_text(strip=True) if title else 'Ingen titel'

            # Extrahera författare
            author = product.find('span', itemprop='author')
            author_name = author.get_text(strip=True) if author else 'Ingen författare'

            # Extrahera pris
            price = product.find('div', itemprop='offers')
            price_value = price.get_text(strip=True) if price else 'Ingen prisinformation'

            # Lägg till bokinformation i listan
            books_data.append({
                'title': title_text,
                'author': author_name,
                'price': price_value
            })

            # Logga information om varje bok
            logger.info(f"Extraherade bok: {title_text} av {author_name}, Pris: {price_value}")

        except Exception as e:
            logger.error(f"Fel vid extrahering av data för en produkt: {e}")
            continue

    # Om några böcker hittades, skapa en DataFrame och logga antalet
    if books_data:
        df = pd.DataFrame(books_data)
        logger.info(f"Antal böcker extraherade: {len(df)}")

        # Skriv ut DataFrame
        print(df)
    else:
        logger.warning("Inga böcker hittades på sidan.")
else:
    logger.error(f"Kunde inte hämta eller bearbeta data från {base_url}. Statuskod: {response.status_code if response else 'Ingen svar från servern.'}")
    
df.info()