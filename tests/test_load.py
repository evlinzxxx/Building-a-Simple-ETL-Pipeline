import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import DataSaver

class TestDataSaver(unittest.TestCase):

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        # Arrange
        df = pd.DataFrame({
            'title': ['Kaos Polos', 'Jaket Hoodie'],
            'price': [15000, 35000],
            'rating': [4.0, 4.8]
        })
        saver = DataSaver(df)

        # Act
        saver.save_to_csv('dummy_output.csv')

        # Assert
        mock_to_csv.assert_called_once_with('dummy_output.csv', index=False)

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets(self, mock_creds_loader, mock_build):
        # Arrange
        df = pd.DataFrame({
            'title': ['Celana Jeans', 'Kemeja Batik'],
            'price': [50000, 60000],
            'rating': [4.2, 4.7]
        })
        saver = DataSaver(df)

        mock_creds_loader.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Act
        saver.save_to_google_sheets('fake_spreadsheet_id', 'Sheet1!A2')

        # Assert
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

if __name__ == '__main__':
    unittest.main()
