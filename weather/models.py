from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('weather:city-detail', args=[str(self.id)])

    def __str__(self):
        return '{}, {}'.format(self.name, self.country_code)

    class Meta:
        verbose_name_plural = 'cities'
        ordering = ('country_code', 'name')
