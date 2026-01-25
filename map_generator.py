"""
Map generator prototype for Citydle.
Generates 5 detail levels of a city map using OpenStreetMap data.
"""

import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.patches as mpatches
from pathlib import Path

# Configure OSMnx
ox.settings.use_cache = True
ox.settings.log_console = False


def fetch_city_data(city_name: str = None, lat: float = None, lng: float = None, dist: int = 3000):
    """
    Fetch OSM data for a city.

    Args:
        city_name: Name of city (e.g., "Portland, Oregon, USA") - used if lat/lng not provided
        lat: Latitude (preferred over city_name for accuracy)
        lng: Longitude (preferred over city_name for accuracy)
        dist: Radius in meters from city center

    Returns:
        Dict with different map features
    """
    # Use coordinates directly if provided, otherwise geocode by name
    if lat is not None and lng is not None:
        center_point = (lat, lng)
        print(f"Using coordinates: {lat}, {lng}")
    elif city_name:
        center_point = ox.geocode(city_name)
        print(f"Geocoded '{city_name}' to: {center_point}")
    else:
        raise ValueError("Must provide either city_name or lat/lng coordinates")

    data = {}

    # Fetch street network
    print("Fetching streets...")
    data['streets'] = ox.graph_from_point(
        center_point, dist=dist, network_type='all'
    )

    # Fetch water bodies (expanded tags for better coverage)
    print("Fetching water...")
    try:
        data['water'] = ox.geometries_from_point(
            center_point, dist=dist,
            tags={'natural': ['water', 'bay', 'wetland'], 'water': True, 'landuse': 'reservoir'}
        )
        print(f"  Found {len(data['water'])} water features")
    except Exception as e:
        print(f"  No water features: {e}")
        data['water'] = None

    # Fetch rivers/streams (expanded for better river coverage)
    print("Fetching waterways...")
    try:
        data['waterways'] = ox.geometries_from_point(
            center_point, dist=dist,
            tags={'waterway': ['river', 'stream', 'canal']}
        )
        print(f"  Found {len(data['waterways'])} waterway features")
    except Exception as e:
        print(f"  No waterways: {e}")
        data['waterways'] = None

    # Fetch riverbanks/river areas (often polygons)
    print("Fetching river areas...")
    try:
        data['riverbanks'] = ox.geometries_from_point(
            center_point, dist=dist,
            tags={'waterway': 'riverbank', 'water': ['river', 'lake', 'pond']}
        )
        print(f"  Found {len(data['riverbanks'])} riverbank features")
    except Exception as e:
        print(f"  No riverbanks: {e}")
        data['riverbanks'] = None

    # Fetch buildings
    print("Fetching buildings...")
    try:
        data['buildings'] = ox.geometries_from_point(
            center_point, dist=dist,
            tags={'building': True}
        )
        print(f"  Found {len(data['buildings'])} buildings")
    except Exception as e:
        print(f"  No buildings: {e}")
        data['buildings'] = None

    # Fetch parks/green areas
    print("Fetching parks...")
    try:
        data['parks'] = ox.geometries_from_point(
            center_point, dist=dist,
            tags={'leisure': 'park'}
        )
        print(f"  Found {len(data['parks'])} parks")
    except Exception as e:
        print(f"  No parks: {e}")
        data['parks'] = None

    # Fetch major roads only (for level 1)
    print("Fetching major roads...")
    data['major_roads'] = ox.graph_from_point(
        center_point, dist=dist, network_type='drive',
        custom_filter='["highway"~"motorway|trunk|primary"]'
    )

    # Extract multiple major roads for level 4-5 hints
    # Prefer actual street names over highway refs (names are better clues)
    data['major_roads_list'] = []  # List of {'name': str, 'geom': geometry}
    try:
        import pandas as pd
        from shapely.ops import linemerge
        from collections import defaultdict

        edges = ox.graph_to_gdfs(data['major_roads'], nodes=False)

        # Group edges by street name (preferred) or ref as fallback
        road_edges = defaultdict(list)

        for _, edge in edges.iterrows():
            # Prefer actual street name over ref (better clue for game)
            name = edge.get('name')
            if name is not None and not (isinstance(name, float) and pd.isna(name)):
                if isinstance(name, list):
                    name = name[0]
                name = str(name)
                road_edges[name].append(edge.geometry)
            else:
                # Fall back to ref if no name
                ref = edge.get('ref')
                if ref is not None and not (isinstance(ref, float) and pd.isna(ref)):
                    if isinstance(ref, list):
                        ref = ref[0]
                    ref = str(ref)
                    road_edges[ref].append(edge.geometry)

        # Sort by total length and take top 3
        road_lengths = []
        for name, geoms in road_edges.items():
            total_length = sum(g.length for g in geoms)
            road_lengths.append((name, geoms, total_length))

        road_lengths.sort(key=lambda x: x[2], reverse=True)

        # Take top 3 roads
        for name, geoms, _ in road_lengths[:3]:
            merged = linemerge(geoms)
            data['major_roads_list'].append({
                'name': name,
                'geom': merged
            })

        road_names = [r['name'] for r in data['major_roads_list']]
        print(f"Found major roads: {road_names}")
    except Exception as e:
        print(f"Could not extract road names: {e}")

    return data, center_point


