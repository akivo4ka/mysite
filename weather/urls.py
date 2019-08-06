from django.urls import path

from . import views

app_name = 'weather'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('city/add/', views.CityCreateView.as_view(), name='city-add'),
    path('city/<int:pk>/', views.CityDetailView.as_view(), name='city-detail'),
]
