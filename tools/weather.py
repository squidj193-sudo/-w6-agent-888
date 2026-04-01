import requests

def get_weather(city: str) -> str:
    """取得指定城市目前的天氣與天氣預報資訊。
    
    Args:
        city: 城市名稱 (例如: "Taipei", "Tokyo", "London")。
        
    Returns:
        字串格式的天氣資訊，包含目前天氣狀態與預測。
    """
    try:
        # 使用 format=j1 來取得詳細的 JSON 資料，適合給 Agent 解析
        # 也可以改用 ?format=3 等純文字簡短格式
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 為了避免 JSON 太大，我們擷取重要資訊組成字串回傳給 Agent
        current = data.get("current_condition", [{}])[0]
        weather_desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        temp_c = current.get("temp_C", "Unknown")
        humidity = current.get("humidity", "Unknown")
        wind_speed_kmph = current.get("windspeedKmph", "Unknown")
        
        result = [
            f"City: {city}",
            f"Current Condition: {weather_desc}",
            f"Temperature: {temp_c}°C",
            f"Humidity: {humidity}%",
            f"Wind Speed: {wind_speed_kmph} km/h",
        ]
        
        # 抓取未來三天的預報簡歷
        weather_forecast = data.get("weather", [])
        if weather_forecast:
            result.append("--- Forecast ---")
            for day in weather_forecast:
                date = day.get("date", "Unknown")
                max_temp = day.get("maxtempC", "Unknown")
                min_temp = day.get("mintempC", "Unknown")
                avg_temp = day.get("avgtempC", "Unknown")
                result.append(f"Date: {date} | Max: {max_temp}°C | Min: {min_temp}°C | Avg: {avg_temp}°C")
                
        return "\n".join(result)
        
    except Exception as e:
        return f"取得 {city} 天氣失敗: {str(e)}"
