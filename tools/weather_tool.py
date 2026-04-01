"""
weather_tool.py
---------------
查詢目的地的即時天氣。
資料來源：https://wttr.in/{city}?format=j1
解析欄位：temp_C、weatherDesc
"""

import requests


def get_weather(city: str) -> dict:
    """
    查詢指定城市的即時天氣。

    Args:
        city: 城市名稱（英文），例如 "Taipei"、"Tokyo"、"Paris"

    Returns:
        包含以下欄位的字典：
            - city        (str)  : 查詢的城市名稱
            - temp_C      (str)  : 當前氣溫（攝氏度）
            - weatherDesc (str)  : 天氣描述（英文）
            - feels_like_C(str)  : 體感溫度（攝氏度）
            - humidity    (str)  : 濕度（%）

    Raises:
        ValueError: 無法解析回應或城市不存在時拋出。
        requests.RequestException: 網路請求失敗時拋出。
    """
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"HTTP 錯誤（城市可能不存在）：{e}") from e
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"網路請求失敗：{e}") from e

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"無法解析 JSON 回應：{e}") from e

    # wttr.in j1 格式：current_condition 是一個 list，取第一筆
    current = data["current_condition"][0]

    temp_C = current.get("temp_C", "N/A")
    feels_like_C = current.get("FeelsLikeC", "N/A")
    humidity = current.get("humidity", "N/A")

    # weatherDesc 也是一個 list of dicts，取第一筆的 value
    weather_desc_list = current.get("weatherDesc", [])
    weather_desc = (
        weather_desc_list[0].get("value", "N/A")
        if weather_desc_list
        else "N/A"
    )

    return {
        "city": city,
        "temp_C": temp_C,
        "weatherDesc": weather_desc,
        "feels_like_C": feels_like_C,
        "humidity": humidity,
    }


# ── Gemini Function Calling 宣告（供 Agent 使用）────────────────────────────
weather_tool_declaration = {
    "name": "get_weather",
    "description": (
        "查詢指定城市的即時天氣，回傳攝氏溫度與天氣描述。"
        "使用 wttr.in 公開服務，無需 API 金鑰。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "目標城市的英文名稱，例如 Taipei、Tokyo、Paris。",
            }
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

    test_city = sys.argv[1] if len(sys.argv) > 1 else "Taipei"
    print(f"查詢城市：{test_city}")
    try:
        result = get_weather(test_city)
        print(f"  [temp]  氣溫      : {result['temp_C']} °C")
        print(f"  [desc]  天氣描述  : {result['weatherDesc']}")
        print(f"  [feel]  體感溫度  : {result['feels_like_C']} °C")
        print(f"  [humi]  濕度      : {result['humidity']} %")
    except Exception as e:
        print(f"錯誤：{e}")
