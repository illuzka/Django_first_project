import requests
from bs4 import BeautifulSoup

class MainTable:
    """
    :param
    :return:
    """
    url = 'https://coincodex.com/market-overview/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    def gainers_losers(self):
        if self.soup.findAll('text')[1].text[-1] and self.soup.findAll('text')[0].text[-1] == '%':
            losers_percent = (self.soup.findAll('text')[1].text)
            gainers_percent = (self.soup.findAll('text')[0].text)
        else:
            losers_percent = None
            gainers_percent = None

        return gainers_percent, losers_percent

    def dom_vol_marcap(self):
        btc_dominance, total_volume, total_mar_cap = 0, 0, 0

        for i, j in enumerate(self.soup.findAll('span')):
            if j.text == 'BTC Dominance':
                btc_dominance = self.soup.findAll('span')[i+3].text
            elif j.text == 'Total Volume':
                total_volume = self.soup.findAll('span')[i+3].text
            elif j.text == 'Total Market Cap':
                total_mar_cap = self.soup.findAll('span')[i+3].text

        try:
            if btc_dominance[-1] == '%' and total_volume[-1] == 'B' and total_mar_cap[-1] == 'B':
                return btc_dominance, total_volume, total_mar_cap
        except TypeError:
            return None


