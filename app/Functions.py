import time
from playwright.sync_api import Playwright

from app.Models import Item
from app.Soup import Soup


def run(url, playwright: Playwright):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    # other actions...
    time.sleep(25)
    html = page.inner_html("body")
    with open("output.html", "w", encoding="utf-8") as file:
        file.writelines(html)
    browser.close()
    return html


def create_item(item: Item, soup: Soup, url):
    item.url = url
    item.title = soup.title
    item.price = soup.price
    item.decimal_price = soup.decimal_price
    item.shipping = soup.shipping
    item.category_price = soup.category_price
    item.total_rating = soup.total_rating
    item.rating = soup.rating
    item.features = soup.features
    item.seller = soup.seller
    item.brand = soup.brand
    item.details = soup.details
    item.img_url = soup.img_url
    return item
