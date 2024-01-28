# requests, beautifulsoup4
# dua step utama
# 1. dapetin data HTML nya dulu, pakai PLAYWRIGHT
# 2. scraping dngn beautifulsoup4
# 3. export/simpan data ke xlsx, kemungkinan pakai Panda
# 4. Ke database
# TO FIX captcha???
from app.PlayWright import PlayWright
from app.Soup import Soup
from app.Models import Item, Subcategory, Category
from app.Functions import create_item, save_to_xlsx


def parsing_keywords():
    url = "https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/"  # "https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/search?terms=Computer"  # url = "https://www.amazon.com/HP-Flagship-i5-1155G7-Bluetooth-Accessories/dp/B0CPF2T2FD?pf_rd_r=BA29D1VNXE2765GP16CE&pf_rd_t=Events&pf_rd_i=deals&pf_rd_p=4ec8afa9-2097-4b21-a8c6-defe88813034&pf_rd_s=slot-14&ref=dlx_deals_gd_dcl_tlt_0_5bbcf5a6_dt_sl14_34&th=1"

    html = PW.goto(url)
    PW.save_html()
    soup = Soup(html)
    # soup.parsing()
    keywords = soup.get_keywords
    return keywords
    """
    for url in product_urls[0:2]:
        html = PW.goto(url)
        soup = Soup(html)
        # print(url)
        soup.parsing()
        item = Item()
        created_item = create_item(item, soup, url)
        item_output.append(created_item)

        # print(created_item)
    item_output = [item.dict() for item in item_output]
    save_to_xlsx(outputs=item_output)
    PW.close()  # close browser?
    """


def parsing_products_per_keyword(keywords):
    output = []
    # keywords = [x for x in keywords]
    # print(keywords)
    for keyword in keywords:
        # print(f"accessing : {keyword.__str__}")
        html = PW.get_product_urls(f"{url}search?terms={keyword}")
        soup = Soup(html)
        if soup.get_product_urls is not None:
            output.extend(soup.get_product_urls)
        print(output)


def main2():
    url = "https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/"  # "https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/search?terms=Computer"  # url = "https://www.amazon.com/HP-Flagship-i5-1155G7-Bluetooth-Accessories/dp/B0CPF2T2FD?pf_rd_r=BA29D1VNXE2765GP16CE&pf_rd_t=Events&pf_rd_i=deals&pf_rd_p=4ec8afa9-2097-4b21-a8c6-defe88813034&pf_rd_s=slot-14&ref=dlx_deals_gd_dcl_tlt_0_5bbcf5a6_dt_sl14_34&th=1"
    PW = PlayWright()

    html = PW.goto(url)
    PW.save_html()
    soup = Soup(html)
    # soup.parsing()
    # product_urls = soup.catalogue_urls
    output = soup.get_categories
    # TO ADDRESS error print soup.get_categories
    # for i in output:
    #    i: Category = i
    #    print(i.subcategory.href)
    urls = [i.subcategory.href for i in output if i is not None]
    return urls


def main3(urls):
    PW = PlayWright()
    output = []
    for url in urls:
        html = PW.goto(url)
        PW.save_html()
        soup = Soup(html)
        url_products = soup.get_urls_from_subcategories
        output.extend(url_products)
    return output


# PR benerin xlsx
# masukin ke database
# scraping category
# optimisasi biar nggk overload

# PR improve looping, pngn ngescrape bbrp url sekaligus
# categori
# self.description = self.find("div", id="productDescription").get_text()

# self.items = self.find("dl", id="witb-content-list").get_text()
# self.table = self.find("table", id="productDetails_detailBullets_sections1")
# self.table = self.table.find_all("tr")
# self.id = self.table[0].td.get_text()
# self.rank = self.table[2].td.get_text()
# self.upload_date = self.table[3].td.get_text()


if __name__ == "__main__":
    url = "https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/"  # "https://www.amazon.com/stores/page/5BA42671-3E42-4AEB-B9E4-272F10DD0121/search?terms=Computer"  # url = "https://www.amazon.com/HP-Flagship-i5-1155G7-Bluetooth-Accessories/dp/B0CPF2T2FD?pf_rd_r=BA29D1VNXE2765GP16CE&pf_rd_t=Events&pf_rd_i=deals&pf_rd_p=4ec8afa9-2097-4b21-a8c6-defe88813034&pf_rd_s=slot-14&ref=dlx_deals_gd_dcl_tlt_0_5bbcf5a6_dt_sl14_34&th=1"
    PW = PlayWright()
    keywords = parsing_keywords()
    parsing_products_per_keyword(keywords)
