import time
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Test cases for the Gaming Ecommerce application
class GamingEcommerceTests(unittest.TestCase):
    BASE_URL = 'http://34.235.115.176:3000/'
    TIMEOUT = 120  # seconds

    @classmethod
    def setUpClass(cls):
        print('⚙️ Launching Chrome...')
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.wait = WebDriverWait(cls.driver, 20)  # Increased timeout

        print('🚀 Waiting for application to be ready...')
        cls.wait_for_app_ready()
        print('✅ Application is up and running!')

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    @staticmethod
    def is_server_running():
        try:
            response = requests.get(GamingEcommerceTests.BASE_URL, timeout=5)
            return 200 <= response.status_code < 400
        except requests.RequestException:
            return False

    @classmethod
    def wait_for_app_ready(cls, retries=10, delay=5):
        for i in range(retries):
            if not cls.is_server_running():
                print(f'⏳ Server not responding, retrying ({i + 1}/{retries})...')
                time.sleep(delay)
                continue
            try:
                cls.driver.get(cls.BASE_URL)
                cls.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                title = cls.driver.title
                if title:
                    return
            except Exception as e:
                print(f'⏳ App not ready, retrying ({i + 1}/{retries})... {str(e)}')
                time.sleep(delay)
        raise Exception(f'❌ Application not reachable after retries. Ensure the server is running at {cls.BASE_URL}')

    def test_load_home_page(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.assertTrue(self.driver.title)

    def test_load_products_page(self):
        self.driver.get(f'{self.BASE_URL}products')
        self.wait.until(EC.url_contains('/products'))
        self.assertIn('/products', self.driver.current_url)

    def test_navigate_to_login_page(self):
        self.driver.get(f'{self.BASE_URL}login')
        self.wait.until(EC.url_contains('/login'))
        self.assertIn('/login', self.driver.current_url)

    def test_navigate_to_register_page(self):
        self.driver.get(f'{self.BASE_URL}register')
        self.wait.until(EC.url_contains('/register'))
        self.assertIn('/register', self.driver.current_url)

    def test_home_page_title(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.assertNotEqual(self.driver.title, '')

    def test_products_page_title(self):
        self.driver.get(f'{self.BASE_URL}products')
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.assertNotEqual(self.driver.title, '')

    def test_basic_routes_no_errors(self):
        routes = ['', 'products', 'login', 'register']
        for route in routes:
            self.driver.get(f'{self.BASE_URL}{route}')
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            page_source = self.driver.page_source
            self.assertNotIn('Cannot GET', page_source)
            self.assertNotIn('404', page_source)

    def test_application_running_on_server(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.url_contains('34.235.115.176'))
        self.assertIn('34.235.115.176', self.driver.current_url)

    def test_footer_presence_on_home_page(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'footer')))
        footer = self.driver.find_element(By.TAG_NAME, 'footer')
        self.assertTrue(footer.is_displayed(), "Footer is not displayed on the home page.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GamingEcommerceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"\n--- Test Summary ---")
    print(f"Total tests: {result.testsRun}")
    print(f"Passed tests: {passed}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
