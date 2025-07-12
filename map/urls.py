from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from .views import (
    HomeMapView,
    SolveRouteView,
)

urlpatterns = [
    # Empty path - Home page
    path('', HomeMapView.as_view(), name='map-home'),
    path('solve-route/', SolveRouteView.as_view(), name='solve-route')
    ]+ debug_toolbar_urls()