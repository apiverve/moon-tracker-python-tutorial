#!/usr/bin/env python3
"""
Where the moon is, from the command line.

    python tracker.py 40.71 -74.01        # right now
    python tracker.py 40.71 -74.01 21:30  # at a time today (UTC)
    python tracker.py                     # pick a city

Reads APIVERVE_API_KEY from .env, like the web app.
"""
import math
import sys
from datetime import datetime, timezone

from apiverve import ApiError, call_api

PLACES = [
    ('New York', 40.7128, -74.006),
    ('London', 51.5074, -0.1278),
    ('Tokyo', 35.6762, 139.6503),
    ('Sydney', -33.8688, 151.2093),
]
COMPASS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']


def show(d):
    moon = d['moon']
    # Altitude and azimuth come back in radians; azimuth is measured from south.
    altitude = math.degrees(moon['altitude'])
    print(f"\n  {d['date']} {d['time']} UTC at {d['coordinates']['latitude']}, {d['coordinates']['longitude']}")
    print(f"  The moon is {'UP' if altitude > 0 else 'below the horizon'}: "
          f"{abs(altitude):.1f}° {'above' if altitude > 0 else 'below'}")
    if isinstance(moon.get('azimuth'), (int, float)):
        bearing = (math.degrees(moon['azimuth']) + 180) % 360
        print(f"  Direction  {bearing:.0f}° ({COMPASS[round(bearing / 45) % 8]})")
    if isinstance(moon.get('distance'), (int, float)):
        print(f"  Distance   {moon['distance']:,.0f} km")
    print()


def pick_place():
    for i, (name, _, _) in enumerate(PLACES, 1):
        print(f'  {i}. {name}')
    choice = input('\nPick a city: ').strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(PLACES):
        raise SystemExit('Pick a number from the list, or pass a latitude and longitude.')
    return PLACES[int(choice) - 1][1:]


def main():
    args = sys.argv[1:]
    try:
        lat, lon = (float(args[0]), float(args[1])) if len(args) >= 2 else pick_place()
    except ValueError:
        raise SystemExit('Usage: python tracker.py <latitude> <longitude> [HH:MM]')
    time = args[2] if len(args) >= 3 else datetime.now(timezone.utc).strftime('%H:%M')
    try:
        show(call_api('moonposition', {'lat': lat, 'lon': lon, 'time': time}))
    except ApiError as err:
        raise SystemExit(f'Error: {err}')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
