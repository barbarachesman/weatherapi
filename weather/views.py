from datetime import datetime

from django.shortcuts import render
import requests
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DeleteView, ListView

from weather.models import City, Temperatures


def home(request):
    response = requests.get('https://api.hgbrasil.com/weather?array_limit=2&fields=only_results,temp,city_name,results,tem,date,date&key=65b97445&city_name=Campinas,SP')
    weather = response.json()
    return render(request, 'weather_api/templates/home.html', {
        'temperature': weather['temp'],
        'date': weather['date'],
        'city': weather['city_name']
    })


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        city_name = self.kwargs.get('city_name')
        print(city_name)
        response = requests.get(
            'https://api.hgbrasil.com/weather?array_limit=2&fields=only_results,temp,city_name,results,tem,date,date&key=65b97445&city_name=Campinas,SP')
        context = response.json()
        print(context)
        # context['temperature'] = context[0]
        # context['date'] = context[1]
        # context['city'] = context[2]
        return context


class CityView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        city_name = self.kwargs.get('city_name')
        url = 'https://api.hgbrasil.com/weather?array_limit=2&fields=only_results,temp,city_name,results,tem,date,time&key=828262e3&city_name=' + city_name
        print(url)
        response = requests.get(url)
        context = response.json()
        print(response.json())
        new_city, created = City.objects.get_or_create(city_name=city_name)
        print(new_city, created)
        # if created:
        datetime_weather = context['date'] + " " + context['time']
        datetime_weather_formatted = datetime.strptime(datetime_weather, '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M:%S")

        teste = Temperatures.objects.create(
                city=new_city,
                date=datetime_weather_formatted,
                temperature=context['temp']
            )
        print(teste)
        # if created:
        #     print('criou')

        return context
        # else:
        #     print('ja tinha')
        #
        #     return response.json()
        #
        #


class DeleteCity(DeleteView):
    model = City

    success_url = reverse_lazy('home')  # This is where this view will

    def delete(self, request, *args, **kwargs):
        city_name = self.kwargs.get('city_name')
        deletea = City.objects.get(city_name=city_name).delete()
        return deletea
    # redirect the user


def delete(city_name):
    city = City.objects.get(city_name=city_name)
    a = Temperatures.objects.get(city=city).delete()
    a.save()



class PathCity(DeleteView):
    model = City
    template_name = 'home.html'
    slug_field = 'city_name'
    slug_url_kwarg = 'city_name'

    def delete(self, request, *args, **kwargs):
        city_name = self.kwargs.get('city_name')
        city = City.objects.get(city_name=city_name)
        a = Temperatures.objects.get(city=city).delete()
        a.save()


class CEPView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        response = requests.get('https://viacep.com.br/ws/01001000/json/')
        context = response
        print(context)
        context['temperature'] = context[0]
        # context['date'] = context[1]
        # context['city'] = context[2]
        return context


class HomeListView(ListView):
    model = Temperatures
    queryset = Temperatures.objects.all()
    context_object_name = 'book_list'
    template_name = 'home.html'
