"""
City selector for Hidden Atlas.
Handles loading city data, filtering, and daily city selection.
"""

import csv
import random
from datetime import date
from pathlib import Path
from typing import Optional


# Data file path
DATA_DIR = Path(__file__).parent / "data"
CITIES_FILE = DATA_DIR / "cities15000.txt"  # GeoNames format

# Country code to name mapping (common ones)
COUNTRY_CODES = {
    'US': 'United States', 'GB': 'United Kingdom', 'CA': 'Canada',
    'AU': 'Australia', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy',
    'ES': 'Spain', 'BR': 'Brazil', 'MX': 'Mexico', 'JP': 'Japan',
    'CN': 'China', 'IN': 'India', 'RU': 'Russia', 'KR': 'South Korea',
    'NL': 'Netherlands', 'BE': 'Belgium', 'SE': 'Sweden', 'NO': 'Norway',
    'DK': 'Denmark', 'FI': 'Finland', 'PL': 'Poland', 'AT': 'Austria',
    'CH': 'Switzerland', 'PT': 'Portugal', 'IE': 'Ireland', 'NZ': 'New Zealand',
    'ZA': 'South Africa', 'AR': 'Argentina', 'CL': 'Chile', 'CO': 'Colombia',
    'PE': 'Peru', 'VE': 'Venezuela', 'EG': 'Egypt', 'NG': 'Nigeria',
    'KE': 'Kenya', 'TH': 'Thailand', 'VN': 'Vietnam', 'PH': 'Philippines',
    'ID': 'Indonesia', 'MY': 'Malaysia', 'SG': 'Singapore', 'HK': 'Hong Kong',
    'TW': 'Taiwan', 'TR': 'Turkey', 'SA': 'Saudi Arabia', 'AE': 'UAE',
    'IL': 'Israel', 'GR': 'Greece', 'CZ': 'Czech Republic', 'HU': 'Hungary',
    'RO': 'Romania', 'UA': 'Ukraine', 'PK': 'Pakistan', 'BD': 'Bangladesh',
}

# Country code to continent mapping
COUNTRY_TO_CONTINENT = {
    # North America
    'US': 'North America', 'CA': 'North America', 'MX': 'North America',
    'GT': 'North America', 'CU': 'North America', 'HT': 'North America',
    'DO': 'North America', 'HN': 'North America', 'NI': 'North America',
    'SV': 'North America', 'CR': 'North America', 'PA': 'North America',
    'JM': 'North America', 'TT': 'North America', 'PR': 'North America',
    # South America
    'BR': 'South America', 'AR': 'South America', 'CO': 'South America',
    'PE': 'South America', 'VE': 'South America', 'CL': 'South America',
    'EC': 'South America', 'BO': 'South America', 'PY': 'South America',
    'UY': 'South America', 'GY': 'South America', 'SR': 'South America',
    # Europe
    'GB': 'Europe', 'DE': 'Europe', 'FR': 'Europe', 'IT': 'Europe',
    'ES': 'Europe', 'NL': 'Europe', 'BE': 'Europe', 'SE': 'Europe',
    'NO': 'Europe', 'DK': 'Europe', 'FI': 'Europe', 'PL': 'Europe',
    'AT': 'Europe', 'CH': 'Europe', 'PT': 'Europe', 'IE': 'Europe',
    'GR': 'Europe', 'CZ': 'Europe', 'HU': 'Europe', 'RO': 'Europe',
    'UA': 'Europe', 'BY': 'Europe', 'RS': 'Europe', 'HR': 'Europe',
    'BG': 'Europe', 'SK': 'Europe', 'SI': 'Europe', 'LT': 'Europe',
    'LV': 'Europe', 'EE': 'Europe', 'MD': 'Europe', 'BA': 'Europe',
    'AL': 'Europe', 'MK': 'Europe', 'ME': 'Europe', 'XK': 'Europe',
    'LU': 'Europe', 'MT': 'Europe', 'IS': 'Europe', 'CY': 'Europe',
    # Asia
    'CN': 'Asia', 'JP': 'Asia', 'IN': 'Asia', 'KR': 'Asia',
    'ID': 'Asia', 'PK': 'Asia', 'BD': 'Asia', 'VN': 'Asia',
    'TH': 'Asia', 'MY': 'Asia', 'PH': 'Asia', 'SG': 'Asia',
    'MM': 'Asia', 'KH': 'Asia', 'LA': 'Asia', 'NP': 'Asia',
    'LK': 'Asia', 'KZ': 'Asia', 'UZ': 'Asia', 'TM': 'Asia',
    'KG': 'Asia', 'TJ': 'Asia', 'AF': 'Asia', 'MN': 'Asia',
    'HK': 'Asia', 'TW': 'Asia', 'KP': 'Asia',
    # Middle East (as Asia)
    'TR': 'Asia', 'SA': 'Asia', 'AE': 'Asia', 'IL': 'Asia',
    'IR': 'Asia', 'IQ': 'Asia', 'SY': 'Asia', 'JO': 'Asia',
    'LB': 'Asia', 'KW': 'Asia', 'QA': 'Asia', 'BH': 'Asia',
    'OM': 'Asia', 'YE': 'Asia', 'AZ': 'Asia', 'GE': 'Asia',
    'AM': 'Asia',
    # Africa
    'EG': 'Africa', 'NG': 'Africa', 'ZA': 'Africa', 'KE': 'Africa',
    'ET': 'Africa', 'TZ': 'Africa', 'UG': 'Africa', 'DZ': 'Africa',
    'SD': 'Africa', 'MA': 'Africa', 'AO': 'Africa', 'GH': 'Africa',
    'MZ': 'Africa', 'CI': 'Africa', 'CM': 'Africa', 'NE': 'Africa',
    'BF': 'Africa', 'ML': 'Africa', 'MW': 'Africa', 'ZM': 'Africa',
    'SN': 'Africa', 'ZW': 'Africa', 'RW': 'Africa', 'TN': 'Africa',
    'SO': 'Africa', 'TD': 'Africa', 'GN': 'Africa', 'SS': 'Africa',
    'LY': 'Africa', 'CG': 'Africa', 'CD': 'Africa', 'MG': 'Africa',
    'MU': 'Africa', 'BW': 'Africa', 'NA': 'Africa', 'GA': 'Africa',
    # Oceania
    'AU': 'Oceania', 'NZ': 'Oceania', 'PG': 'Oceania', 'FJ': 'Oceania',
    # Russia spans both but commonly grouped with Europe/Asia
    'RU': 'Europe',
}


