export const markers = [];

let mapInstance = null;
let markerLayerInstance = null;

export function initialize(map, markerLayer) {
  mapInstance = map;
  markerLayerInstance = markerLayer;
}

export function addMarker(latlng, name) {
  if (!mapInstance || !markerLayerInstance) {
    console.error("MarkerManager not initialized with map and markerLayer");
    return;
  }
  const marker = L.marker(latlng).addTo(markerLayerInstance).bindPopup(name);
  markers.push(marker);
  updateMarkerTable();
}

export function removeMarker(index) {
  if (index >= 0 && index < markers.length) {
    markerLayerInstance.removeLayer(markers[index]);
    markers.splice(index, 1);
    updateMarkerTable();
  }
}

// Update the sidebar marker table
export function updateMarkerTable() {
  const tbody = document.querySelector("#marker-table tbody");
  if (!tbody) return;

  tbody.innerHTML = "";

  markers.forEach((marker, index) => {
    const name = marker.getPopup().getContent();
    const { lat, lng } = marker.getLatLng();

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${name}</td>
      <td>${lat.toFixed(5)}, ${lng.toFixed(5)}</td>
      <td><button onclick="window.removeMarker(${index})">Remove</button></td>
    `;
    tbody.appendChild(row);
  });
}

// Expose removeMarker globally for sidebar buttons
window.removeMarker = removeMarker;
