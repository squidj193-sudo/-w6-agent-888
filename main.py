import os
import sys
import io
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 匯入各個工具
from tools.weather import get_weather
from tools.attractions_tool import search_attractions, search_travel_tips
from tools.get_travel_advice import get_travel_advice

# 強制 stdout 使用 UTF-8，避免 Windows cmd 亂碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def load_skill(filepath: str) -> str:
    """讀取 System Prompt 檔案"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def main():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("請在 .env 檔案中設定 GEMINI_API_KEY。")
        return

    print("初始化 Agent 中...")
    # 初始化最新的 google-genai 客戶端
    client = genai.Client(api_key=api_key)

    # 讀取行前簡報 Skill 設定
    skill_prompt = load_skill("skills/trip_briefing.txt")

    # 將所有功能放入 list 供 Gemini 使用
    tools_list = [
        get_weather,
        search_attractions,
        search_travel_tips,
        get_travel_advice
    ]

    city = input("請輸入想去的城市（例如：Tokyo）：")
    if not city.strip():
        print("未輸入城市，程式結束。")
        return

    print("\n正在整合資訊與產出簡報，請稍候...\n")

    try:
        # 發出 API 請求
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=city,
            config=types.GenerateContentConfig(
                system_instruction=skill_prompt,
                tools=tools_list,
                temperature=0.7,
            )
        )
        
        # 輸出 Agent 的結果
        print(response.text)

    except Exception as e:
        print(f"產生簡報時發生錯誤：{e}")

if __name__ == "__main__":
    main()
