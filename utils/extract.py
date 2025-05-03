import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    """Mengambil konten HTML dari URL tertentu."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gagal mengakses URL: {url}. Detail: {e}")

def extract_product_info(card, selectors):
    """Ekstraksi informasi produk dari satu elemen kartu produk."""
    data = {}
    for key, rule in selectors.items():
        if 'class' in rule:
            element = card.find(rule['tag'], class_=rule['class'])
        elif 'string_contains' in rule:
            element = card.find(rule['tag'], string=lambda text: text and rule['string_contains'] in text)
        else:
            element = None
        data[key] = element.text.strip() if element else rule['default']
    return data

def scrape_main(url):
    """Scraping produk dari halaman utama atau halaman tertentu."""
    html = fetch_page_content(url)
    soup = BeautifulSoup(html, 'html.parser')
    product_cards = soup.find_all('div', class_='collection-card')

    if not product_cards:
        raise Exception("Tidak ada produk yang ditemukan pada halaman ini.")

    selectors = {
        'title':  {'tag': 'h3', 'class': 'product-title', 'default': 'Unknown Title'},
        'price':  {'tag': 'div', 'class': 'price-container', 'default': 'Price Unavailable'},
        'rating': {'tag': 'p', 'string_contains': 'Rating', 'default': 'No Rating'},
        'colors': {'tag': 'p', 'string_contains': 'Colors', 'default': 'No Color Info'},
        'size':   {'tag': 'p', 'string_contains': 'Size', 'default': 'No Size Info'},
        'gender': {'tag': 'p', 'string_contains': 'Gender', 'default': 'No Gender Info'}
    }

    products = [extract_product_info(card, selectors) for card in product_cards]
    return products
