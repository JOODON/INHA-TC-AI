import __init__ as scraper
import plot_stock as visualizer
import posting as publisher


def run_automation():
    print("=" * 40)
    print("주식 분석 및 블로그 포스팅 자동화 시작")
    print("=" * 40)

    # 1단계: 실시간 거래상위 종목 스크래핑 (__init__.py)
    print("\n[Step 1] 실시간 거래 상위 종목을 불러오는 중...")
    stocks = scraper.get_top_30_stocks()

    if not stocks:
        print("데이터를 불러오지 못해 종료합니다.")
        return

    print("\n--- 현재 실시간 거래상위 Top 30 ---")
    for i, s in enumerate(stocks, 1):
        print(f"[{i:2d}] {s['name']} ({s['code']})")

    # 2단계: 사용자 종목 선택 및 차트 생성 (plot_stock.py)
    try:
        choice = int(input("\n분석 및 포스팅할 종목 번호를 선택하세요: ")) - 1
        if 0 <= choice < len(stocks):
            selected = stocks[choice]
            name = selected['name']
            code = selected['code']

            print(f"\n[Step 2] {name} 차트 생성 중...")
            visualizer.draw_chart(name, code)

            # 3단계: Gemini API 연동 블로그 포스팅 생성 (posting.py)
            print(f"\n[Step 3] Gemini AI를 이용한 블로그 초안 생성 중...")
            publisher.create_posting(name, code)

            print("\n" + "=" * 40)
            print(f"✨ 모든 작업이 완료되었습니다!")
            print(f" 저장된 차트: stock_trend.png")
            print(f" 블로그 경로: post_YYYY-MM-DD_{name}/index.md")
            print("=" * 40)
        else:
            print("잘못된 번호입니다. 프로그램을 종료합니다.")
    except ValueError:
        print("숫자만 입력 가능합니다.")
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")


if __name__ == "__main__":
    run_automation()