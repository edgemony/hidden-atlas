# Citydle

**A daily geography guessing game.** Identify cities from progressively revealing map clues in 5 attempts or less!

<!-- Once deployed, add:
**[Play Now →](https://your-url.com)**
-->

## About

Each day features a new city from around the world. Start with an abstract view of water and highways, then reveal more details with each guess until the full labeled map appears.

### How to Play

You have 5 attempts to guess the city. Each wrong guess reveals more detail:

1. **Level 1** - Water bodies + major highways (abstract)
2. **Level 2** - Full street grid
3. **Level 3** - Parks and green spaces
4. **Level 4** - Buildings + highlighted major roads
5. **Level 5** - Complete map with labeled streets

### Features

- 🌍 **Daily Challenge** - New city every day at midnight UTC
- 📊 **Population Bonus Round** - Guess the city's population after completing the game
- 💡 **Progressive Hints** - Continent hint at Level 3, country hint at Level 5
- 📱 **Mobile Friendly** - Responsive design works on any device
- 🎨 **Clean Dark Theme** - Easy on the eyes with navy, cyan, and coral colors
- 💾 **Game State Saves** - Your progress persists if you refresh the page
- 📤 **Share Results** - Share your score without spoiling the answer!

---

## For Developers

### Quick Start

Want to run Citydle locally, contribute, or fork it for your own version?

#### Prerequisites
- Python 3.9+
- pip

#### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/citydle.git
cd citydle
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Generate maps for the next 7 days:
```bash
python generate_daily_maps.py --days 7
```

4. Open `public/index.html` in your browser, or serve it with:
```bash
python -m http.server --directory public 8000
```

Then visit http://localhost:8000

### Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript (no frameworks!)
- **Map Generation**: Python with OSMnx, Matplotlib, GeoPandas
- **Data Sources**: OpenStreetMap (via OSMnx) + GeoNames cities15000
- **Hosting**: Static site - no backend needed!

### Project Structure

```
citydle/
├── public/              # Frontend (deploy this folder)
│   ├── index.html      # Main game interface
│   ├── styles.css      # Styling
│   ├── game.js         # Game logic
│   └── maps/           # Generated maps (gitignored)
├── map_generator.py    # Creates styled maps from OSM data
├── city_selector.py    # Daily city selection logic
├── generate_daily_maps.py  # Batch map generation
└── data/cities15000.txt    # GeoNames city database
```

### Deployment

The game is designed as a static site for easy deployment to Vercel, Netlify, or GitHub Pages:

1. **Pre-generate maps** for 30-90 days:
   ```bash
   python generate_daily_maps.py --days 60
   ```

2. **Deploy the `public/` folder** to your hosting platform of choice

For automated daily map generation with GitHub Actions, see [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md).

### Contributing

Contributions are welcome! Feel free to:
- Report bugs or suggest features via [Issues](../../issues)
- Submit pull requests
- Fork the project and make it your own

**Documentation:**
- [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) - Detailed setup, deployment, and customization
- [CLAUDE.md](CLAUDE.md) - Development notes and architecture

---

## License

MIT

## Acknowledgments

- Map data from [OpenStreetMap](https://www.openstreetmap.org/)
- City data from [GeoNames](https://www.geonames.org/)
- Built with [OSMnx](https://github.com/gboeing/osmnx)
