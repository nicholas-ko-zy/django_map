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


# def home(request):
#     return render(request, template_name='map/home.html')


class HomeMapView(TemplateView):
    # These are just parameters for ListView
    # What model to use in each post
    # What template to use
    template_name = 'map/leaflet/index.html'
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


