from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
# from rest_framework.views import APIView
# from rest_framework.response import Response
from django.contrib.gis.geos import Point
import pydeck as pdk
from django.conf import settings
import os
import re
import folium
from .utils import make_markers_and_add_to_map
import xyzservices.providers as xyz
import folium.plugins as plugins


# def home(request):
#     return render(request, template_name='map/home.html')


class HomeMapView(TemplateView):
    template_name = 'map/index.html'
  
    
class MapView(TemplateView):
    template_name = 'map/map.html'    

    def get_context_data(self, **kwargs):
        figure = folium.Figure()
        

        # Make the map
        map = folium.Map(
            location = [40.416, -3.70],
            zoom_start = 11,
            tiles = 'Stadia.StamenWatercolor')
        
        tile_provider = xyz.Stadia.StamenToner
        tile_provider["url"] = tile_provider["url"] + "?api_key={api_key}"

        plugins.Geocoder().add_to(map)
        folium.TileLayer(
            tiles=tile_provider.build_url(api_key='62a84e8e-27d0-4f67-a68b-132baef17d6f'),
            attr=tile_provider.attribution,
            name=tile_provider.name,
            max_zoom=tile_provider.max_zoom,
            detect_retina=True
        ).add_to(map)

        map.add_to(figure)
        
        # Add a click to markers
        
        # # Fetch the objects from database and make Markers for them
        # for house in House.objects.all():
        #     make_markers_and_add_to_map(map, house)
      
        # Render and send to template
        figure.render()
        return {"map": figure}

class LondonMapView(TemplateView):
    # These are just parameters for ListView
    # What model to use in each post
    # What template to use
    template_name = 'map/hexagon_map.html'
    # Method to get context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN
    #     context['default_lat'] = 40.7128  # New York default coords
    #     context['default_lng'] = -74.0060
    #     return context
    # Set order of posts to be most recent first
    # ordering = ['-date_posted']
    # paginate_by = 5

def deckgl_view(request):
    # Your deck.gl layer definition
    layer = pdk.Layer(
        "HexagonLayer",
        "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv",
        get_position="[lng, lat]",
        elevation_scale=50,
        extruded=True,
        pickable=True,
        elevation_range=[0, 3000],
        coverage=1,
    )

    # Your initial view state
    initial_view_state = pdk.ViewState(
        latitude=52.2323,
        longitude=-1.415,
        zoom=6,
        pitch=40.5,
        bearing=-27.36,
    )

    # Create the pydeck chart
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=initial_view_state,
        map_provider="carto",
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip=True,
    )

    # Generate the HTML as a string
    deck_html = r.show()
    # Pass the HTML string to the template context
    context = {'deck_map_html': deck_html}
    return render(request, 'map/deckgl_template.html', context)


def hexagon_map(request):
    # Singapore accident data (replace with your actual data)
    UK_ACCIDENTS_DATA = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
    
    # Define the layer
    layer = pdk.Layer(
        'HexagonLayer',  # `type` positional argument is here
        UK_ACCIDENTS_DATA,
        get_position=['lng', 'lat'],
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=1)

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=-1.415,
        latitude=52.2323,
        zoom=6,
        min_zoom=5,
        max_zoom=15,
        pitch=40.5,
        bearing=-27.36)

    # Generate HTML
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='light'  # OSM-compatible style
    )
    # full_html = deck.to_html()
    # map_only = re.search(r'<div id="deck-container-[^"]*".*?</div>.*?<script.*?</script>', full_html, re.DOTALL).group()

    # Pass the rendered HTML to template
    return render(request, 'map/hexagon_map.html', {
        'map_html': map_only
    })


