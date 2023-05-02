'''from django.urls import path
from . import views

urlpatterns = [
    path('he/', views.show),
]'''

from django.urls import path
from .views import temperature_map

urlpatterns = [
    path('he/', temperature_map, name='temperature-map'),
]
