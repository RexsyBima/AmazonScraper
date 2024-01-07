from playwright.sync_api import sync_playwright
from app.Functions import run


class PlayWright:
    def __init__(self, url):
        self.url = url

    def goto(self):
        with sync_playwright() as playwright:
            self.html = run(url=self.url, playwright=playwright)
        return self.html

    def save_html(self):
        with open("output.html", "w", encoding="utf-8") as file:
            file.writelines(self.html)
