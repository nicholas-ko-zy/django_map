// Wait for full initialization
function initRouteButton() {
    // Create button
    const routeButton = document.createElement('button');
    routeButton.id = 'route-button';
    routeButton.innerHTML = '🚗 Calculate Route';
    
    // Style the button (fixed at bottom center)
    Object.assign(routeButton.style, {
        position: 'fixed',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: '1000',
        padding: '12px 24px',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        borderRadius: '25px',
        cursor: 'pointer',
        fontSize: '16px',
        fontWeight: 'bold',
        boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
        display: 'block'
    });

    // Add to DOM (before map container)
    const mapDiv = document.getElementById('map');
    document.body.insertBefore(routeButton, mapDiv);

    // Click handler with AJAX implementation
    routeButton.addEventListener('click', async function() {
        if (!window.appMap?.markerLayer) {
            alert('Map is not ready. Please try again.');
            return;
        }

        const markers = window.appMap.markerLayer.getLayers();
        if (markers.length < 2) {
            alert('Please add at least 2 markers');
            return;
        }

        // Show loading state
        routeButton.disabled = true;
        routeButton.innerHTML = '⏳ Calculating...';

        try {
            // Prepare coordinates
            const coordinates = markers.map(marker => {
                const latlng = marker.getLatLng();
                return [latlng.lat, latlng.lng]; // Note: Changed to [lon,lat] to match expected format
            });
            
            // AJAX call to Django backend
            const response = await fetch('/solve-route/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({ coordinates })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            // Clear existing routes if any
            if (window.currentRoutes) {
                window.currentRoutes.forEach(route => {
                    window.appMap.map.removeLayer(route);
                });
            }

            // Process each vehicle route
            window.currentRoutes = [];
            const colors = ['#3388ff', '#ff5733', '#33ff57', '#f033ff']; // Different colors for each route
            
            result.vehicles.forEach((vehicle, index) => {
                // Convert path to GeoJSON LineString format
                const routeGeoJSON = {
                    type: 'Feature',
                    geometry: {
                        type: 'LineString',
                        coordinates: vehicle.path
                    },
                    properties: {
                        distance_km: vehicle.summary.distance_km,
                        duration_min: vehicle.summary.duration_min
                    }
                };

                // Draw route with unique color
                const routeLayer = L.geoJSON(routeGeoJSON, {
                    style: { 
                        color: colors[index % colors.length],
                        weight: 5,
                        opacity: 0.8
                    }
                }).addTo(window.appMap.map);

                // Add popup with route info
                routeLayer.bindPopup(`
                    <b>Route ${index + 1}</b><br>
                    Distance: ${vehicle.summary.distance_km.toFixed(1)} km<br>
                    Duration: ${vehicle.summary.duration_min.toFixed(1)} min
                `);

                window.currentRoutes.push(routeLayer);
            });

            // Zoom to show all routes if there are any
            if (window.currentRoutes.length > 0) {
                const bounds = window.currentRoutes.reduce((acc, route) => {
                    return acc.extend(route.getBounds());
                }, window.currentRoutes[0].getBounds());
                
                window.appMap.map.fitBounds(bounds);
            }

        } catch (error) {
            console.error('Routing error:', error);
            alert('Routing failed: ' + error.message);
        } finally {
            // Reset button state
            routeButton.disabled = false;
            routeButton.innerHTML = '🚗 Calculate Route';
        }
    });
}

// Helper to get CSRF token
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Initialize when ready
if (document.readyState === 'complete') {
    initRouteButton();
} else {
    window.addEventListener('load', initRouteButton);
}