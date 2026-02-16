# Moon Position Tracker | APIVerve API Tutorial

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab)](https://python.org)
[![APIVerve | Moon Position](https://img.shields.io/badge/APIVerve-Moon_Position-purple)](https://apiverve.com/marketplace/moonposition?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial)

A Python CLI tool to track the moon's position in the sky. Get altitude, azimuth, and distance from any location on Earth.

![Screenshot](https://raw.githubusercontent.com/apiverve/moon-tracker-python-tutorial/main/screenshot.jpg)

---

### Get Your Free API Key

This tutorial requires an APIVerve API key. **[Sign up free](https://dashboard.apiverve.com?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial)** - no credit card required.

---

## Features

- Track moon position from any coordinates
- Altitude above/below horizon
- Azimuth with compass direction
- Distance to the moon
- Support for custom date/time
- Pre-configured example locations
- Interactive CLI interface

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/apiverve/moon-tracker-python-tutorial.git
   cd moon-tracker-python-tutorial
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key**
   ```bash
   export APIVERVE_API_KEY=your-api-key-here
   ```

4. **Run the tracker**
   ```bash
   python tracker.py
   ```

## Project Structure

```
moon-tracker-python-tutorial/
├── tracker.py          # Main Python script
├── requirements.txt    # Python dependencies
├── screenshot.jpg      # Preview image
├── LICENSE             # MIT license
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. Select a location or enter coordinates
2. Optionally specify date and time
3. API calculates moon's position
4. Display altitude, azimuth, and distance

### The API Call

```python
response = requests.get('https://api.apiverve.com/v1/moonposition',
    headers={'x-api-key': API_KEY},
    params={
        'lat': 37.7749,
        'lon': -122.4194,
        'date': '01-22-2026',
        'time': '14:30'
    }
)
```

## API Reference

**Endpoint:** `GET https://api.apiverve.com/v1/moonposition`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lat` | number | Yes | Latitude (-90 to 90) |
| `lon` | number | Yes | Longitude (-180 to 180) |
| `date` | string | No | Date (MM-DD-YYYY format) |
| `time` | string | No | Time (HH:MM format) |

**Example Response:**

```json
{
  "status": "ok",
  "error": null,
  "data": {
    "date": "01-22-2026",
    "time": "14:30",
    "coordinates": {
      "latitude": 37.7749,
      "longitude": -122.4194
    },
    "moon": {
      "altitude": -0.407908976399288,
      "azimuth": 1.4720499058762104,
      "distance": 404332.68340679689
    }
  }
}
```

## Understanding the Data

| Field | Description |
|-------|-------------|
| `altitude` | Angle above/below horizon (radians). Positive = visible |
| `azimuth` | Compass direction (radians from north) |
| `distance` | Distance to moon in kilometers |

### Converting Radians to Degrees

```python
degrees = radians * (180 / 3.14159)
```

## Example Locations

| Location | Latitude | Longitude |
|----------|----------|-----------|
| San Francisco | 37.7749 | -122.4194 |
| New York | 40.7128 | -74.0060 |
| London | 51.5074 | -0.1278 |
| Tokyo | 35.6762 | 139.6503 |

## Customization Ideas

- Add moon phase data
- Create visualization graph
- Add sunrise/sunset comparison
- Build web interface
- Track multiple celestial bodies
- Add notification for moonrise

## Related APIs

Explore more APIs at [APIVerve](https://apiverve.com/marketplace?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial):

- [Moon Phases](https://apiverve.com/marketplace/moonphases?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial) - Current moon phase
- [Sun Position](https://apiverve.com/marketplace/sunposition?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial) - Track the sun
- [Sunrise Sunset](https://apiverve.com/marketplace/sunrisesunset?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial) - Daily sun times

## License

MIT - see [LICENSE](LICENSE)

## Links

- [Get API Key](https://dashboard.apiverve.com?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial) - Sign up free
- [APIVerve Marketplace](https://apiverve.com/marketplace?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial) - Browse 300+ APIs
- [Moon Position API](https://apiverve.com/marketplace/moonposition?utm_source=github&utm_medium=tutorial&utm_campaign=moon-tracker-python-tutorial) - API details
