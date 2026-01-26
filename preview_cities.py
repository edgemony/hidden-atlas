"""Preview the next N days of cities without generating maps."""

import sys
from datetime import date, timedelta
from city_selector import load_cities, get_daily_city, format_city_name, safe_print

def preview_upcoming_cities(days: int = 7):
    """Show which cities will be featured in the next N days."""
    print(f"Loading cities...")
    cities = load_cities()
    print(f"Loaded {len(cities)} cities\n")

    today = date.today()

    print(f"{'Date':<15} {'City':<30} {'Country':<20} {'Population':>15}")
    print("-" * 85)

    for i in range(days):
        target_date = today + timedelta(days=i)
        city = get_daily_city(cities, target_date)

        date_str = target_date.strftime('%Y-%m-%d')
        day_label = "(Today)" if i == 0 else f"(+{i} days)"

        city_name = city['name']
        country = city['country']
        pop = f"{city['population']:,}"
        continent = city['continent']

        line = f"{date_str} {day_label:<7} {city_name:<30} {country:<20} {pop:>15}"
        safe_print(line)

        # Extra info for today
        if i == 0:
            print(f"  Coordinates: {city['lat']}, {city['lng']}")
            safe_print(f"  Continent: {continent}")

if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    preview_upcoming_cities(days)
