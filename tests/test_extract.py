import unittest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_main

class TestExtractAlternative(unittest.TestCase):

    def setUp(self):
        self.url = "https://fashion-studio.dicoding.dev/"

    @patch('utils.extract.requests.get')
    def test_scrape_main_success(self, mock_get):
        """Test scrape_main returns correct product data on valid response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Outerwear</h3>
                    <div class="price-container">$45</div>
                    <p>Rating: 3.15 stars</p>
                    <p>Colors: Black, White</p>
                    <p>Size: XL</p>
                    <p>Gender: Female</p>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        result = scrape_main(self.url)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        product = result[0]
        expected_values = {
            'title': 'Outerwear',
            'price': '$45',
            'colors': 'Black',
            'size': 'XL'
        }

        for key, expected in expected_values.items():
            with self.subTest(key=key):
                self.assertIn(expected, product[key])

    @patch('utils.extract.requests.get')
    def test_scrape_main_http_error(self, mock_get):
        """Test scrape_main raises exception on failed HTTP response."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            scrape_main(self.url)

        self.assertIn("404", str(context.exception))

if __name__ == '__main__':
    unittest.main()
