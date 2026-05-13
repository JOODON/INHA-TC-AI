import requests
from bs4 import BeautifulSoup
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

if __name__ == "__main__":
    print("\n--- 🚀 [단독 실행 테스트] 실시간 거래상위 Top 30 ---")
    stocks = get_top_30_stocks()
    if stocks:
        for i, s in enumerate(stocks, 1):
            print(f"[{i:2d}] {s['name']} ({s['code']})")
    else:
        print("데이터를 가져오지 못했습니다.")