import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# ==================== 替换为你的服务器信息 ====================
SERVER_JSON_PATH = "/www/wwwroot/app.238999.xyz/football_data.json"
# ==================== 抓取配置 ====================
def main():
    # 雪缘园 国内稳定数据源（GitHub Actions 可访问）
    url = "https://www.xyy.com.cn/live/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        matches = []
        # 解析实时直播赛事
        live_matches = soup.find_all("tr", class_="trLive")
        for match in live_matches:
            try:
                home_team = match.find("td", class_="team_l").text.strip()
                away_team = match.find("td", class_="team_r").text.strip()
                score = match.find("td", class_="score").text.strip()
                match_time = match.find("td", class_="time").text.strip()
                status = "进行中" if "直播" in match_time else "未开赛"

                matches.append({
                    "match_time": match_time,
                    "home_team": home_team,
                    "away_team": away_team,
                    "score": score,
                    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": status
                })
            except Exception as e:
                continue

        # 生成 JSON 数据
        result = {
            "data": matches,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(matches)
        }

        # 保存到本地（供 Actions 同步）
        with open("football_data.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"抓取成功！共 {len(matches)} 场比赛")
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        # 生成空数据避免前端报错
        with open("football_data.json", "w", encoding="utf-8") as f:
            json.dump({
                "data": [],
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total": 0
            }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
