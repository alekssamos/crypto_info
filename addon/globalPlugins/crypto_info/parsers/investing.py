"""parser module for the ru.investing.com website"""
import re
from urllib.request import urlopen, Request
from .base import Base  # noqa


class Investing(Base):
    """parser for the ru.investing.com website"""

    name = "investing.com"

    flags = re.DOTALL + re.IGNORECASE

    def get_info(self):
        """Get the currency table from the ru.investing.com website

        Returns:
                 tuple: (headers 1d list, content 2d list with rows and cols)
        """
        url = "https://ru.investing.com/crypto/"
        s = (
            urlopen(Request(url, headers={"User-Agent": "Mozilla"}))
            .read()
            .decode("UTF8")
        )
        # with open("page.html", "r", encoding="UTF8") as f: s = f.read()
        table = re.search(
            r"""(<table.*?js-top-crypto-table[^>]+>+.*?</table>)""", s, self.flags
        ).group(1)
        thead = re.search("(<thead.*?>.*?</thead>)", table, self.flags).group(1)
        tbody = re.search("(<tbody.*?>.*?</tbody>)", table, self.flags).group(1)
        thead_trs = []
        table_headers = []
        tbody_trs = re.findall("(<tr[^>]{0,}>.*?</tr>)", tbody, self.flags)
        table_content = []
        thead_trs.append(re.search("(<tr[^>]?>.*?</tr>)", thead, self.flags).group(1))
        table_headers = re.findall("<th[^>]{0,}>(.*?)</th>", thead_trs[0], self.flags)
        table_headers = [self.strip_tags(l) for l in table_headers]
        tbody_tr_tds = []
        for tr in tbody_trs:
            tbody_tr_tds = re.findall("<td[^>]{0,}>(.*?)</td>", tr, self.flags)
            tbody_tr_tds = [self.strip_tags(l) for l in tbody_tr_tds]
            for i in range(3, 9):
                tbody_tr_tds[i] = self.strToFloat(tbody_tr_tds[i])

            table_content.append(tbody_tr_tds)

        return (table_headers, table_content)

if __name__ == "__main__":
    iv = Investing()
    headers, content = iv.get_info()
    allcap = sum([l[4] for l in content])
    print("total of all capitalizations:", allcap)
    print("*" * 50)
    print(headers)
    print("*" * 50)
    print(content)
