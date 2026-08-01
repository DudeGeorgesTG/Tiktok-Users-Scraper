# 🚀 TikTok User Scraper

> A high-performance, **proxyless** TikTok user scraper built with **Python AsyncIO** and **AIOHTTP**, capable of collecting **up to 1,000 users per second** (depending on hardware and network conditions).

---

## ✨ Features

- ⚡ Up to **1,000 users/sec**
- 🌐 **100% Proxyless** — No proxies required
- 🚀 Fully asynchronous architecture
- 🧵 250 concurrent workers
- 🔍 Automatic user discovery
- 👥 Full profile extraction
- 💾 Saves results instantly to JSON
- 🔄 Continuous scraping
- 🛡️ Duplicate filtering
- 📈 Built for large-scale data collection

---

## 📋 Collected Information

Each user includes:

- Username
- User ID
- SecUID
- Nickname
- Biography
- Follower Count
- Following Count
- Likes Count
- Video Count
- Verified Status
- Private Account Status
- Region
- Profile Picture URL
- Total Favorited
- Collection Timestamp

---

## ⚙️ Performance

| Feature | Value |
|----------|-------|
| Language | Python 3 |
| Networking | AsyncIO + AIOHTTP |
| Workers | 250 |
| Search Threads | 15 |
| Proxies | ❌ Not Required |
| Output | JSON |
| Speed | Up to 1,000 Users/sec* |

> *Performance depends on your hardware, internet connection, and TikTok response times.

---

## 📁 Output

Scraped users are automatically saved to:

```text
scraped.json
```

Each line contains a complete JSON object.

Example:

```json
{
  "username": "example",
  "user_id": "123456789",
  "nickname": "Example User",
  "follower_count": 15234,
  "following_count": 102,
  "video_count": 87,
  "verified": false,
  "region": "US"
}
```

---

## 🚀 Why This Scraper?

Unlike many TikTok scrapers that rely on rotating proxy networks, this project operates **entirely proxyless**, making it:

- Easier to deploy
- Lower operational cost
- Faster setup
- High throughput
- Reliable for large scraping sessions

---

## 📦 Requirements

- Python 3.10+
- aiohttp

Install dependencies:

```bash
pip install aiohttp
```

---

## ▶️ Usage

```bash
python scraper.py
```

Scraped users will automatically be written to `scraped.json`.

---

## 📊 Use Cases

- Creator Discovery
- Data Collection
- Market Research
- Trend Analysis
- Machine Learning Datasets
- Social Media Analytics
- Research Projects

---

## ⭐ Support

If you find this project useful, please consider giving it a **⭐ Star** on GitHub.

---

## ⚠️ Disclaimer

This project is provided for **educational and research purposes only**. Users are solely responsible for ensuring their use complies with TikTok's Terms of Service and all applicable laws and regulations.
