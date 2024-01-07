# requests, beautifulsoup4
# dua step utama
# 1. dapetin data HTML nya dulu, pakai PLAYWRIGHT
# 2. scraping dngn beautifulsoup4
# 3. export/simpan data ke xlsx, kemungkinan pakai Panda
# 4. Ke database
# TO FIX captcha???
from app.PlayWright import PlayWright
from app.Soup import Soup
from app.Models import Item
from app.Functions import create_item


if __name__ == "__main__":
    url = "https://www.amazon.com/HP-Flagship-i5-1155G7-Bluetooth-Accessories/dp/B0CPF2T2FD?pf_rd_r=BA29D1VNXE2765GP16CE&pf_rd_t=Events&pf_rd_i=deals&pf_rd_p=4ec8afa9-2097-4b21-a8c6-defe88813034&pf_rd_s=slot-14&ref=dlx_deals_gd_dcl_tlt_0_5bbcf5a6_dt_sl14_34&th=1"
    PW = PlayWright(url)

    html = PW.goto()
    PW.save_html()
    soup = Soup(html)
    soup.parsing()
    item = Item()
    created_item = create_item(item, soup, url)

    print(item)

# PR improve looping, pngn ngescrape bbrp url sekaligus
# categori
# self.description = self.find("div", id="productDescription").get_text()

# self.items = self.find("dl", id="witb-content-list").get_text()
# self.table = self.find("table", id="productDetails_detailBullets_sections1")
# self.table = self.table.find_all("tr")
# self.id = self.table[0].td.get_text()
# self.rank = self.table[2].td.get_text()
# self.upload_date = self.table[3].td.get_text()
