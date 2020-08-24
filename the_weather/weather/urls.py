from django.urls import path

from weather import views

urlpatterns = [
   path('', views.index, name='home'),
   path('delete/<city_name>', views.delete_city, name='delete-city')
]