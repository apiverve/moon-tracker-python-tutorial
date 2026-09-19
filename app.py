"""
The web app: the page in public/ and the API route it calls, which holds your key.

Run it locally with `python app.py`, then open http://localhost:3000
On Vercel, this file becomes a Python function and public/ is served from the CDN.
"""
import os
import re
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from apiverve import ApiError, api_key, call_api, rate_limited

app = Flask(__name__)
PUBLIC = Path(__file__).with_name('public')


@app.before_request
def guard():
    """Every /api route needs the key, and counts against the visitor's rate limit."""
    if not request.path.startswith('/api/'):
        return None
    api_key()
    ip = request.headers.get('x-forwarded-for', '').split(',')[0].strip() or request.remote_addr or 'local'
    if rate_limited(ip):
        return fail('Too many requests. Wait a minute and try again.', 429)
    return None


@app.errorhandler(ApiError)
def api_error(err):
    return fail(str(err), err.status)


def fail(message, status=400):
    return jsonify(error=message), status


TIME = re.compile(r'^([01]\d|2[0-3]):[0-5]\d$')


def coordinate(name, limit):
    try:
        value = float(request.args.get(name, ''))
    except ValueError:
        return None
    return value if -limit <= value <= limit else None


@app.get('/api/moon')
def moon():
    """GET /api/moon?lat=40.71&lon=-74.01&time=21:30: where the moon is in the sky (time is UTC, today)."""
    lat, lon = coordinate('lat', 90), coordinate('lon', 180)
    if lat is None or lon is None:
        return fail('Enter a latitude from -90 to 90 and a longitude from -180 to 180.')
    params = {'lat': round(lat, 4), 'lon': round(lon, 4)}
    time = request.args.get('time', '').strip()
    if time:
        if not TIME.match(time):
            return fail('Use a 24-hour time, like 21:30.')
        params['time'] = time
    return jsonify(call_api('moonposition', params))


# The page. On Vercel the CDN serves public/ before a request reaches this app;
# these routes serve it when you run the app locally.
@app.get('/')
def index():
    return send_from_directory(PUBLIC, 'index.html')


@app.get('/<path:name>')
def static_file(name):
    return send_from_directory(PUBLIC, name)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 3000)), debug=True)
