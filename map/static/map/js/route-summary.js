export function renderRouteSummary(vehicles, locationNames) {
    const container = document.getElementById('route-summary');
    if (!container) return;
  
    container.innerHTML = ''; // Clear previous content
  
    const colors = ['#3388ff', '#ff5733', '#33ff57', '#f033ff'];
  
    vehicles.forEach((vehicle, idx) => {
      const color = colors[idx % colors.length];
      const routeDiv = document.createElement('div');
      routeDiv.className = 'route-summary-route';
      routeDiv.style.borderColor = color;
  
      // Create colored box for route color
      const colorBox = document.createElement('span');
      colorBox.className = 'route-color-box';
      colorBox.style.backgroundColor = color;
  
      // Build route text: location1 -> location2 -> ...
      // vehicle.route is array of indices, map to locationNames
      const routeText = vehicle.route
        .map(i => locationNames[i] || `Loc ${i}`)
        .join(' → ');
  
      // Compose route div content
      routeDiv.appendChild(colorBox);
      routeDiv.appendChild(document.createTextNode(routeText));
  
      container.appendChild(routeDiv);
    });
  }
  