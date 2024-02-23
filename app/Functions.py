import time
from tkinter import wantobjects
from playwright.sync_api import Playwright, Browser, Page
from app.Models import Item
from app.Soup import Soup
from amazoncaptcha import AmazonCaptcha
import pandas as pd
from cs50 import SQL
import psutil


type_data = ["image", "font"]  # stylesheet"


def insert_into_db(item: Item, db: SQL) -> None:
    db.execute(
        "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, url STRING, title STRING, price FLOAT, total_rating INTEGER, rating FLOAT, brand STRING, img_url STRING)"
    )
    db.execute(
        "INSERT INTO products (url, title, price, total_rating, rating, brand, img_url) VALUES(?,?,?,?,?,?,?)",
        item.url,
        item.title,
        item.final_price,
        item.total_rating,
        item.rating,
        item.brand,
        item.img_url,
    )


def run(url, browser: Browser, page: Page):
    """
    to running playwright chromium browser, has built in captcha fix/solution
    """
    page.goto(url, timeout=999999, wait_until="load")
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
    wait_ = page.locator(".product-title-word-break")
    wait_.wait_for()
    # page.get_by_text("MORE", exact=True).click()
    html = page.inner_html("body")
    # page.close()
    return html, browser, page


def run_scroll(url, playwright: Playwright):
    """
    to running playwright chromium browser, has built in captcha fix/solution
    """

    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False, args=["--no-sandbox"])
    page = browser.new_context(record_har_mode="minimal")
    page = page.new_page()
    page.route("**/*", block_aggressively)  #
    page.goto(url)
    before_html = page.inner_html("body")
    # page.get_by_text("Show more").click()
    while True:
        # page.mouse.wheel(delta_x=0.0, delta_y=1080.0)
        after_html = page.inner_html("body")
        if before_html == after_html:
            break
        else:
            before_html = after_html
        # page.get_by_text("Show more").click()
        page.keyboard.press("End")
        time.sleep(1)
        page.keyboard.press("Home")
    # page.get_by_text("MORE", exact=True).click()
    html = page.inner_html("body")
    browser.close()
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
    # item.price = soup.price
    # item.decimal_price = soup.decimal_price
    item.final_price = soup.final_price
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


def remove_duplicates(input_list):
    unique_list = []

    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)

    return unique_list


def process_remaining_urls(input_list_db: list, input_list_json: list):
    output = []
    for url in input_list_json:
        if url not in input_list_db:
            output.append(url)
    return output


def kill_process_by_name(process_name):
    # Get a list of all processes
    all_processes = psutil.process_iter(["pid", "name"])

    # Iterate through each process and terminate if the name matches
    for process in all_processes:
        if process.info["name"] == process_name:
            try:
                # Terminate the process
                pid = process.info["pid"]
                psutil.Process(pid).terminate()
                print(f"Terminated {process_name} with PID {pid}")
            except Exception as e:
                print(f"Failed to terminate {process_name}: {e}")
