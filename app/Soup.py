from bs4 import BeautifulSoup
import json
from app.Models import Category

class Soup(BeautifulSoup):
    """
    class Soup, inherits from BeautifulSoup. contains parsing mechanisms
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    def __init__(self, html):
        super().__init__(html, "html.parser")

    def parsing(
        self,
        category: list = [],
        category_price: list = [],
        features: list = [],
        details: dict = {},
    ):
        """
        to parse per item, pretty self explanatory        
        
        """
        self.title = self.find("span", id="productTitle").get_text()
        # self.initial_price = self.find("span", class_="a-text-price").span.get_text()
        # self.discount = self.find(
        #    "span", class_="reinventPriceSavingsPercentageMargin"
        # ).get_text()
        self.price = self.find("span", class_="a-price-whole").get_text().replace(".", " ") if self.find("span", class_="a-price-whole") is not None else "Unavailable/Out Of Stock"
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
        self.seller = self.find("a", id="sellerProfileTriggerId").get_text() if self.find("a", id="sellerProfileTriggerId") is not None else None 
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

    @property
    def captcha(self):
        """
        to get the value of the captha
        """
        captcha = (
            self.find("div", class_="a-section")
            .find("div", class_="a-box")
            .find("div", class_="a-box")
            .find("img")["src"]
        )
        return captcha

    @property
    def catalogue_urls(self, output: list = []):
        """
        
        to get urls catalogue product catalog ex = laptop, computer
        aka main category
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        urls = self.find("ul", class_="ProductGrid__grid__f5oba").find_all(
            "li", class_="ProductGridItem__itemOuter__KUtvv"
        )
        for i in urls:
            url = f"https://amazon.com{i.a["href"]}"
            output.append(url)
        return output

    @property
    def get_categories(self, output : list = []):# -> list:
        """Lost track, to fix = get all subcats at once (so far only last one of subcategory(ies))
        ex = Categories -> Monitor ->Only scrape 'Learn From Home
        """
        categories = self.find("ul", class_ ="Navigation__navList__HrEra").find_all("li", class_="Navigation__hasChildren__jSUsH")
        item = {"category" : None}
        for i in categories:
            ITEM = Category()
            output_category = []
            category = i.find("span", class_="Navigation__linkText__LoQD4").get_text()
            subcats = i.find_all("li", class_="Navigation__navItem__bakjf")
            item["category"] = category
            ITEM.category = category 
            #print(f"category is {category}")
            for cat in subcats[2:]:
                href = f"https://www.amazon.com{cat.find("a")["href"]}"
                cat_name = cat.find("span").get_text()
                #print(cat_name)
                ITEM.subcategory.href = href
                ITEM.subcategory.name = cat_name #.append({"subname" : cat_name, "href" : href})
                output_category.append({"subname" : cat_name, "href" : href})
            output.append(ITEM)
            #print(ITEM.category) #TO BE FIXED DISISI SAYA
            item["subcategory"] = output_category
        return output
    
    @property
    def get_urls_from_subcategories(self):
        """
        get item products after accessing subcategories
        Keyword arguments:
        argument -- description
        Return: return_description
        """   
        output = []
        products_urls = self.find("div", id="ProductGrid-Evg8im6rwo").find_all("li", class_="ProductGridItem__itemOuter__KUtvv")
        for url in products_urls:
            url : BeautifulSoup = url
            href = f"https://www.amazon.com{url.find("a")["href"]}"
            output.append(href)
        return output
