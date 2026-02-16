#!/usr/bin/env python3
"""
Moon Position Tracker - APIVerve API Tutorial
Track the moon's position in the sky from any location.
"""

import os
import requests
from datetime import datetime

API_KEY = os.environ.get('APIVERVE_API_KEY', 'your-api-key-here')
API_URL = 'https://api.apiverve.com/v1/moonposition'


def get_moon_position(latitude, longitude, date=None, time=None):
    """Get moon position for given coordinates and optional date/time."""
    headers = {
        'x-api-key': API_KEY
    }

    params = {
        'lat': latitude,
        'lon': longitude
    }

    if date:
        params['date'] = date
    if time:
        params['time'] = time

    response = requests.get(API_URL, headers=headers, params=params)
    return response.json()


def format_altitude(altitude):
    """Convert altitude radians to degrees and description."""
    degrees = altitude * (180 / 3.14159)
    if degrees > 0:
        return f"{degrees:.1f}° above horizon"
    else:
        return f"{abs(degrees):.1f}° below horizon"


def format_azimuth(azimuth):
    """Convert azimuth radians to degrees and compass direction."""
    degrees = azimuth * (180 / 3.14159)
    degrees = degrees % 360

    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = int((degrees + 22.5) / 45) % 8

    return f"{degrees:.1f}° ({directions[index]})"


def format_distance(distance_km):
    """Format moon distance."""
    miles = distance_km * 0.621371
    return f"{distance_km:,.0f} km ({miles:,.0f} miles)"


def display_moon_position(data):
    """Display moon position data."""
    if data.get('status') != 'ok':
        print(f"Error: {data.get('error', 'Unknown error')}")
        return

    moon_data = data['data']
    coords = moon_data['coordinates']
    moon = moon_data['moon']

    print("\n" + "=" * 50)
    print("          MOON POSITION TRACKER")
    print("=" * 50)

    print(f"\n  Date: {moon_data['date']}")
    print(f"  Time: {moon_data['time']}")
    print(f"\n  Location:")
    print(f"    Latitude:  {coords['latitude']}°")
    print(f"    Longitude: {coords['longitude']}°")

    print(f"\n  Moon Position:")
    print(f"    Altitude: {format_altitude(moon['altitude'])}")
    print(f"    Azimuth:  {format_azimuth(moon['azimuth'])}")
    print(f"    Distance: {format_distance(moon['distance'])}")

    # Visibility indicator
    if moon['altitude'] > 0:
        print("\n    Status: Moon is VISIBLE above the horizon")
    else:
        print("\n    Status: Moon is below the horizon")

    print("\n" + "=" * 50)


def main():
    """Main function with example locations."""
    print("\nMoon Position Tracker")
    print("=====================")

    # Example locations
    locations = [
        {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194},
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    ]

    print("\nAvailable locations:")
    for i, loc in enumerate(locations, 1):
        print(f"  {i}. {loc['name']}")
    print("  5. Custom coordinates")

    try:
        choice = input("\nSelect location (1-5): ").strip()

        if choice == '5':
            lat = float(input("Enter latitude: "))
            lon = float(input("Enter longitude: "))
        elif choice in ['1', '2', '3', '4']:
            loc = locations[int(choice) - 1]
            lat, lon = loc['lat'], loc['lon']
            print(f"\nSelected: {loc['name']}")
        else:
            print("Invalid choice. Using San Francisco.")
            lat, lon = 37.7749, -122.4194

        # Optional date/time
        use_custom = input("\nUse current time? (y/n): ").strip().lower()
        date, time = None, None

        if use_custom == 'n':
            date = input("Enter date (MM-DD-YYYY): ").strip()
            time = input("Enter time (HH:MM): ").strip()

        print("\nFetching moon position...")
        result = get_moon_position(lat, lon, date, time)
        display_moon_position(result)

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except ValueError as e:
        print(f"\nInvalid input: {e}")
    except requests.RequestException as e:
        print(f"\nAPI request failed: {e}")


if __name__ == '__main__':
    main()
