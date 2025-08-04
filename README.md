# Earth911 Electronics Recycling Locator Scraper

This Python script uses Selenium to scrape data from [Earth911](https://search.earth911.com/) for electronics recycling locations in a specific ZIP code.

## ✅ Features

- Searches for **"Electronics"** recycling in ZIP code `10001`
- Selects a larger search radius
- Extracts the following information from the first 5 results:
  - Business name
  - Last updated date
  - Street address
  - Materials accepted
- Saves the extracted data to a CSV file: `data.csv`

---

## 📦 Requirements

- Python 3.7+
- Google Chrome browser installed
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (must match your installed Chrome version)
- Selenium

### Install dependencies:

```bash
pip install selenium
