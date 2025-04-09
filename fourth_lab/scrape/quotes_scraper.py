from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_quotes():
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    driver.get("http://quotes.toscrape.com/login")

    # --- Log in ---
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("admin")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    time.sleep(1)  # Wait for redirect

    driver.get("http://quotes.toscrape.com/page/1/")
    time.sleep(1)

    quotes = driver.find_elements(By.CLASS_NAME, "quote")
    for q in quotes:
        text = q.find_element(By.CLASS_NAME, "text").text
        author = q.find_element(By.CLASS_NAME, "author").text
        print(f"\n📜 {text}\n👤 {author}")

    driver.quit()

if __name__ == "__main__":
    scrape_quotes()
