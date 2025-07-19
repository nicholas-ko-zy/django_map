// map.js

// Use Leaflet global L object
const CENTER = [1.37564, 103.79740];
const ZOOM_LEVEL = 10.5;

const map = L.map('map').setView(CENTER, ZOOM_LEVEL);

L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png?api_key=62a84e8e-27d0-4f67-a68b-132baef17d6f', {
  maxZoom: 20,
  attribution: '&copy; <a href="https://stadiamaps.com/" target="_blank">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
}).addTo(map);
const markerLayer = L.layerGroup().addTo(map);

window.appMap = { map, markerLayer };

