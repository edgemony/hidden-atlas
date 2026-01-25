# Citydle

A daily geography guessing game where players identify a city from progressively revealing map clues.

## Concept

Each day, a new city is featured. Players have 5 attempts to guess the city:

1. **Level 1**: Water bodies + major highways only (abstract)
2. **Level 2**: Add full street grid
3. **Level 3**: Add parks (green areas)
4. **Level 4**: Add buildings (subset) + highlight top 3 major roads in coral
5. **Level 5**: Full buildings + labeled major roads on the map

The challenge is to identify the city with as few tries as possible.

## Core Components

### Map Generation (`map_generator.py`)
- Generate styled maps at 5 different detail levels
- Supports direct lat/lng coordinates (preferred) or city name geocoding
- Dark theme: navy background (#1a1a2e), cyan water (#4a90a4), coral highlights (#ff6b6b)
- Fetches: water, waterways, streets, buildings, parks, major roads from OSM
- Top 3 major roads by length are highlighted and labeled
- Prefers actual street names over highway refs (e.g., "Downtown Connector" instead of "I-75")
- Uses adjustText library to prevent label overlaps on Level 5
- Uses OSMnx 1.x API (`geometries_from_point`, `graph_from_point`)

### City Selection (`city_selector.py`)
- Uses GeoNames cities15000 dataset (~2,300 cities with pop > 250K)
- `load_cities(min_population=250000)` - loads and filters city data
- `get_daily_city(cities, date)` - deterministic selection based on date (same city for everyone)
- City dict includes: name, country, continent, lat, lng, population, admin (state code)
- `COUNTRY_TO_CONTINENT` mapping for ~70 countries to their continents
- `get_continent(country_code)` - returns continent name from ISO2 code
- Data file: `data/cities15000.txt` (downloaded from GeoNames)

### Bonus Round (`game.js`)
After completing the main game (win or lose), players can guess the city's population:
- Input accepts flexible formats: `500000`, `500,000`, `500k`, `1.5m`
- Accuracy thresholds determine feedback:
  - **Excellent** (cyan): within 10% of actual
  - **Good** (light cyan): within 25%
  - **Close** (light coral): within 50%
  - **Far** (dark coral): more than 50% off
- Shows actual population and whether guess was high/low
- Result included in share text with emoji indicator
- State persists to localStorage

### Hints System (`game.js`)
Progressive hints revealed after wrong guesses:
- **Hint 1** (after 2nd wrong guess, Level 3+): Shows continent
- **Hint 2** (after 4th wrong guess, Level 5): Shows country
- Hints display in a separate row below map (Hint 1 left, Hint 2 right)
- Map maintains full size regardless of hint visibility
- Large, easy-to-read font sizes (1.2em for labels)
- Hints persist across page refreshes via game state
- Responsive: stacks vertically on mobile

### Web Hosting
- Simple web frontend to display the game
- Track user's current attempt
- Reveal next map level on incorrect guess

### Utilities
- Supporting tools as needed

## Tech Stack
- Python backend
- Map data source: OpenStreetMap (via OSMnx 1.x) - designed to be swappable later
- OSMnx for fetching/rendering map data with fine-grained control over features

## Current Status
### Done
- [x] Map generation prototype with 5 detail levels
- [x] Water bodies, streets, parks, buildings rendering
- [x] Major road highlighting (top 3 by length)
- [x] Road labels on map with rotation
- [x] Label overlap prevention (adjustText library)
- [x] City selection with GeoNames dataset (~2,300 cities at 250K+ pop)
- [x] Daily rotation logic (deterministic based on date)
- [x] Direct coordinate lookup (more accurate than name geocoding)
- [x] Prefer street names over highway refs for better game clues
- [x] Bonus round - population guessing with accuracy feedback
- [x] Hints system - continent (Level 3) and country (Level 5) hints in separate row layout
- [x] Hints layout optimization - separate row preserves map size, larger fonts
- [x] Continent mapping for all countries in dataset
- [x] Finish Web frontend - most already complete

### TODO
- [ ] Clean up combined road names (e.g., "I 77;US 21" → "I-77")

## Development Notes
- Python venv is in `.venv` folder
- Run map generation: `python map_generator.py` (uses Portland, OR by default)
- Generate daily maps: `python generate_daily_maps.py --date 2026-01-25` (specific date)
- Generate next 7 days: `python generate_daily_maps.py --days 7`
- Test city selector: `python city_selector.py`
- Maps output to: `public/maps/YYYY-MM-DD/` with `level1-5.png` and `city.json`
