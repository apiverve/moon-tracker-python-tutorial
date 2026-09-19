import { api, busy, esc, showError, stats } from './ui.js';

const PLACES = [
  ['New York', 40.7128, -74.006],
  ['London', 51.5074, -0.1278],
  ['Tokyo', 35.6762, 139.6503],
  ['Sydney', -33.8688, 151.2093],
  ['Cape Town', -33.9249, 18.4241]
];
const COMPASS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];

const form = document.getElementById('form');
const lat = document.getElementById('lat');
const lon = document.getElementById('lon');
const go = document.getElementById('go');
const here = document.getElementById('here');
const result = document.getElementById('result');

const deg = (radians) => (radians * 180) / Math.PI;
const km = (n) => Math.round(n).toLocaleString();

document.getElementById('places').innerHTML = PLACES
  .map(([name, la, lo]) => `<button type="button" data-lat="${la}" data-lon="${lo}">${esc(name)}</button>`)
  .join('');

document.getElementById('places').addEventListener('click', (e) => {
  const chip = e.target.closest('button');
  if (!chip) return;
  lat.value = chip.dataset.lat;
  lon.value = chip.dataset.lon;
  form.requestSubmit();
});

here.addEventListener('click', () => {
  if (!navigator.geolocation) return showError(result, 'This browser can’t share your location.');
  navigator.geolocation.getCurrentPosition(
    ({ coords }) => {
      lat.value = coords.latitude.toFixed(4);
      lon.value = coords.longitude.toFixed(4);
      form.requestSubmit();
    },
    () => showError(result, 'Location access was blocked. Enter coordinates instead.')
  );
});

// The API returns altitude and azimuth in radians. Azimuth is measured from
// south towards west, so add 180° for a compass bearing.
function describe(d) {
  const altitude = deg(d.moon.altitude);
  const up = altitude > 0;
  const rows = [['Altitude', `${Math.abs(altitude).toFixed(1)}° ${up ? 'above' : 'below'} the horizon`]];
  if (typeof d.moon.azimuth === 'number') {
    const bearing = (deg(d.moon.azimuth) + 180 + 360) % 360;
    rows.push(['Direction', `${bearing.toFixed(0)}° (${COMPASS[Math.round(bearing / 45) % 8]})`]);
  }
  if (typeof d.moon.distance === 'number') {
    rows.push(['Distance', `${km(d.moon.distance)} km (${km(d.moon.distance * 0.621371)} mi)`]);
  }
  rows.push(['Location', `${d.coordinates.latitude}, ${d.coordinates.longitude}`]);
  rows.push(['Time', `${d.time} UTC, ${d.date}`]);
  return `
    <div class="figure">
      <div class="big ${up ? 'good' : ''}">${up ? 'Above the horizon' : 'Below the horizon'}</div>
      <div class="sub">${up ? 'The moon is up at this location right now.' : 'The moon has set here. Try again later, or pick another place.'}</div>
    </div>
    ${stats(rows)}`;
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const now = new Date();
  const time = `${String(now.getUTCHours()).padStart(2, '0')}:${String(now.getUTCMinutes()).padStart(2, '0')}`;
  const query = new URLSearchParams({ lat: lat.value, lon: lon.value, time });
  busy(go, 'Looking up…', async () => {
    try {
      result.innerHTML = describe(await api(`/api/moon?${query}`));
    } catch (err) {
      showError(result, err);
    }
  });
});
