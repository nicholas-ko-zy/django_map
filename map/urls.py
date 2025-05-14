from django.urls import path

from .views import (
    HomeMapView,
    hexagon_map,
    LondonMapView,
    deckgl_view,
)

urlpatterns = [
    # Empty path - Home page
    path('', HomeMapView.as_view(), name='map-home'),
    path('deck_gl_map', deckgl_view, name='deck-gl-demo'),
    ]