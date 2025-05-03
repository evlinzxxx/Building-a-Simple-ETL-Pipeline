import pandas as pd
import numpy as np
from datetime import datetime

class DataTransform:
    """Kelas untuk membersihkan dan mentransformasi data produk."""

    def __init__(self, products):
        self.products = products

    def clean_price(self, price_series):
        price_cleaned = price_series.replace(r'[^\d.]', '', regex=True)
        return pd.to_numeric(price_cleaned, errors='coerce') * 16000

    def clean_rating(self, rating_series):
        rating_cleaned = rating_series.replace(r'[^0-9.]', '', regex=True)
        return pd.to_numeric(rating_cleaned, errors='coerce')
    
    def transform(self):
        df = pd.DataFrame(self.products)

        if df.empty:
            print("Data kosong, tidak ada yang perlu diproses.")
            return pd.DataFrame()

        df = df[df['title'].str.lower() != 'unknown product']

        def clean_price(rp_string):
            try:
                return float(rp_string.replace("Rp", "").replace(".", "").strip())
            except:
                return None

        df['price'] = df['price'].apply(clean_price)
        df = df.dropna(subset=['price'])
        df['rating'] = self.clean_rating(df['rating'])

        # Hapus data dengan rating > 5
        df = df[df['rating'] <= 5]

        # Ekstrak angka pertama dari kolom colors dan ubah ke integer
        df['colors'] = df['colors'].str.extract(r'(\d+)')
        df['colors'] = pd.to_numeric(df['colors'], errors='coerce')

        df['colors'] = df['colors'].fillna(0)

        # Cek tipe data
        print(df.info())

        df['gender'] = df['gender'].str.replace('Gender:', '', regex=False).str.strip()
        df['size'] = df['size'].str.replace('Size:', '', regex=False).str.strip()

        df.dropna(subset=['price', 'rating', 'colors'], inplace=True)
        df.drop_duplicates(inplace=True)

        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return df


