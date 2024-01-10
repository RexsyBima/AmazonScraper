from playwright.sync_api import sync_playwright
from app.Functions import run


class PlayWright:
    def goto(self, url):
        with sync_playwright() as playwright:
            self.html, self.browser, self.page = run(url=url, playwright=playwright)
        return self.html

    def save_html(self):
        with open("output.html", "w", encoding="utf-8") as file:
            file.writelines(self.html)

    def close(self):
        self.browser.close()
        self.page.close()
