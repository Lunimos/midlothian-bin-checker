from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ----------------------------
# CONFIGURATION
# Set your postcode below
# Your Discord webhook should be set as a GitHub Actions secret called DISCORD_WEBHOOK
# ----------------------------
POSTCODE = "YOUR_POSTCODE_HERE"  # e.g. "EH6 5DX"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def get_bin_info():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://my.midlothian.gov.uk/service/Bin_Collection_Dates",
            wait_until="networkidle",
            timeout=30000
        )

        frame = page.wait_for_selector("iframe", timeout=15000)
        form_frame = frame.content_frame()

        form_frame.wait_for_selector('input[name="postcode"]', timeout=15000)
        form_frame.fill('input[name="postcode"]', POSTCODE)
        page.keyboard.press("Enter")

        form_frame.wait_for_selector('select[name="listAddress"] option:nth-child(2)', timeout=10000, state="attached")
        form_frame.select_option('select[name="listAddress"]', index=1)

        form_frame.wait_for_selector('span[data-name="html2"]', timeout=10000)
        html = form_frame.inner_html('span[data-name="html2"]')
        browser.close()
        return html

def find_next_two_bins(html):
    soup = BeautifulSoup(html, "html.parser")
    bins = []

    for h3 in soup.find_all("h3"):
        bin_name = h3.get_text(strip=True)
        td = h3.find_parent("table").find("b")
        if not td:
            continue
        date_str = td.get_text(strip=True)

        if not date_str or "No subscription" in date_str:
            continue

        try:
            parts = date_str.split()
            date = datetime.strptime(parts[-1], "%d/%m/%Y")
            bins.append((bin_name, date_str, date))
        except:
            continue

    if not bins:
        return "Could not find any upcoming bin collections."

    bins.sort(key=lambda x: x[2])
    next_two = bins[:2]

    lines = ["📅 **Upcoming bin collections:**"]
    for bin_name, date_str, _ in next_two:
        lines.append(f"🗑️ **{bin_name}** on **{date_str}**")

    return "\n".join(lines)

def send_to_discord(message):
    requests.post(WEBHOOK, json={"content": message})

if __name__ == "__main__":
    html = get_bin_info()
    message = find_next_two_bins(html)
    print(message)
    send_to_discord(message)
