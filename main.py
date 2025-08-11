import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

BMS_URL = "https://in.bookmyshow.com/movies/chennai/coolie/buytickets/ET00395817/20250814"
DISTRICT_URL = "https://www.district.in/movies/coolie-movie-tickets-in-chennai-MV172677?frmtid=zcw3aqxszc"

last_bms_text = None
last_district_text = None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def check_site(url, last_text, site_name):
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        current_text = soup.get_text()
        if last_text is None:
            return current_text, False
        if current_text != last_text:
            send_telegram_message(f"🎬 New show detected on {site_name}!")
            return current_text, True
        return last_text, False
    except Exception as e:
        print(f"Error checking {site_name}: {e}")
        return last_text, False

def main():
    global last_bms_text, last_district_text
    while True:
        last_bms_text, bms_changed = check_site(BMS_URL, last_bms_text, "BookMyShow")
        last_district_text, district_changed = check_site(DISTRICT_URL, last_district_text, "District.in")
        time.sleep(60)

if __name__ == "__main__":
    main()
