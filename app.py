from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import time

app = Flask(__name__)
BASE_URL = "https://pendujatt.com.se"

def get_mp3_link(song_name):
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # Replit Chromium
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Open search page
        query = song_name.replace(" ", "+")
        search_url = f"{BASE_URL}/search.php?q={query}"
        driver.get(search_url)
        time.sleep(3)  # wait for JS to load results

        # Find first song link
        first_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/song/']")
        song_page_url = first_link.get_attribute("href")

        # Go to song page
        driver.get(song_page_url)
        time.sleep(3)  # wait for download links to appear

        # Find all MP3 links
        mp3_links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.mp3']")

        if len(mp3_links) < 2:
            return None

        # Pick the second download button (index 1)
        second_mp3_link = mp3_links[1].get_attribute("href")
        second_mp3_link = urljoin(song_page_url, second_mp3_link)
        return second_mp3_link

    except Exception as e:
        print("❌ Error:", e)
        return None
    finally:
        driver.quit()

@app.route("/get_link", methods=["GET"])
def get_link():
    song_name = request.args.get("song_name")
    if not song_name:
        return jsonify({"error": "Please provide song_name parameter"}), 400

    link = get_mp3_link(song_name)
    if not link:
        return jsonify({"error": "MP3 link not found"}), 404

    return jsonify({"song_name": song_name, "mp3_link": link})

@app.route("/")
def home():
    return "🎵 Pendujatt MP3 API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

