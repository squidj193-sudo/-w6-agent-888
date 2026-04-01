"""
attractions_tool.py
-------------------
搜尋目的地熱門景點與旅遊注意事項。
使用 DuckDuckGo Search（無需 API 金鑰）進行網路搜尋。
搜尋關鍵字範例：「Tokyo 景點」、「Taipei 旅遊注意事項」
"""

from ddgs import DDGS


def search_attractions(city: str, max_results: int = 5) -> list[dict]:
    """
    搜尋指定城市的熱門景點。

    Args:
        city:        城市名稱（中英文皆可），例如 "Tokyo"、"台北"
        max_results: 回傳的搜尋結果筆數，預設 5 筆

    Returns:
        list of dict，每筆包含：
            - title  (str): 網頁標題
            - url    (str): 來源網址
            - snippet(str): 摘要文字
    """
    query = f"{city} 景點 推薦"
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title":   r.get("title", ""),
                "url":     r.get("href", ""),
                "snippet": r.get("body", ""),
            })

    return results


def search_travel_tips(city: str, max_results: int = 5) -> list[dict]:
    """
    搜尋指定城市的旅遊注意事項。

    Args:
        city:        城市名稱（中英文皆可），例如 "Tokyo"、"台北"
        max_results: 回傳的搜尋結果筆數，預設 5 筆

    Returns:
        list of dict，每筆包含：
            - title  (str): 網頁標題
            - url    (str): 來源網址
            - snippet(str): 摘要文字
    """
    query = f"{city} travel tips precautions things to know"
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title":   r.get("title", ""),
                "url":     r.get("href", ""),
                "snippet": r.get("body", ""),
            })

    return results


# ── Gemini Function Calling 宣告（供 Agent 使用）────────────────────────────
attractions_tool_declaration = {
    "name": "search_attractions",
    "description": (
        "使用 DuckDuckGo 搜尋指定城市的熱門景點推薦，"
        "回傳景點名稱、網址與簡介摘要。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "目標城市名稱，中英文皆可，例如 Tokyo、台北、Paris。",
            },
            "max_results": {
                "type": "integer",
                "description": "回傳的搜尋結果筆數，預設為 5。",
            },
        },
        "required": ["city"],
    },
}

travel_tips_tool_declaration = {
    "name": "search_travel_tips",
    "description": (
        "使用 DuckDuckGo 搜尋指定城市的旅遊注意事項、禁忌與必知資訊，"
        "回傳相關文章標題、網址與摘要。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "目標城市名稱，中英文皆可，例如 Tokyo、台北、Paris。",
            },
            "max_results": {
                "type": "integer",
                "description": "回傳的搜尋結果筆數，預設為 5。",
            },
        },
        "required": ["city"],
    },
}


# ── 快速測試（直接執行此檔案時啟動）────────────────────────────────────────
if __name__ == "__main__":
    import sys
    import io

    # 強制 stdout 使用 UTF-8，避免 Windows cp950 亂碼
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    city = sys.argv[1] if len(sys.argv) > 1 else "Tokyo"

    print(f"{'='*55}")
    print(f"  城市：{city}")
    print(f"{'='*55}")

    # ── 熱門景點 ────────────────────────────────────────────
    print("\n[景點推薦]\n")
    try:
        attractions = search_attractions(city, max_results=3)
        for i, r in enumerate(attractions, 1):
            print(f"  {i}. {r['title']}")
            print(f"     {r['url']}")
            print(f"     {r['snippet'][:100]}...")
            print()
    except Exception as e:
        print(f"  錯誤：{e}")

    # ── 旅遊注意事項 ─────────────────────────────────────────
    print("\n[旅遊注意事項]\n")
    try:
        tips = search_travel_tips(city, max_results=3)
        for i, r in enumerate(tips, 1):
            print(f"  {i}. {r['title']}")
            print(f"     {r['url']}")
            print(f"     {r['snippet'][:100]}...")
            print()
    except Exception as e:
        print(f"  錯誤：{e}")
