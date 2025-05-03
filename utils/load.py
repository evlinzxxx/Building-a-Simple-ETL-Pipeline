import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import logging

class DataSaver:
    """Kelas untuk menyimpan data ke CSV, Google Sheets, dan PostgreSQL."""

    def __init__(self, data, log=True):
        self.data = data
        self.enable_log = log
        if self.enable_log:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    def _log(self, message, level="info"):
        if self.enable_log:
            getattr(logging, level)(message)

    def is_data_valid(self):
        if self.data is None or self.data.empty:
            self._log("❌ Data kosong. Tidak ada yang akan disimpan.", "warning")
            return False
        return True

    def save_to_csv(self, filename="products.csv"):
        if not self.is_data_valid():
            return
        try:
            self.data.to_csv(filename, index=False)
            self._log(f"✅ Data berhasil disimpan ke file CSV: {filename}")
        except Exception as e:
            self._log(f"❌ Gagal menyimpan ke CSV: {e}", "error")

    def save_to_google_sheets(self, spreadsheet_id, range_name, credentials_file="google-sheets-api.json"):
        if not self.is_data_valid():
            return
        try:
            creds = Credentials.from_service_account_file(credentials_file)
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()

            body = {'values': [self.data.columns.tolist()] + self.data.values.tolist()}  # dengan header
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            self._log(f"✅ Data berhasil disimpan ke Google Sheets (ID: {spreadsheet_id})")
        except Exception as e:
            self._log(f"❌ Gagal menyimpan ke Google Sheets: {e}", "error")

    def save_to_postgresql(self, table_name='products',
                           username='developer', password='supersecretpassword',
                           host='localhost', port='5432', database='productsdb'):
        if not self.is_data_valid():
            return
        try:
            engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
            self.data.to_sql(table_name, engine, if_exists='replace', index=False)
            self._log(f"✅ Data berhasil disimpan ke tabel PostgreSQL: '{table_name}'")
        except Exception as e:
            self._log(f"❌ Gagal menyimpan ke PostgreSQL: {e}", "error")

    def save_all(self,
                 csv_name="products.csv",
                 spreadsheet_id='1kzNLvnIMcF9y96q9-qsRf_o_3XanUtg_fxGgRT5M-Qs',
                 range_name='Sheet1!A1'):
        """Simpan data ke semua tujuan: CSV, PostgreSQL, dan Google Sheets."""
        self.save_to_csv(csv_name)
        self.save_to_postgresql()
        self.save_to_google_sheets(spreadsheet_id, range_name)
