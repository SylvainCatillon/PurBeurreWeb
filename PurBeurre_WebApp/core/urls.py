from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('universe/', views.universe, name='universe'),
]