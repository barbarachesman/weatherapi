"""weather_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.ApiView.as_view(), name='home'),
    path('city/<slug:city_name>', views.get_city_view, name='city'),
    path('delete/city/<slug:city_name>', views.delete_city, name='city_delete'),
    path('path/city/<slug:city_name>', views.path_city, name='city_path'),
    path('cities/max_temperatures', views.cities_max_temperatures, name='cities'),
    path('city/cep/<slug:cep>', views.cep_view, name='cep_view'),
]
