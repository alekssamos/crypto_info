"""parser module for the ru.investing.com website"""
import re
import json
from urllib.request import urlopen, Request
from .base import Base  # noqa


class Investing(Base):
    """parser for the ru.investing.com website"""

    name = "investing.com"

    def get_info(self, convert_numbers=True):
        """Get the currency table from the ru.investing.com website

        Returns:
                 tuple: (headers 1d list, content 2d list with rows and cols)
        """

        url = "https://ru.investing.com/crypto/Service/LoadCryptoCurrencies"
        data = b"draw=1&columns%5B0%5D%5Bdata%5D=currencies_order&columns%5B0%5D%5Bname%5D=currencies_order&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=function&columns%5B1%5D%5Bname%5D=crypto_id&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=function&columns%5B2%5D%5Bname%5D=name&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=symbol&columns%5B3%5D%5Bname%5D=symbol&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=function&columns%5B4%5D%5Bname%5D=price_usd&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=market_cap_formatted&columns%5B5%5D%5Bname%5D=market_cap_usd&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=24h_volume_formatted&columns%5B6%5D%5Bname%5D=24h_volume_usd&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=total_volume&columns%5B7%5D%5Bname%5D=total_volume&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=change_percent_formatted&columns%5B8%5D%5Bname%5D=change_percent&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=percent_change_7d_formatted&columns%5B9%5D%5Bname%5D=percent_change_7d&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=currencies_order&order%5B0%5D%5Bdir%5D=asc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&currencyId=12"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "https://ru.investing.com/crypto/",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://ru.investing.com"
        }

        opener = Request(url, data = data, headers = headers)
        resp = urlopen(opener)
        content = resp.read().decode("UTF-8")
        j = json.loads(content)
        data_items = j["data"]
        ret_headers = (
            "Name", "Ticker", "Price",
            "Capitalization", "Change percent in 24 h", "Value 24 h",
            "Value", "Change 24 h", "Change 7 d"
        )
        ret_content = []
        tmp_data = []
        for ditem in data_items:
            tmp_data.append(ditem["name"])
            tmp_data.append(ditem["symbol"])
            tmp_data.append(ditem["price_usd"] if convert_numbers else str(ditem["price_usd"])+" $")
            tmp_data.append(float(ditem["market_cap_usd"]) if convert_numbers else ditem["market_cap_usd_formatted"])
            tmp_data.append(float(ditem["24h_volume_usd"]) if convert_numbers else ditem["24h_volume_usd_formatted"])
            tmp_data.append(self.strToFloat(ditem["total_volume"]) if convert_numbers else ditem["total_volume"])
            tmp_data.append(self.strToFloat(ditem["change_percent"]) if convert_numbers else ditem["change_percent"])
            tmp_data.append(self.strToFloat(ditem["percent_change_7d"]) if convert_numbers else ditem["percent_change_7d"])
            ret_content.append(tmp_data)
            tmp_data = []
        return (ret_headers, tuple(ret_content))


if __name__ == "__main__":
    iv = Investing()
    headers, content = iv.get_info()
    allcap = sum([l[4] for l in content])
    print("total of all capitalizations:", allcap)
    print("*" * 50)
    print(headers)
    print("*" * 50)
    print(content)
