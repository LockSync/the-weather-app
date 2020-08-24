import requests
from django.shortcuts import render, redirect

# Create your views here.
from weather.forms import CityForm
from weather.models import City


def index(request):
    # use the API from WeatherOpenMap
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=ef2d6f3bfd01b0190126858aca4b20eb'
    cities = City.objects.all()
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            # get access to data during request.post

            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            # check if the city exists in database
            if existing_city_count == 0:
                # check if the city exists in the world
                r = requests.get(url.format(new_city)).json()
                print(r)
                # if code == 404 : the city doesn't exist
                # if the code == 200, the city exists
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesn't exist in the world"
            else:
                err_msg = 'City already exists in the database'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City add successfully'
            message_class = 'is-success'

    form = CityForm()
    weather_data = []
    for i in range(len(cities)):
        # format a string
        r = requests.get(url.format(cities[i].name)).json()
        city_weather = {
            'city': cities[i].name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    print(weather_data)
    context = {'weather_data': weather_data,
               'form': form,
               'message': message,
               'message_class': message_class
               }
    return render(request, 'weather/weather.html', context, )


# delete city
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')