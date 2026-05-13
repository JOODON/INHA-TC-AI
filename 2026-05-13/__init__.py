import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 스크래핑 파트 ( 주식 데이터 30 개 가지고 오는걸로 함 )
def get_top_30_stocks():
    url = "https://finance.naver.com/sise/sise_quant.naver"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.encoding = 'euc-kr'
        soup = BeautifulSoup(response.text, 'html.parser')

        stock_elements = soup.select('a.tltle')
        stock_list = []

        for i, stock in enumerate(stock_elements[:30], 1):
            name = stock.get_text(strip=True)
            code = stock.get('href').split('code=')[-1]
            stock_list.append({"name": name, "code": code})

        return stock_list
    except Exception as e:
        print(f"스크래핑 에러: {e}")
        return []