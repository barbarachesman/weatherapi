from datetime import datetime

from django.http import HttpResponse
import requests
from django.template.defaultfilters import lower
from django.views.generic import TemplateView, DeleteView, ListView

from weather.models import City, Temperatures


class HomeListView(ListView):
    model = Temperatures
    queryset = Temperatures.objects.all()
    context_object_name = 'book_list'
    template_name = 'home.html'


class ApiView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(ApiView, self).get_context_data(**kwargs)
        context['latest_temperatures'] = Temperatures.objects.all()[:5]
        context['cities_max_temperatures'] = cities_max_temperatures()
        context['cities'] = City.objects.all()

        return context


def get_city_view(request, city_name):
    url = 'https://api.hgbrasil.com/weather?array_limit=2&fields=only_results,temp,city_name,results,tem,date,time&key=6698769b&city_name=' + city_name

    response = requests.get(url)
    if response:
        context = response.json()
        new_city, created = City.objects.get_or_create(city_name=lower(city_name))
        datetime_weather = context['date'] + " " + context['time']
        datetime_weather_formatted = datetime.strptime(datetime_weather, '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M:%S")

        Temperatures.objects.create(
            city=new_city,
            date=datetime_weather_formatted,
            temperature=context['temp']
        )

        return HttpResponse("Add!")
    else:
        return HttpResponse("Chave API Bloqueada!")


def delete_city(request, city_name):
    City.objects.filter(city_name=lower(city_name)).delete()
    return HttpResponse("Deleted!")


def path_city(request, city_name):
    Temperatures.objects.filter(city__city_name=lower(city_name)).delete()
    return HttpResponse("Deleted!")


def cities_max_temperatures():
    temperatures = Temperatures.objects.order_by('-temperature')[:3]
    return temperatures


def cep_view(request, cep):
    url = 'https://viacep.com.br/ws/'+cep+'/json/'
    response = requests.get(url)
    data_cep = response.json()
    city_name = data_cep['localidade']
    City.objects.get_or_create(city_name=lower(city_name))

    return HttpResponse("Created city!")
