from bs4 import BeautifulSoup


class Soup(BeautifulSoup):
    def __init__(self, html):
        super().__init__(html, "html.parser")

    def parsing(
        self,
        category: list = [],
        category_price: list = [],
        features: list = [],
        details: dict = {},
    ):
        self.title = self.find("span", id="productTitle").get_text()
        # self.initial_price = self.find("span", class_="a-text-price").span.get_text()
        # self.discount = self.find(
        #    "span", class_="reinventPriceSavingsPercentageMargin"
        # ).get_text()
        self.price = (
            self.find("span", class_="a-price-whole").get_text().replace(".", " ")
        )
        self.decimal_price = self.find("span", class_="a-price-fraction").get_text()
        self.shipping = self.find("span", class_="a-color-secondary").get_text()
        self.category_price = self.findAll("span", class_="twisterSwatchPrice")
        self.category = self.findAll("span", class_="swatch-title-text-display")
        for i in self.category:
            category.append(i.get_text())
        self.category = (
            category  # [i for i in category if i != ""] -> solve empty string
        )
        for i in self.category_price:
            category_price.append(i.get_text())
        self.total_rating = self.find("span", id="acrCustomerReviewText").get_text()
        self.rating = self.find("span", id="acrPopover").a.span.get_text()
        self.features = self.find("div", id="feature-bullets").find_all(
            "li", class_="a-spacing-mini"
        )

        for i in self.features:
            features.append(i.get_text())
        self.features = features
        self.seller = self.find("a", id="sellerProfileTriggerId").get_text()
        self.brand = self.find("a", id="bylineInfo").get_text()
        self.details = self.find("div", id="poExpander")
        self.details_product = self.details.find_all("tr", class_="a-spacing-small")
        for i in self.details_product:
            details[i.find("td", class_="a-span3").get_text()] = i.find(
                "td", class_="a-span9"
            ).get_text()
        self.details = details
        self.img_url = self.find("div", id="main-image-container").find(
            "img", class_="a-dynamic-image"
        )["src"]
