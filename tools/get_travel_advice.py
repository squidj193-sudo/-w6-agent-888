import requests

def get_travel_advice() -> str:
    """
    取得一則出發前的人生建議（旅行格言）。
    
    Returns:
        str: 一句隨機的人生建議。
    """
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("slip", {}).get("advice", "請帶著開闊的心胸去旅行！")
    except Exception as e:
        return f"無法取得建議，但請記得：旅行中最美的風景是人（錯誤訊息：{e}）"
