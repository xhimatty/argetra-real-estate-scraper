import json
from curl_cffi import requests
from bs4 import BeautifulSoup
import re
from lxml import html

def get_urls():
    session = requests.Session()
    listing_urls = []
    for x in range(1, 2):
        url = f"https://www.argetra.com/city/naumburg/s{x}"
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

        response = session.get(url, impersonate='chrome146')
        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)

                items = data if isinstance(data, list) else [data]
                
                for item in items:
                    if item.get("@type") == "ItemList":
                        elements = item.get("itemListElement", [])
                        for element in elements:
                            links = element.get("url")
                            if links:
                                listing_urls.append(links)

            except (json.JSONDecodeError, TypeError):
                continue

    print(f"Total listings URLs: {len(listing_urls)}:\n")

    return listing_urls

url_data = get_urls()

def get_property_data(url_data):
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    property_data = []
    for url in url_data:
        response = session.get(url, impersonate='chrome146')
        html_content = response.text
        tree = html.fromstring(html_content)
        soup = BeautifulSoup(response.text, "html.parser")
        address = soup.find('h1')
        address = address.get_text(strip=True) if address else "N/A"

        price = soup.find('use', {'xlink:href': '#icon-euro'})
        price = price.find_parent('div').get_text(strip=True) if price else "N/A"

        area = soup.find('use', {'xlink:href': '#icon-flaeche'})
        area = area.find_parent('div').get_text(strip=True) if area else "N/A"

        rooms = soup.find('use', {'xlink:href': '#icon-floorplan'})
        if rooms:
            raw_rooms = rooms.find_parent('div').get_text(strip=True)
            match = re.search(r'\d+\s*(?:Rooms?|Zimmer)', raw_rooms, re.IGNORECASE)
            rooms = match.group(0) if match else "N/A"
        else:
            rooms = "N/A"

        balcony = soup.find('use', {'xlink:href': '#icon-balkon'})
        balcony = balcony.find_parent('div').get_text(strip=True) if balcony else "N/A"

        kitchen = soup.find('use', {'xlink:href': '#icon-kueche'})
        kitchen = kitchen.find_parent('div').get_text(strip=True) if kitchen else "N/A"

        bathroom = soup.find('use', {'xlink:href': '#icon-bad'})
        bathroom = bathroom.find_parent('div').get_text(strip=True) if bathroom else "N/A"

        garage = soup.find('use', {'xlink:href': '#icon-garage'})
        garage = garage.find_parent('div').get_text(strip=True) if garage else "N/A"

        basement = soup.find('use', {'xlink:href': '#icon-keller'})
        basement = basement.find_parent('div').get_text(strip=True) if basement else "N/A"

        floor = soup.find('use', {'xlink:href': '#icon-etage'})
        floor = floor.find_parent('div').get_text(strip=True) if floor else "N/A"

        # Locate the Property section block
        property_container = tree.xpath('//p[contains(text(), "Property")]/parent::div')

        if property_container:
            market_value = tree.xpath('//span[contains(text(), "Market value")]/following-sibling::span[1]/text()')
            market_value = market_value[0].strip() if market_value else "N/A"

            minimum_bid = tree.xpath('//span[contains(text(), "Minimum bid")]/following-sibling::span[1]/text()')
            minimum_bid = minimum_bid[0].strip() if minimum_bid else "N/A"

            living_space = tree.xpath('//span[contains(text(), "Living space")]/following-sibling::span[1]/text()')
            living_space = living_space[0].strip() if living_space else "N/A"

            land_area = tree.xpath('//span[contains(text(), "Land area")]/following-sibling::span[1]/text()')
            land_area = land_area[0].strip() if land_area else "N/A"

            year_built = tree.xpath('//span[contains(text(), "Year of construction")]/following-sibling::span[1]/text()')
            year_built = year_built[0].strip() if year_built else "N/A"


        property_data.append(
            {
                'url': url,
                'address': address,
                'price': price,
                'area': area,
                'rooms': rooms,
                'balcony': balcony,
                'kitchen': kitchen,
                'bathroom': bathroom,
                'garage': garage,
                'basement': basement,
                'floor': floor,
                'market_value': market_value,
                'minimum_bid': minimum_bid,
                'living_space': living_space,
                'land_area': land_area,
                'year_built': year_built,
            }
        )
    return property_data


if __name__ == '__main__':
    results = get_property_data(url_data)
    print(results)