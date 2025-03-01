"""project_root/
├── manage.py
├── project_root/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── distance_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   │   ├── distance_app/
│   │   │   ├── map.html
│   ├── static/
│   │   ├── distance_app/
│   │   │   ├── style.css
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
"""
# settings.py (add 'distance_app' to INSTALLED_APPS)
INSTALLED_APPS = [
    ...
    'distance_app',
]

# urls.py (in project_root)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('distance_app.urls')),
]

# urls.py (in distance_app)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map_view'),
]

# forms.py
from django import forms

class LocationForm(forms.Form):
    from_location = forms.CharField(label='From', max_length=100)
    to_location = forms.CharField(label='To', max_length=100)

# views.py
from django.shortcuts import render
from .forms import LocationForm
import pydeck as pdk
import geopy.distance
from geopy.geocoders import Nominatim

def get_coordinates(location):
    geolocator = Nominatim(user_agent="django_pydeck_app")
    location = geolocator.geocode(location)
    return (location.latitude, location.longitude) if location else (None, None)

def map_view(request):
    form = LocationForm()
    distance = None
    map_html = ""

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            to_location = form.cleaned_data['to_location']

            from_coords = get_coordinates(from_location)
            to_coords = get_coordinates(to_location)

            if None not in from_coords + to_coords:
                distance = geopy.distance.distance(from_coords, to_coords).km

                # Create a Pydeck map
                view_state = pdk.ViewState(
                    latitude=(from_coords[0] + to_coords[0]) / 2,
                    longitude=(from_coords[1] + to_coords[1]) / 2,
                    zoom=5
                )

                layer = pdk.Layer(
                    "LineLayer",
                    data=[{
                        "from": {"lat": from_coords[0], "lon": from_coords[1]},
                        "to": {"lat": to_coords[0], "lon": to_coords[1]}
                    }],
                    get_source_position="[from.lon, from.lat]",
                    get_target_position="[to.lon, to.lat]",
                    get_width=5,
                    get_color=[255, 0, 0],
                    pickable=True
                )

                deck = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state
                )

                map_html = deck.to_html(as_string=True)

    return render(request, 'distance_app/map.html', {'form': form, 'distance': distance, 'map_html': map_html})

# map.html
<!DOCTYPE html>
<html>
<head>
    <title>Distance Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        form { margin-bottom: 20px; }
        #map { width: 100%; height: 500px; }
    </style>
</head>
<body>
    <h1>Distance Calculator</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Calculate Distance</button>
    </form>

    {% if distance %}
        <p><strong>Distance:</strong> {{ distance|floatformat:2 }} km</p>
    {% endif %}

    <div id="map">{{ map_html|safe }}</div>
</body>
</html>

# requirements.txt
Django
pydeck
geopy
