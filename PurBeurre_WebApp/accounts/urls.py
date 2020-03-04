from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path('create/', views.create, name='create'),
    path('myaccount/', views.my_account, name='my_account'),
]