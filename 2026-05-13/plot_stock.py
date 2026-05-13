import yfinance as yf
import matplotlib.pyplot as plt
from __init__ import get_top_30_stocks  # 스크래퍼 임포트

# 그래프 한글 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def draw_chart(name, code):
    print(f"\n[차트 생성] {name}({code}) 데이터를 분석 중...")

    # 코스피(.KS) 시도 후 실패 시 코스닥(.KQ) 시도
    ticker = f"{code}.KS"
    hist = yf.Ticker(ticker).history(period="1mo")
    if hist.empty:
        ticker = f"{code}.KQ"
        hist = yf.Ticker(ticker).history(period="1mo")

    if hist.empty:
        print(" 데이터를 가져올 수 없습니다.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['Close'], marker='o', color='royalblue', linewidth=2)
    plt.title(f"{name} 최근 1개월 주가 추이")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("stock_trend.png")
    print("stock_trend.png' 저장 완료!")
    plt.show()


def main():
    # 1. 데이터 가져오기 (from __init__.py)
    stocks = get_top_30_stocks()

    if not stocks:
        print("데이터를 불러오지 못했습니다.")
        return

    # 2. 목록 보여주기
    print("\n--- 현재 실시간 거래상위 Top 30 ---")
    for i, s in enumerate(stocks, 1):
        print(f"[{i:2d}] {s['name']} ({s['code']})")

    # 3. 사용자 선택 및 그래프 출력
    try:
        choice = int(input("\n분석할 번호 선택: ")) - 1
        if 0 <= choice < len(stocks):
            draw_chart(stocks[choice]['name'], stocks[choice]['code'])
        else:
            print("번호가 범위를 벗어났습니다.")
    except ValueError:
        print("숫자를 입력해 주세요.")


if __name__ == "__main__":
    main()