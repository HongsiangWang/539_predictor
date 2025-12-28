import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_fantasy5_history(start_year, end_year):
    all_results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for year in range(start_year, end_year - 1, -1):
        print(f"fetching {year} data...")
        url = f"https://www.lottery.net/california/fantasy-5/numbers/{year}"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(
                    f" fail to fetch {year} (error: {response.status_code}),skip")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            year_count = 0

            date_links = soup.find_all('a', href=True)
            for link in date_links:
                if f'/california/fantasy-5/numbers/' in link['href'] and 'prize payout' in link.get('title', ''):

                    date_text = link.get_text(separator=" ", strip=True)

                    parent_row = link.find_parent('tr')
                    if parent_row:
                        ball_tags = parent_row.find_all('li', class_='ball')
                        nums = [b.get_text(strip=True) for b in ball_tags]

                        if len(nums) >= 5:
                            all_results.append([date_text] + nums[:5])
                            year_count += 1

            print(f"{year} fetch sucessful,totally {year_count} numbers。")
            # 稍微停頓，避免被網站阻擋
            time.sleep(1.5)

        except Exception as e:
            print(f"fetch {year} fail: {e}")

    if all_results:
        df = pd.DataFrame(all_results, columns=[
                          "date", "num1", "num2", "num3", "num4", "num5"])
        df = df.drop_duplicates()

        filename = f'data/fantasy5_history.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    else:
        print("fail to fetch any data。")


if __name__ == "__main__":
    scrape_fantasy5_history(2025, 2015)
