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
                    f" fail to fetch {year} (error: {response.status_code}), skip")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            year_count = 0

            # Find all table rows (tr)
            rows = soup.find_all('tr')

            for row in rows:
                # --- 1. Extract date ---
                # Look for <td>, as date is always in td
                td_cell = row.find('td')
                if not td_cell:
                    continue

                # Try to get date from <a>, if no <a>, get directly from <td> text
                date_link = td_cell.find('a')
                if date_link:
                    date_text = date_link.get_text(separator=" ", strip=True)
                else:
                    date_text = td_cell.get_text(separator=" ", strip=True)

                # Filter out non-date headers (e.g., table title "Date")
                if "Date" in date_text or not date_text:
                    continue

                # --- 2. Extract numbers ---
                # Find all <li> with class="ball"
                ball_tags = row.find_all('li', class_='ball')
                nums = [b.get_text(strip=True) for b in ball_tags]

                # Ensure we have at least 5 numbers
                if len(nums) >= 5:
                    all_results.append([date_text] + nums[:5])
                    year_count += 1

            print(f"{year} fetch successful, totally {year_count} numbers.")
            # Slight pause to avoid being blocked by the site
            time.sleep(1.5)

        except Exception as e:
            print(f"fetch {year} fail: {e}")

    if all_results:
        df = pd.DataFrame(all_results, columns=[
                          "date", "num1", "num2", "num3", "num4", "num5"])
        df = df.drop_duplicates()

        filename = 'data/fantasy5_history.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Total fetched: {len(df)} records and saved.")

    else:
        print("Failed to fetch any data.")


if __name__ == "__main__":
    scrape_fantasy5_history(2025, 2015)
