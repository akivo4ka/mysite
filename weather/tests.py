from django.test import TestCase
from django.urls import reverse

from .models import City


def create_city(name, country):
    """
    Create a city with the given name
    """
    return City.objects.create(name=name, country_code=country)


class CityIndexViewTest(TestCase):
    def test_no_cities(self):
        """
        If no cities exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('weather:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cities yet.")
        self.assertQuerysetEqual(response.context['cities'], [])

    def test_city(self):
        """
        City is displayed on the index page.
        """
        create_city(name='Moscow', country='RU')
        response = self.client.get(reverse('weather:index'))
        self.assertQuerysetEqual(
            response.context['cities'],
            ['<City: Moscow, RU>']
        )

    def test_cities(self):
        """
        Cities are displayed on the index page.
        """
        create_city(name='Moscow', country='RU')
        create_city(name='London', country='GB')
        create_city(name='New York', country='US')
        response = self.client.get(reverse('weather:index'))
        self.assertQuerysetEqual(
            response.context['cities'],
            ['<City: London, GB>', '<City: Moscow, RU>', '<City: New York, US>']
        )


class CityCreateViewTests(TestCase):
    def test_create_city(self):
        """
        Create view creates city (with correct name and country)
        """
        url = reverse('weather:city-add')
        self.client.post(url, {'name': 'Moscow,RU'})
        self.assertEquals(City.objects.count(), 1)

    def test_city_with_incorrect_name(self):
        """
        Create view does not create city with incorrect name
        """
        url = reverse('weather:city-add')
        self.client.post(url, {'name': 'Moscow123'})
        self.assertEquals(City.objects.count(), 0)

    def test_already_existing_city(self):
        """
        Create view does not create already existing city
        """
        url = reverse('weather:city-add')
        self.client.post(url, {'name': 'Moscow,RU'})
        self.client.post(url, {'name': 'Moscow,RU'})
        self.assertEquals(City.objects.count(), 1)

    def test_different_cities(self):
        """
        Check create view for different cities
        """
        url = reverse('weather:city-add')
        self.client.post(url, {'name': 'Moscow'})
        self.client.post(url, {'name': 'Moscow,RU'})
        self.client.post(url, {'name': 'Moscow123'})
        self.client.post(url, {'name': 'London,UK'})
        self.client.post(url, {'name': 'London'})
        self.client.post(url, {'name': 'New York,US'})
        self.client.post(url, {'name': 'NewYork,US'})
        self.assertEquals(City.objects.count(), 3)


class CityDetailViewTest(TestCase):
    def test_not_found_city(self):
        """
        Check detail view for city with incorrect name
        """
        city_with_incorrect_name = create_city('Moscow123', 'RU')
        url = reverse('weather:city-detail', args=(city_with_incorrect_name.id,))
        response = self.client.get(url)
        self.assertContains(response, 'city not found')

    def test_city(self):
        """
        Check detail view for city with correct name
        """
        city = create_city('Moscow', 'RU')
        url = reverse('weather:city-detail', args=(city.id,))
        response = self.client.get(url)
        self.assertContains(response, 'Moscow')
