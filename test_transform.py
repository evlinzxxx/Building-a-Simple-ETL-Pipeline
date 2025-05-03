import unittest
import pandas as pd
import numbers
from utils.transform import DataTransform

class TestDataTransformerAlternative(unittest.TestCase):

    def setUp(self):
        """Inisialisasi data produk umum untuk digunakan di beberapa test."""
        self.valid_products = [
            {'title': 'Product X', 'price': 'Rp15.000', 'rating': '4.7', 'colors': 'Red', 'size': 'L', 'gender': 'Men'},
            {'title': 'Product Y', 'price': 'Rp27.500', 'rating': '3.8', 'colors': 'Blue', 'size': 'XL', 'gender': 'Women'}
        ]
        self.invalid_products = [
            {'title': 'Rejected Product', 'price': 'RpXYZ', 'rating': '3.0', 'colors': 'Black', 'size': 'M', 'gender': 'Unisex'}
        ]

    def test_valid_transformation(self):
        """Test transformasi produk dengan format harga yang valid."""
        transformer = DataTransform(self.valid_products)
        df = transformer.transform()

        self.assertEqual(df.shape[0], 2, "Seharusnya ada dua baris produk.")

        expected_columns = ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        for column in expected_columns:
            with self.subTest(column=column):
                self.assertIn(column, df.columns)

        with self.subTest("Cek harga numerik positif"):
            self.assertGreater(df['price'].iloc[0], 0)
            self.assertIsInstance(df['price'].iloc[0], numbers.Number)

        with self.subTest("Cek nama produk pertama"):
            self.assertEqual(df['title'].iloc[0], 'Product X')

    def test_invalid_price_filtered(self):
        """Test transformasi dengan data harga tidak valid harus diabaikan."""
        transformer = DataTransform(self.invalid_products)
        df = transformer.transform()

        self.assertTrue(df.empty, "DataFrame harus kosong jika harga tidak valid.")

if __name__ == '__main__':
    unittest.main()
