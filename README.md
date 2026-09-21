# Argetra Real Estate Scraper

A web scraper designed to extract real estate and foreclosure property listings from Argetra.com. It handles TLS fingerprinting using curl_cffi to bypass anti-bot protections, pulls structured JSON-LD schema data from search pages, and uses a combination of BeautifulSoup and XPath to parse deeply nested property features.

The scraper targets property listings in Naumburg and processes multiple listing pages before extracting structured data from each property detail page.


## Features
- Anti-Bot Bypass: Utilizes TLS/JA3 impersonation via curl_cffi to mimic realistic browser browser TLS signatures (chrome146).

- Hybrid Extraction Method: Combines JSON-LD structured data parsing for quick link discovery, standard CSS/icon sibling traversal via BeautifulSoup, and precise DOM querying using XPath for secondary property details.

- Strong Data Parsing: Employs regex pattern matching on icon tags to extract key metrics (e.g., room counts) regardless of shifting whitespace or German formatting variations (Zimmer / Rooms).


## Supported Categories

While the scraper is configured by default for Naumburg properties (`/city/naumburg/`), the scraper's pagination logic and extraction patterns accept any city or category directory structure on Argetra (e.g., changing `/city/naumburg/s1` to `/city/berlin/s1` or other category endpoints).

## Use Cases

The extracted datase can support:

- Real estate market research
- Property valuation analysis
- Auction and minimum-bid research
- Property inventory collection
- Comparative property analysis
- Real estate data aggregation


## Data Extracted

| Field          | Description            |
| -------------- | ---------------------- |
| `url`          | Property listing URL   |
| `address`      | Property title/address |
| `price`        | Listed property price  |
| `area`         | Property area          |
| `rooms`        | Number of rooms        |
| `balcony`      | Balcony availability   |
| `kitchen`      | Kitchen availability   |
| `bathroom`     | Bathroom availability  |
| `garage`       | Garage availability    |
| `basement`     | Basement availability  |
| `floor`        | Property floor         |
| `market_value` | Market valuation       |
| `minimum_bid`  | Minimum bid amount     |
| `living_space` | Living space           |
| `land_area`    | Land area              |
| `year_built`   | Year of construction   |


## Tech Stack
    Python
    curl_cffi
    BeautifulSoup
    lxml
    RegEx
    JSON-LD
    XPath


## Requirements
Install the dependencies:

```Bash
pip install curl-cffi beautifulsoup4 lxml
```

## Output

```json
{
    "url": "https://www.argetra.com/search/etagenwohnung-in-06618-naumburg", 
    "address": "Etagenwohnung in 06618 Naumburg", 
    "price": "€104,000", 
    "area": "59 m²", 
    "rooms": "2 Rooms", 
    "balcony": "Balcony", 
    "kitchen": "Kitchen", 
    "bathroom": "Bathroom", 
    "garage": "Garage", 
    "basement": "Basement", 
    "floor": "1. Floor", 
    "market_value": "€104,000.00", 
    "minimum_bid": "€52,000.00", 
    "living_space": "59 m²", 
    "land_area": "5,796 m²", 
    "year_built": "1981"
}
```
