import * as MarkerManager from './marker-manager.js';

document.addEventListener("DOMContentLoaded", () => {
  const dropzoneElement = document.getElementById("file-uploader");
  if (!dropzoneElement) {
    console.error("Dropzone element #file-uploader not found");
    return;
  }

  // Disable autoDiscover to prevent Dropzone attaching automatically
  Dropzone.autoDiscover = false;

  const myDropzone = new Dropzone(dropzoneElement, {
    url: "/file/post",  // Your upload endpoint if needed; can be dummy if parsing client-side
    maxFilesize: 5,      // MB
    acceptedFiles: ".csv",
    parallelChunkUploads: false,

    // If you want to parse CSV client-side instead of uploading to server,
    // you can intercept the file here and parse it yourself
    autoProcessQueue: false, // We'll handle files manually

    init: function () {
      this.on("addedfile", (file) => {
        // Use FileReader to parse CSV content client-side
        const reader = new FileReader();
        reader.onload = (event) => {
          const csvText = event.target.result;
          parseCSVAndAddMarkers(csvText);
        };
        reader.readAsText(file);

        // Remove the file preview immediately, since we're not uploading to server
        this.removeFile(file);
      });
    },
  });

  function parseCSVAndAddMarkers(csvText) {
    // Simple CSV parsing assuming header: name,lat,lon
    // You can replace with a robust CSV parser like PapaParse if needed

    const lines = csvText.trim().split("\n");
    if (lines.length < 2) {
      alert("CSV must have at least one data row");
      return;
    }

    const header = lines[0].split(",").map(h => h.trim().toLowerCase());
    const nameIndex = header.indexOf("name");
    const latIndex = header.indexOf("lat");
    const lonIndex = header.indexOf("lon");

    if (nameIndex === -1 || latIndex === -1 || lonIndex === -1) {
      alert("CSV header must include 'name', 'lat', and 'lon' columns");
      return;
    }

    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(",").map(c => c.trim());
      const name = cols[nameIndex];
      const lat = parseFloat(cols[latIndex]);
      const lon = parseFloat(cols[lonIndex]);

      if (isNaN(lat) || isNaN(lon)) {
        console.warn(`Invalid coordinates at line ${i + 1}:`, cols);
        continue;
      }

      MarkerManager.addMarker([lat, lon], name);
    }
  }
});
