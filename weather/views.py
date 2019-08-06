import datetime

import requests
from django import forms
from django.views import generic
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .models import City

APP_ID = '332aff71953e43412a946ab10190bc7a'
ERROR_MSG = 'Something went wrong. Try again later'


class IndexView(generic.ListView):
    template_name = 'weather/index.html'
    context_object_name = 'cities'

    def get_queryset(self):
        return City.objects.all()


def get_city_data(city_name):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[422, 500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    response = session.get('http://api.openweathermap.org/data/2.5/weather',
                           params={'q': city_name, 'APPID': APP_ID})
    data = response.json()
    return data


def update_new_city(new_city, data):
    name = data['name']
    country = data['sys']['country']
    new_city.name = name
    new_city.country_code = country


class CityCreateView(generic.CreateView):
    model = City
    template_name = 'weather/city_add.html'
    fields = ['name']

    def form_valid(self, form):
        new_city = form.save(commit=False)
        user_name = new_city.name.strip().split(',')[0]
        data = get_city_data(new_city.name)
        if not data:
            form.add_error(None, forms.ValidationError(ERROR_MSG))
            return super().form_invalid(form)
        if not is_data_cod_success(data):
            form.add_error(None, forms.ValidationError('Error: {}'.format(data)))
            return super().form_invalid(form)
        update_new_city(new_city, data)
        if City.objects.filter(name=user_name, country_code=new_city.country_code).count() > 0:
            form.add_error(None, forms.ValidationError('This City already exists'))
            return super().form_invalid(form)
        new_city.save()
        return super().form_valid(form)


def is_data_cod_success(data):
    return data.get('cod') == 200


class CityDetailView(generic.DetailView):
    model = City
    template_name = 'weather/city_detail.html'

    def parse_weather_data(self, data):
        time = datetime.datetime.fromtimestamp(data['dt']).strftime("%a %e %b %Y %H:%M")
        weather_description = data['weather'][0]['description']
        temperature_abs = data['main']['temp']
        temperature_celsius = round(temperature_abs - 273.15)
        temperature_fahrenheit = round(9 / 5 * temperature_abs - 459.67)
        name = self.object.name
        weather_data = {'city': name,
                        'time': time,
                        'description': weather_description,
                        'temperature_celsius': temperature_celsius,
                        'temperature_fahrenheit': temperature_fahrenheit
                        }
        return weather_data

    def get_weather_data(self):
        full_name = '{},{}'.format(self.object.name, self.object.country_code)
        data = get_city_data(full_name)
        if not data:
            return {'error': ERROR_MSG}
        if not is_data_cod_success(data):
            return {'error': data}
        weather_data = self.parse_weather_data(data)
        return weather_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        weather_data = self.get_weather_data()
        context['weather_data'] = weather_data
        return context
