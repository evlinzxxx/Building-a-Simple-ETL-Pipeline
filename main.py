from colorama import init, Fore, Style
from utils.extract import scrape_main
from utils.transform import DataTransform
from utils.load import DataSaver

# Inisialisasi colorama
init(autoreset=True)

def log_success(message):
    print(f"{Fore.GREEN}{Style.BRIGHT}  {message}{Style.RESET_ALL}")

def log_failure(message):
    print(f"{Fore.RED}{Style.BRIGHT}  {message}{Style.RESET_ALL}")

def log_warning(message):
    print(f"{Fore.YELLOW}{Style.BRIGHT}  {message}{Style.RESET_ALL}")

class WebScraper:
    """Scraper data dari situs fashion."""

    def __init__(self, base_url, max_pages=50):
        self.base_url = base_url
        self.max_pages = max_pages
        self.products = []

    def run_scraping(self):
        for page in range(1, self.max_pages + 1):
            page_suffix = "" if page == 1 else f"page{page}"
            full_url = f"{self.base_url}{page_suffix}"
            label = f"Halaman {page}"
            self._scrape_and_collect(full_url, label)
        return self.products

    def _scrape_and_collect(self, url, label):
        try:
            data = scrape_main(url)
            self.products.extend(data)
            log_success(f"{label:<10}: Berhasil scraping {url}")
        except Exception as err:
            log_failure(f"{label:<10}: Gagal scraping {url} - {err}")

class ProductPipeline:
    """Mengolah data produk yang sudah di-scrape."""

    def __init__(self, raw_products):
        self.raw_products = raw_products

    def run_pipeline(self):
        transformer = DataTransform(self.raw_products)
        return transformer.transform()

def run():
    base_url = "https://fashion-studio.dicoding.dev/"
    scraper = WebScraper(base_url)

    # Step 1: Scrape
    products = scraper.run_scraping()

    if not products:
        log_warning("Tidak ada produk yang ditemukan.")
        return

    # Step 2: Transform
    pipeline = ProductPipeline(products)
    cleaned_data = pipeline.run_pipeline()

    # Step 3: Save
    saver = DataSaver(cleaned_data)
    saver.save_all()

if __name__ == "__main__":
    run()