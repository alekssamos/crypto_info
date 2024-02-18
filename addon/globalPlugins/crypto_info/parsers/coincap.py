"""parser module for the coincap API"""
import json
from urllib.request import urlopen, Request
from .base import Base  # noqa


class Coincap(Base):
    """parser module for the coincap API"""

    name = "coincap"

    @staticmethod
    def format_float(f, i=3):
        return float(("%."+str(i)+"f") % float(f))

    def get_info(self, convert_numbers=True):
        """Get the currency table from the api.coincap.io/v2/assets

        Returns:
                 tuple: (headers 1d list, content 2d list with rows and cols)
        """

        url = "https://api.coincap.io/v2/assets"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "X-Requested-With": "XMLHttpRequest",
        }

        opener = Request(url, headers = headers)
        resp = urlopen(opener)        
        content = resp.read().decode("UTF-8")
        j = json.loads(content)
        data_items = j["data"]
        ret_headers = (
            "Name",
            "Ticker",
            "Price",
            "Capitalization",
            "Change percent in 24 h",
            "Value 24 h",
            "Value",
            "Change 24 h",
            "Change 7 d",
        )
        # attention, I have not found any changes in this API in seven days
        ret_content = []
        tmp_data = []
        for ditem in data_items:
            tmp_data.append(ditem["name"])
            tmp_data.append(ditem["symbol"])
            priceUsd = self.format_float(ditem["priceUsd"])
            tmp_data.append(priceUsd if convert_numbers else str(priceUsd) + " $")
            tmp_data.append(
                self.format_float(ditem["marketCapUsd"], 1)
                if convert_numbers
                else str(self.format_float(ditem["marketCapUsd"], 1)) + " $"
            )
            tmp_data.append(
                self.format_float(ditem["volumeUsd24Hr"])
                if convert_numbers
                else str(self.format_float(ditem["volumeUsd24Hr"])) + " $"
            )
            tmp_data.append(
                self.format_float(ditem["supply"])
                if convert_numbers
                else str(self.format_float(ditem["supply"]))
            )
            tmp_data.append(
                self.format_float(ditem["changePercent24Hr"], 2)
                if convert_numbers
                else str(self.format_float(ditem["changePercent24Hr"], 2)) + "%"
            )
            tmp_data.append(0.0 if convert_numbers else "0.0")
            ret_content.append(tmp_data)
            tmp_data = []
        return (ret_headers, tuple(ret_content))


if __name__ == "__main__":
    cc = Coincap()
    headers, content = cc.get_info()
    print("*" * 50)
    print(headers)
    print("*" * 50)
    print(content)
