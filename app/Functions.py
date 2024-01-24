import time
from playwright.sync_api import Playwright
from app.Models import Item
from app.Soup import Soup
from amazoncaptcha import AmazonCaptcha
import pandas as pd

type_data = ["image", "font"]  # stylesheet"


def run(url, playwright: Playwright):
    """
    to running playwright chromium browser, has built in captcha fix/solution
    """

    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_context(record_har_mode="minimal")
    page = page.new_page()
    # page.route("**/*", block_aggressively)
    page.goto(url)
    html = page.inner_html("body")
    soup = Soup(html)
    captcha_url = soup.captcha
    print(captcha_url)
    if captcha_url is not None:  # SOLVING CAPTCHA
        amazon = AmazonCaptcha.fromlink(captcha_url)
        solution = amazon.solve()
        page.get_by_placeholder("Type characters").fill(solution)
        page.get_by_text("Continue shopping").click()
        print(solution)
        time.sleep(5)
    time.sleep(5)
    # page.get_by_text("MORE", exact=True).click()
    html = page.inner_html("body")
    return html, browser, page


def block_aggressively(route):
    if route.request.resource_type in type_data:
        route.abort()
    else:
        route.continue_()


# Captcha solver
# Dapatin gambar/url captcha
# Pakai amazoncaptcha buat dapatin jawabannya
# cari tahu gimana jawaban captcha bisa ditaruh di elemen form
# cari tahu gimana kita bisa ngeklik tombol continue shopping


# Category solver
# https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/search?ingress=2&visitId=3366a0bb-c951-426b-a4c9-5dde279de7bb&ref_=ast_bln&terms=computer
# https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/search?terms=Computer
# bisa pakai f string, bikin list kosakata buatnyari produknya gitu


def create_item(item: Item, soup: Soup, url):
    """
    create the pydantic basemodel of Item

    Keyword arguments:
    argument -- description
    Return: return_description
    """

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


def save_to_xlsx(pd: pd = pd, outputs: list = [], filename: str = "output"):
    """

    save the output of list of dictionary, into a proper output.xlsx file

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    df = pd.DataFrame(outputs)
    df.to_excel(f"{filename}.xlsx")
