import requests
import json
import os
from datetime import datetime

# API 설정
API_KEY = "AIzaSyCP5RMBXqeACnyyqlI5xu2wPgrbK_eFXGg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"


def call_gemini(prompt):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"에러 발생: {e}"


def create_posting(stock_name, stock_code):
    # 폴더 생성
    today_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"post_{today_str}_{stock_name}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # --- [작업 1] 3편 분량의 시리즈 기획안 작성 (index.md) ---
    print(f" {stock_name} 시리즈 기획안(index.md) 생성 중...")
    plan_prompt = f"종목 '{stock_name}'을 주제로 한 블로그 시리즈 3편을 기획해줘. 제목과 각 편의 핵심 요약만 포함해서 마크다운 형식으로 작성해줘."
    planning_content = call_gemini(plan_prompt)

    with open(os.path.join(folder_name, "index.md"), "w", encoding="utf-8") as f:
        f.write(f"# [시리즈 기획] {stock_name} 분석\n\n" + planning_content)

    # --- [작업 2] 1편 초안 문서 작성 (post1.md) ---
    print(f" 1편 초안(post1.md) 작성 중...")
    post_prompt = f"""
    '{stock_name}({stock_code})' 시리즈의 제 1편 초안을 작성해줘.
    전문적인 분석가 톤으로 작성하고, 중간에 반드시 아래 차트 태그를 넣어줘:
    ![차트](../stock_trend.png)
    """
    post1_content = call_gemini(post_prompt)

    with open(os.path.join(folder_name, "post1.md"), "w", encoding="utf-8") as f:
        f.write(post1_content)

    print(f"완료! {folder_name} 폴더에 index.md와 post1.md가 저장되었습니다.")


if __name__ == "__main__":
    create_posting("삼성전자", "005930")