def render_level(data: dict, level: int, output_path: str = None, figsize=(10, 10)):
    """
    Render map at a specific detail level (1-5).

    Level 1: Water + major roads only (very abstract)
    Level 2: Water + more streets
    Level 3: Water + all streets + parks
    Level 4: Water + streets + parks + some buildings
    Level 5: Full detail
    """
    fig, ax = plt.subplots(figsize=figsize, facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    # Common style settings
    water_color = '#4a90a4'
    street_color = '#3d3d5c'
    street_color_light = '#5c5c8a'
    park_color = '#2d5a3d'
    building_color = '#4a4a6a'

    # Level 1: Just water and major roads
    if level >= 1:
        # Draw water bodies
        if data.get('water') is not None and len(data['water']) > 0:
            data['water'].plot(ax=ax, color=water_color, alpha=0.9)

        if data.get('waterways') is not None and len(data['waterways']) > 0:
            data['waterways'].plot(ax=ax, color=water_color, alpha=0.8, linewidth=4)

        if data.get('riverbanks') is not None and len(data['riverbanks']) > 0:
            data['riverbanks'].plot(ax=ax, color=water_color, alpha=0.9)

        # Draw major roads
        if data.get('major_roads') is not None:
            ox.plot_graph(
                data['major_roads'], ax=ax,
                node_size=0, edge_color=street_color,
                edge_linewidth=1.5, edge_alpha=0.5,
                show=False, close=False
            )

    # Level 2: Add more streets
    if level >= 2:
        if data.get('streets') is not None:
            ox.plot_graph(
                data['streets'], ax=ax,
                node_size=0, edge_color=street_color,
                edge_linewidth=0.5, edge_alpha=0.4,
                show=False, close=False
            )

    # Level 3: Add parks
    if level >= 3:
        if data.get('parks') is not None and len(data['parks']) > 0:
            data['parks'].plot(ax=ax, color=park_color, alpha=0.6)

    # Level 4: Add some buildings (simplified) + highlight major road
    if level >= 4:
        if data.get('buildings') is not None and len(data['buildings']) > 0:
            # Only show a subset of buildings
            buildings = data['buildings'].head(len(data['buildings']) // 3)
            buildings.plot(ax=ax, color=building_color, alpha=0.4)

        # Highlight major roads (no labels yet)
        for road in data.get('major_roads_list', []):
            geom = road['geom']
            if hasattr(geom, 'geoms'):  # MultiLineString
                for line in geom.geoms:
                    xs, ys = line.xy
                    ax.plot(xs, ys, color='#ff6b6b', linewidth=3, alpha=0.6, zorder=10)
            else:  # LineString
                xs, ys = geom.xy
                ax.plot(xs, ys, color='#ff6b6b', linewidth=3, alpha=0.6, zorder=10)

    # Level 5: Full buildings + street labels on the map
    if level >= 5:
        if data.get('buildings') is not None and len(data['buildings']) > 0:
            data['buildings'].plot(ax=ax, color=building_color, alpha=0.6)

        # Highlight major roads and label them
        import numpy as np
        from adjustText import adjust_text as adjust_text_func

        texts = []
        for road in data.get('major_roads_list', []):
            geom = road['geom']
            road_name = road['name']

            # Draw the road thicker/brighter to highlight it
            if hasattr(geom, 'geoms'):  # MultiLineString
                for line in geom.geoms:
                    xs, ys = line.xy
                    ax.plot(xs, ys, color='#ff6b6b', linewidth=4, alpha=0.8, zorder=10)
            else:  # LineString
                xs, ys = geom.xy
                ax.plot(xs, ys, color='#ff6b6b', linewidth=4, alpha=0.8, zorder=10)

            # Get midpoint for label placement
            if hasattr(geom, 'geoms'):
                # Use the longest segment
                longest = max(geom.geoms, key=lambda g: g.length)
                coords = list(longest.coords)
            else:
                coords = list(geom.coords)

            # Find midpoint
            mid_idx = len(coords) // 2
            mid_x, mid_y = coords[mid_idx]

            # Add text (adjustText will handle positioning)
            txt = ax.text(
                mid_x, mid_y, road_name,
                fontsize=10, color='white', alpha=0.95,
                fontweight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ff6b6b', alpha=0.9, edgecolor='none'),
                zorder=11
            )
            texts.append(txt)

        # Adjust text positions to avoid overlaps
        if texts:
            adjust_text_func(texts, ax=ax, expand_points=(1.5, 1.5),
                            force_text=(0.5, 0.5), force_points=(0.5, 0.5))

    # Clean up axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    # Add level indicator
    ax.text(
        0.02, 0.98, f"Attempt {level}/5",
        transform=ax.transAxes,
        fontsize=12, color='white', alpha=0.7,
        verticalalignment='top'
    )

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor='#1a1a2e', edgecolor='none')
        print(f"Saved: {output_path}")

    return fig, ax


def generate_all_levels(city_name: str = None, lat: float = None, lng: float = None, output_dir: str = "output"):
    """Generate all 5 levels for a city using name or coordinates."""
    Path(output_dir).mkdir(exist_ok=True)

    if lat is not None and lng is not None:
        print(f"Generating maps for coordinates: {lat}, {lng}")
    else:
        print(f"Generating maps for: {city_name}")
    print("-" * 40)

    data, center = fetch_city_data(city_name=city_name, lat=lat, lng=lng)

    for level in range(1, 6):
        print(f"\nRendering level {level}...")
        output_path = Path(output_dir) / f"level_{level}.png"
        render_level(data, level, str(output_path))
        plt.close()

    print("\nDone! Check the output folder.")


if __name__ == "__main__":
    # Test with a sample city
    generate_all_levels("Portland, Oregon, USA")
