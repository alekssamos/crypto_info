"""Parser websites, base class with functions"""
import html
import re


class Base:
    """Base class for all parsers"""

    name = ""

    def get_info(self, convert_numbers=True):
        """Get the currency table from the website

        Args:
            convert_numbers (bool, optional): [description]. Defaults to True.

        Returns:
            tuple: (headers 1d list, content 2d list with rows and cols)
        """

    def strip_tags(self, text):
        """delete html tags from string

        Args:
                text (str): the HTML text

        Returns:
                str: clean text
        """
        res = re.sub("<[^>]+>", "", text).strip()
        return res

    def strToFloat(self, text):
        """convert string to float

        Args:
            text (str): the string

        Returns:
            float: converted string
        """
        if "," in text and "." in text:
            text = text.replace(",", "")

        res = float(re.sub("[^0-9.,+-]", "", text.replace(",", ".")))
        return res

    def strToInt(self, text):
        """convert string to int

        Args:
            text (str): the string

        Returns:
            int: converted string
        """
        res = int(re.sub("[^0-9+-]", "", text))
        return res

    def toStr(self, obj):
        """convert any type to string with (plus) sign

        Args:
            obj (object): the object

        Returns:
            str: converted string
        """
        res = html.unescape(str(obj))
        if "-" not in res and re.match("[\d]", res[0]):
            res = "+" + res
        return res
