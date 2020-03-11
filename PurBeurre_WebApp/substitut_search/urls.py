from django.urls import path

from . import views

app_name = "substitut"
urlpatterns = [
    path('search/', views.search, name='search'),
]