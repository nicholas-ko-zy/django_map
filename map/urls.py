from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from .views import (
    HomeMapView,
    hexagon_map,
    LondonMapView,
    MapView,
    deckgl_view,
)

urlpatterns = [
    # Empty path - Home page
    path('', HomeMapView.as_view(), name='map-home'),
    path('medium', MapView.as_view(), name='medium-map'),
    path('deck_gl_map', deckgl_view, name='deck-gl-demo'),
    ]+ debug_toolbar_urls()