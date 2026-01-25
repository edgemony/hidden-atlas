# Hidden Atlas Frontend - Quick Start Guide

## What I've Created

A complete frontend for Hidden Atlas with:
- **HTML/CSS/JS game interface** in `public/` folder
- **Map generation script** to create daily city maps
- **Development server** for local testing
- Clean dark theme (navy, cyan, coral)
- Responsive design
- Game state persistence

## Project Structure

```
citydle/
├── public/                    # Frontend files
│   ├── index.html            # Main game page
│   ├── styles.css            # Styling
│   ├── game.js               # Game logic
│   ├── README.md             # Frontend docs
│   └── maps/                 # Generated maps (created on first run)
│       └── YYYY-MM-DD/
│           ├── city.json     # City metadata
│           ├── level1.png    # Map images
│           ├── level2.png
│           ├── level3.png
│           ├── level4.png
│           └── level5.png
├── generate_daily_maps.py    # Map generation script
├── serve.py                  # Development server
└── (existing files...)
```

## How to Use

### 1. Generate Maps for Testing

Generate maps for the next 7 days:

```bash
python generate_daily_maps.py --days 7
```

Or generate for a specific date:

```bash
python generate_daily_maps.py --date 2026-01-24
```

This will create:
- `public/maps/YYYY-MM-DD/level1.png` through `level5.png`
- `public/maps/YYYY-MM-DD/city.json` with city metadata

### 2. Start the Development Server

```bash
python serve.py
```

Then open your browser to: **http://localhost:8000**

### 3. Play the Game

1. Look at the map
2. Type your guess in the input box
3. Press Enter or click "Submit Guess"
4. If wrong, the next level reveals more detail
5. Try to guess in 5 attempts or less!

## Features

### Game Mechanics
- 5 attempts to guess the city
- Each wrong guess reveals more map detail
- Game state saves to browser localStorage
- New city each day at midnight UTC
- Share results to clipboard/social

### Progressive Map Levels
1. Water bodies + major highways
2. Full street grid
3. Parks (green areas)
4. Buildings + highlighted major roads
5. Full map with labeled streets

### UI Features
- Dark theme matching your design
- Responsive (works on mobile)
- Help modal with instructions
- Countdown to next game
- Guess history tracking

## Deployment Options

### Static Hosting (Recommended)

1. **Generate maps in advance**:
   ```bash
   python generate_daily_maps.py --days 30
   ```

2. **Deploy to Vercel/Netlify/Cloudflare Pages**:
   - Upload the `public/` folder
   - Configure to serve from root
   - Done!

### Automated Daily Generation

Set up a GitHub Action or cron job to run:
```bash
python generate_daily_maps.py --days 7
```

This keeps your maps fresh without manual work.

### Alternative: Dynamic Backend

If you want features like user accounts or leaderboards:
- Create a Python API (FastAPI/Flask)
- Generate maps on-demand
- Store in S3 or similar
- See CLAUDE.md for architecture options

## Customization

### Change Map Radius
Edit `map_generator.py` and adjust the `dist` parameter in `fetch_city_data()` (default: 3000m)

### Modify Color Scheme
Edit `public/styles.css` and change the CSS variables:
```css
:root {
    --navy: #1a1a2e;
    --cyan: #4a90a4;
    --coral: #ff6b6b;
}
```

### Adjust City Pool
Edit `city_selector.py` and change the `min_population` parameter to include more/fewer cities.

## Testing Checklist

- [ ] Generate maps for today's date
- [ ] Start development server
- [ ] Open http://localhost:8000
- [ ] Try making correct guess
- [ ] Try making 5 wrong guesses (see all levels)
- [ ] Check that game state persists on page reload
- [ ] Test "Share Results" button
- [ ] Click "How to Play" to see instructions
- [ ] Test on mobile/small screen

## Next Steps

1. **Test locally**: Generate a few days of maps and play through
2. **Refine cities**: Adjust min_population or curate a better city list
3. **Polish maps**: Tune the map styles and radius as needed
4. **Deploy**: Push to Vercel/Netlify for public access
5. **Automate**: Set up daily map generation

## Troubleshooting

**Maps not loading?**
- Check that maps exist in `public/maps/YYYY-MM-DD/`
- Verify the date matches today (UTC)
- Check browser console for errors

**Server won't start?**
- Make sure port 8000 isn't in use
- Run from the project root directory

**Maps look wrong?**
- Check your map_generator.py is working
- Try generating manually first
- Adjust the radius parameter

## Questions?

Check the files:
- `public/README.md` - Frontend details
- `CLAUDE.md` - Overall project docs
- Look at the code - it's well-commented!

Enjoy building Hidden Atlas!
