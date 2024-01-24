from playwright.sync_api import sync_playwright
from app.Functions import run


class PlayWright:
    """
    handle the browser operation using playwright. Use chromium

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    def goto(self, url):
        """

        to access the url of a webpage, specifically, to capture the html data

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        with sync_playwright() as playwright:
            self.html, self.browser, self.page = run(url=url, playwright=playwright)
        return self.html

    def save_html(self):
        """

        to save the html output into proper "output.html" file in computer

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        with open("output.html", "w", encoding="utf-8") as file:
            file.writelines(self.html)

    def close(self):
        """
        to close the browser

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        self.browser.close()
        self.page.close()