def get_continent(country_code: str) -> str:
    """Get continent name from ISO2 country code."""
    return COUNTRY_TO_CONTINENT.get(country_code, 'Unknown')


def load_cities(min_population: int = 250000) -> list[dict]:
    """
    Load cities from GeoNames cities15000.txt and filter by country/population.

    Custom filtering:
    - US cities: population >= 100,000
    - UK cities: population >= 250,000

    GeoNames format (tab-separated):
    0: geonameid, 1: name, 2: asciiname, 3: alternatenames, 4: latitude,
    5: longitude, 6: feature class, 7: feature code, 8: country code,
    9: cc2, 10: admin1 code, 11-13: admin codes, 14: population, ...

    Returns list of city dicts with: name, country, lat, lng, population
    """
    if not CITIES_FILE.exists():
        raise FileNotFoundError(
            f"Cities data file not found: {CITIES_FILE}\n"
            "Download from: https://download.geonames.org/export/dump/cities15000.zip\n"
            "Extract cities15000.txt to the data/ folder."
        )

    cities = []
    with open(CITIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                fields = line.strip().split('\t')
                if len(fields) < 15:
                    continue

                pop = int(fields[14])
                country_code = fields[8]

                # Custom filtering by country
                include = False
                if country_code == 'US' and pop >= 100000:
                    include = True
                elif country_code == 'GB' and pop >= 250000:
                    include = True

                if include:
                    cities.append({
                        'name': fields[1],
                        'name_ascii': fields[2],
                        'country': COUNTRY_CODES.get(country_code, country_code),
                        'iso2': country_code,
                        'continent': get_continent(country_code),
                        'lat': float(fields[4]),
                        'lng': float(fields[5]),
                        'population': pop,
                        'admin': fields[10],  # Admin1 code (state/province code)
                        'timezone': fields[17] if len(fields) > 17 else '',
                    })
            except (ValueError, IndexError):
                continue  # Skip malformed rows

    return cities


def get_daily_city(cities: list[dict], target_date: Optional[date] = None) -> dict:
    """
    Get the city for a specific date. Same date = same city for everyone.

    Uses date as seed for deterministic random selection.
    """
    if target_date is None:
        target_date = date.today()

    # Create seed from date (days since epoch)
    seed = (target_date - date(2024, 1, 1)).days

    # Use seeded random to pick city
    rng = random.Random(seed)
    return rng.choice(cities)


def get_random_city(cities: list[dict]) -> dict:
    """Get a random city (for testing/practice mode)."""
    return random.choice(cities)


def format_city_name(city: dict, include_country: bool = True) -> str:
    """Format city name for display: 'City, State/Province, Country' or 'City, Country'."""
    parts = [city['name']]
    if city.get('admin'):
        parts.append(city['admin'])
    if include_country:
        parts.append(city['country'])
    return ', '.join(parts)


def safe_print(text: str) -> None:
    """Print with fallback for encoding issues on Windows."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))


def get_osm_query(city: dict) -> str:
    """Get the OSM query string for a city (for use with map_generator)."""
    # For US cities, include state for disambiguation
    if city['iso2'] == 'US' and city.get('admin'):
        return f"{city['name']}, {city['admin']}, USA"
    return f"{city['name']}, {city['country']}"


# Quick test
if __name__ == "__main__":
    print("Loading cities...")
    try:
        cities = load_cities()  # Default 250K
        print(f"Loaded {len(cities)} cities with population > 250,000")

        # Show today's city
        today_city = get_daily_city(cities)
        safe_print(f"\nToday's city: {format_city_name(today_city)}")
        print(f"  Population: {today_city['population']:,}")
        print(f"  Coordinates: {today_city['lat']}, {today_city['lng']}")
        safe_print(f"  OSM query: {get_osm_query(today_city)}")

        # Show a few random cities
        print("\nSample random cities:")
        for _ in range(5):
            city = get_random_city(cities)
            safe_print(f"  - {format_city_name(city)} (pop: {city['population']:,})")

    except FileNotFoundError as e:
        print(e)
