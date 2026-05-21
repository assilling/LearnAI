from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 创建 FastMCP 实例
mcp = FastMCP("Weather")

# Open-Meteo API 基础 URL
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"


@mcp.tool()
async def get_forecast(
    latitude: float,
    longitude: float,
    hourly: str = "temperature_2m,weather_code",
    daily: str = "temperature_2m_max,temperature_2m_min,weather_code",
    current: str = "temperature_2m,weather_code",
    timezone: str = "auto",
    forecast_days: int = 7,
    temperature_unit: str = "celsius",
) -> dict[str, Any]:
    """
    获取指定位置的天气预报数据。

    基于 Open-Meteo API (https://open-meteo.com/en/docs)，无需 API key。

    Args:
        latitude: 纬度，范围 -90 到 90 (WGS84 坐标)
        longitude: 经度，范围 -180 到 180 (WGS84 坐标)
        hourly: 每小时天气变量，逗号分隔。常用值:
            - temperature_2m: 2米高度温度
            - relative_humidity_2m: 相对湿度
            - precipitation: 降水量
            - weather_code: 天气代码 (WMO)
            - wind_speed_10m: 10米高度风速
        daily: 每日天气变量聚合，逗号分隔。常用值:
            - temperature_2m_max: 最高温度
            - temperature_2m_min: 最低温度
            - precipitation_sum: 日降水量
            - weather_code: 天气代码
            - sunrise/sunset: 日出日落时间
        current: 当前天气条件变量，逗号分隔
        timezone: 时区，默认为 'auto' (自动检测当地时区)，也可指定如 'Asia/Shanghai'
        forecast_days: 预报天数，0-16天，默认为7天
        temperature_unit: 温度单位，'celsius'(摄氏) 或 'fahrenheit'(华氏)

    Returns:
        包含以下键的字典:
        - latitude, longitude: 位置坐标
        - timezone: 时区
        - hourly: 每小时数据 (包含 time 数组和各项天气变量)
        - daily: 每日数据 (包含 date 数组和各项天气变量)
        - current: 当前天气数据

    Example:
        获取北京7天预报:
        get_forecast(latitude=39.9, longitude=116.4, timezone="Asia/Shanghai")
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly,
        "daily": daily,
        "current": current,
        "timezone": timezone,
        "forecast_days": forecast_days,
        "temperature_unit": temperature_unit,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OPEN_METEO_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
