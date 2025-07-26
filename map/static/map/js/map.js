// map.js
import { MAP_CONFIG } from './constants.js';
// Use Leaflet global L object
const CENTER = [1.37564, 103.79740];
const ZOOM_LEVEL = 10.5;

const map = L.map('map').setView(CENTER, ZOOM_LEVEL);

const markerLayer = L.layerGroup().addTo(map);
window.appMap = { map, markerLayer };

const tileLayer = L.tileLayer(
  `${MAP_CONFIG.TILE_LAYER.URL}?api_key=${MAP_CONFIG.TILE_LAYER.API_KEY}`, 
  {
    maxZoom: MAP_CONFIG.TILE_LAYER.MAX_ZOOM,
    attribution: MAP_CONFIG.TILE_LAYER.ATTRIBUTION
  }
).addTo(map);

const markerLayer = L.layerGroup().addTo(map);

// Make available globally if needed
window.appMap = { map, markerLayer };
