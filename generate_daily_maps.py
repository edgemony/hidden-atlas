#!/usr/bin/env python3
"""
Generate maps for the daily Hidden Atlas game.

This script generates map images for a given date and saves them
in the public/maps/YYYY-MM-DD/ directory for the web frontend.
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

from city_selector import load_cities, get_daily_city
from map_generator import generate_all_levels


def generate_maps_for_date(date, output_dir="public/maps"):
    """Generate maps for a specific date."""
    # Load cities
    cities = load_cities(min_population=250000)

    # Get the city for this date
    city = get_daily_city(cities, date)

    print(f"Generating maps for {date}: {city['name']}, {city['country']}")

    # Create output directory
    date_str = date.strftime("%Y-%m-%d")
    date_dir = Path(output_dir) / date_str
    date_dir.mkdir(parents=True, exist_ok=True)

    # Generate maps
    # Using coordinates directly for better accuracy
    lat, lng = city['lat'], city['lng']

    print(f"  Coordinates: {lat}, {lng}")
    print(f"  Generating 5 map levels...")

    try:
        # Generate all 5 levels at once
        generate_all_levels(
            lat=lat,
            lng=lng,
            output_dir=str(date_dir)
        )

        # Rename files from level_N.png to levelN.png for frontend
        for level in range(1, 6):
            old_name = date_dir / f"level_{level}.png"
            new_name = date_dir / f"level{level}.png"
            if old_name.exists():
                old_name.rename(new_name)
                print(f"    [OK] Level {level}")

        # Create city metadata JSON
        city_data = {
            "name": city['name'],
            "country": city['country'],
            "continent": city.get('continent', 'Unknown'),
            "state": city.get('admin', ''),  # State/province if available
            "latitude": lat,
            "longitude": lng,
            "population": city.get('population', 0)
        }

        city_json_path = date_dir / "city.json"
        with open(city_json_path, 'w', encoding='utf-8') as f:
            json.dump(city_data, f, indent=2, ensure_ascii=False)

        print(f"  [OK] Saved city data to {city_json_path}")
        print(f"  [OK] All maps generated successfully!")

    except Exception as e:
        print(f"\n  [ERROR] Error generating maps: {e}")
        raise


def generate_next_n_days(n=7, output_dir="public/maps"):
    """Generate maps for the next N days."""
    today = datetime.now()

    print(f"Generating maps for the next {n} days...\n")

    for i in range(n):
        date = today + timedelta(days=i)
        generate_maps_for_date(date, output_dir)
        print()  # Blank line between days


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Hidden Atlas maps")
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to generate (default: 7)'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Specific date to generate (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='public/maps',
        help='Output directory (default: public/maps)'
    )

    args = parser.parse_args()

    if args.date:
        # Generate for specific date
        date = datetime.strptime(args.date, "%Y-%m-%d").date()
        generate_maps_for_date(date, args.output)
    else:
        # Generate for next N days
        generate_next_n_days(args.days, args.output)
