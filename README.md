🗑️ Midlothian Bin Checker

Automatically checks your bin collection dates from Midlothian Council and sends a Discord notification every Monday morning with your next two upcoming bin collections.

## What it does

- Scrapes the [Midlothian Council bin collection website](https://my.midlothian.gov.uk/service/Bin_Collection_Dates) using Playwright
- Finds your next two upcoming bin collections
- Sends a Discord message via webhook that looks like this:
  
📅 Upcoming bin collections:

🗑️ Grey Bin on Wednesday 08/04/2026

🗑️ Food Bin on Thursday 09/04/2026


## Setup

### 1. Fork this repo
Click the **Fork** button at the top right of this page

### 2. Set your postcode
Edit `bin_checker.py` and change this line at the top:
```python
POSTCODE = "YOUR_POSTCODE_HERE"
```

### 3. Create a Discord webhook
- Open Discord and go to your server
- Click **Edit Channel → Integrations → Webhooks → New Webhook**
- Copy the webhook URL

### 4. Add your webhook as a GitHub Secret
- Go to your forked repo **Settings → Secrets and variables → Actions**
- Click **New repository secret**
- Name it `DISCORD_WEBHOOK`
- Paste your webhook URL as the value

### 5. Enable GitHub Actions
- Go to the **Actions** tab in your forked repo
- Click **I understand my workflows, enable them**

That's it! It will now run every Monday at 8am UTC and send your bin reminder to Discord. You can also trigger it manually from the Actions tab anytime.

## Requirements
- A Midlothian Council postcode
- A Discord server with a webhook

## Running locally
```bash
pip install -r requirements.txt
playwright install chromium
playwright install-deps chromium
export DISCORD_WEBHOOK=your_webhook_url_here
python bin_checker.py
```

## Note
This only works for addresses in the Midlothian Council area in Scotland.
