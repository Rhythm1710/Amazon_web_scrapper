from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

product_data = {}


def extract_product_details(product_element):
    try:
        product_title = product_element.find_element(
            By.CSS_SELECTOR, ".a-size-medium.a-color-base.a-text-normal").text
    except Exception as e:
        print("Error extracting product title:", e)
        return

    try:
        product_price_element = product_element.find_element(
            By.CLASS_NAME, "a-price-whole")
        product_price = product_price_element.text
    except Exception as e:
        print("Error extracting product price:", e)
        product_price = 'Price not available'

    try:
        stars_element = product_element.find_element(
            By.CSS_SELECTOR, "i.a-icon-star-small")
        star_class = stars_element.get_attribute("class")
        product_star = star_class.split('a-star-small-')[-1].split(' ')[0]
    except Exception as e:
        print("Error extracting product star rating:", e)
        product_star = 'No stars'

    try:
        product_review = product_element.find_element(
            By.CLASS_NAME, "a-size-base.s-underline-text").text
    except Exception as e:
        print("Error extracting product review:", e)
        product_review = 'No reviews'

    try:
        product_link_element = product_element.find_element(
            By.CLASS_NAME, "a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
        product_link = product_link_element.get_attribute("href")
    except Exception as e:
        print("Error extracting product link:", e)
        product_link = 'No link'

    try:
        image_link_element = product_element.find_element(
            By.CLASS_NAME, "a-section.aok-relative.s-image-fixed-height img")
        product_image_link = image_link_element.get_attribute("src")
    except Exception as e:
        print("Error extracting product image link:", e)
        product_image_link = 'No image link'

    product_data[product_title] = {
        "price": product_price,
        "numberOfRatings": product_review,
        "stars": product_star,
        "product_link": product_link,
        "product_image_link": product_image_link
    }


def click_next_button():
    try:
        next_button = driver.find_element(
            By.CSS_SELECTOR, ".s-pagination-next")
        next_button.click()
        return True
    except Exception as e:
        print("Error clicking next button:", e)
        return False


to_search = input("What do you want to search? ")
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("-detach")
driver = webdriver.Firefox(options=firefox_options)
driver.get("https://www.amazon.in/")
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
search_bar.clear()
search_bar.send_keys(to_search)
search_button = driver.find_element(By.ID, value="nav-search-submit-button")
search_button.click()

while len(product_data) < 100:
    product_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot div.s-asin")))

    for product_element in product_elements:
        extract_product_details(product_element)

        if len(product_data) >= 100:
            break

    if not click_next_button():
        break

json_filename = f"{to_search}.json"
with open(json_filename, "w") as json_file:
    json.dump(product_data, json_file)

print("Data scraped and saved to", json_filename)
driver.quit()
