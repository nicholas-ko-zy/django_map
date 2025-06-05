document.addEventListener("DOMContentLoaded", function () {
  const { map, markerLayer } = window.appMap;
  const markers = []; // This array tracks all markers
  let lastQuery = '';

  // Leaflet Search with Nominatim
  const searchControl = new L.Control.Search({
    url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
    jsonpParam: 'json_callback',
    propertyName: 'display_name',
    propertyLoc: ['lat', 'lon'],
    autoCollapse: true,
    autoType: false,
    minLength: 3,
    zoom: 14,
    marker: false,
  });

  map.addControl(searchControl);

  // Function to remove a marker and its table entry
  function removeMarker(index) {
      if (markers[index]) {
          markerLayer.removeLayer(markers[index]); // Remove from map
          markers.splice(index, 1); // Remove from array
          updateMarkerTable(); // Refresh the table
      }
  }

  // Function to update the marker table
  function updateMarkerTable() {
      const table = document.getElementById('marker-table');
      table.innerHTML = ''; // Clear the table

      // Add header row
      const headerRow = table.insertRow();
      headerRow.innerHTML = '<th>Location</th><th>Coordinates</th><th>Remove?</th>';

      // Add a row for each marker
      markers.forEach((marker, index) => {
          const name = marker.getPopup().getContent();
          const latlng = marker.getLatLng();
          const row = table.insertRow();
          row.innerHTML = `
              <td>${name}</td>
              <td>${latlng.lat.toFixed(5)}, ${latlng.lng.toFixed(5)}</td>
              <td><button onclick="removeMarker(${index})">Remove</button></td>
          `;
      });
  }

  searchControl._input.addEventListener('input', function (e) {
    lastQuery = e.target.value;
  });

  searchControl.on('search:locationfound', function (e) {
    const latlng = e.latlng;
    const name = Object.keys(e.target._recordsCache)[0];
    const marker = L.marker(latlng).addTo(markerLayer)
      .bindPopup(name).openPopup();
    
    markers.push(marker); // Add to our markers array
    updateMarkerTable(); // Update the table
  });

  // Make removeMarker function available globally
  window.removeMarker = removeMarker;
});