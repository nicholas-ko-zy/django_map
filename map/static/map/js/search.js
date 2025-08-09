import * as MarkerManager from './marker-manager.js';

document.addEventListener("DOMContentLoaded", function () {
  const { map, markerLayer } = window.appMap;

  // Initialize marker manager with map and markerLayer
  MarkerManager.initialize(map, markerLayer);

  const sidebar = document.getElementById("mySidebar");
  const main = document.getElementById("main");
  const toggleBtn = document.getElementById("sidebarToggle");
  const toggleIcon = toggleBtn.querySelector("i");

  function openNav() {
    sidebar.style.width = "400px";
    main.style.marginRight = "400px";
    toggleIcon.classList.remove("fa-caret-left");
    toggleIcon.classList.add("fa-caret-right");
  }

  function closeNav() {
    sidebar.style.width = "0";
    main.style.marginRight = "0";
    toggleIcon.classList.remove("fa-caret-right");
    toggleIcon.classList.add("fa-caret-left");
  }

  toggleBtn.addEventListener("click", () => {
    if (sidebar.style.width === "400px") {
      closeNav();
    } else {
      openNav();
    }
  });

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

  searchControl._input.addEventListener('input', function (e) {
  });

  searchControl.on('search:locationfound', function (e) {
    const latlng = e.latlng;
    const clickedLat = latlng.lat;
    const clickedLng = latlng.lng;

    // Find the matching name from the search records cache
    let name = Object.keys(e.target._recordsCache).find(address => {
      const record = e.target._recordsCache[address];
      return record.lat === clickedLat && record.lng === clickedLng;
    }) || "Unknown Location";

    // Use MarkerManager to add the marker and update table
    MarkerManager.addMarker(latlng, name);
  });
});
