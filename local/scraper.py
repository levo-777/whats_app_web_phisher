import os
import time
import cv2
import requests
import logging
from pyzbar import pyzbar
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebScraper:
    def __init__(self, url, static_folder="static"):
        self.url = url
        self.static_folder = static_folder
        self.screenshot_path = os.path.join(static_folder, "screenshot.png")
        self.qr_code_path = os.path.join(static_folder, "qr_code.png")
        options = Options()
        self.browser = webdriver.Firefox(options=options)
        self.browser.get(self.url)
        time.sleep(3)
    
    def refresh(self):
        self.browser.refresh()

    def take_screenshot(self):
        self.browser.save_screenshot(self.screenshot_path)
        logging.info("Screenshot taken.")

    def get_local_storage(self):
        return self.browser.execute_script("return localStorage")

    def is_user_logged_in(self):
        try:
            local_storage = self.get_local_storage()
            return bool(local_storage.get('me-display-name', ''))
        except:
            return False

    def clean_up(self):
        self.browser.quit()

class QRCodeHandler:
    @staticmethod
    def crop_qr_code(image_path, output_path):
        try:
            img = cv2.imread(image_path)
            decoded_objects = pyzbar.decode(img)
            for obj in decoded_objects:
                x, y, w, h = obj.rect
                cropped_img = img[y:y+h, x:x+w]
                cv2.imwrite(output_path, cropped_img)
                logging.info(f"QR code saved as {output_path}")
                return True
        except Exception as e:
            logging.error(f"Error cropping QR code: {e}")
        return False

class Notifier:
    @staticmethod
    def notify(endpoint):
        url = f"http://localhost:5000/{endpoint}"
        try:
            response = requests.post(url)
            if response.status_code == 200:
                logging.info(f"Successfully notified Flask app: {endpoint}")
        except Exception as e:
            logging.error(f"Error notifying Flask app: {e}")

def run_scraper():
    scraper = WebScraper("https://web.whatsapp.com")
    qr_handler = QRCodeHandler()
    try:
        while True:
            if scraper.is_user_logged_in():
                phone_number = "+" + scraper.get_local_storage().get('last-wid-md', '').split(":")[0]
                logging.info(f"User Logged In: {phone_number}")
                Notifier.notify("user_logged_in")
                break
            
            if os.path.exists(scraper.screenshot_path):
                os.remove(scraper.screenshot_path)
            scraper.take_screenshot()
            
            if os.path.exists(scraper.qr_code_path):
                os.remove(scraper.qr_code_path)
            if qr_handler.crop_qr_code(scraper.screenshot_path, scraper.qr_code_path):
                Notifier.notify("qr_code_updated")
            
            time.sleep(15)
    except Exception as e:
        logging.error(f"Error in scraper process: {e}")
    finally:
        scraper.clean_up()

if __name__ == "__main__":
    run_scraper()
