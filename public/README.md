# Citydle Frontend

Simple, clean web interface for the Citydle daily geography game.

## Features

- Dark theme with navy, cyan, and coral colors
- 5-level progressive map reveal
- Guess tracking and attempt counter
- Game state persistence (localStorage)
- Share results functionality
- Responsive design
- Help modal with instructions

## File Structure

```
public/
├── index.html          # Main game page
├── styles.css          # Styling
├── game.js            # Game logic
└── maps/              # Generated map images
    └── YYYY-MM-DD/    # Date-based folders
        ├── city.json  # City metadata
        ├── level1.png # Map images
        ├── level2.png
        ├── level3.png
        ├── level4.png
        └── level5.png
```

## Expected Map Structure

The frontend expects maps to be organized by date:

```
/maps/2026-01-24/city.json
/maps/2026-01-24/level1.png
/maps/2026-01-24/level2.png
...
```

### city.json format

```json
{
  "name": "Portland",
  "state": "Oregon",
  "country": "USA"
}
```

## Local Development

Use any static file server. Options:

**Python:**
```bash
python -m http.server 8000
```

**Node.js:**
```bash
npx http-server -p 8000
```

**VS Code:**
Install "Live Server" extension and right-click index.html

Then visit: `http://localhost:8000`

## Deployment

Can be deployed to any static hosting service:
- Vercel
- Netlify
- Cloudflare Pages
- GitHub Pages
- AWS S3 + CloudFront

Just upload the `public/` folder contents.

## Game Logic

- Game resets daily at midnight UTC
- State saved to localStorage
- Accepts city name variations (with/without state)
- Case-insensitive matching
- 5 attempts maximum
- Each wrong guess reveals next map level
