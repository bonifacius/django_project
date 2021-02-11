���������� � �������� ������ ���������� weather:

1. ����������*********************************************************************************

-���������:

python -m pip install django

-������� requirements.txt:

pip freeze > requirements.txt

-������� ���� .gitignore

-������� ������:
django-admin startproject WeatherApp

-������� ����������:
python manage.py startapp weather


2. ���������**********************************************************************************

-�������������� ���������� � WeatherApp /settings.py -> INSTALLED_APPS
 ����������� � ����� �������� ������ ����������
-python manage.py migrate

-������� ������ superuser: 

python manage.py createsuperuser

-��������� ������ �����:

python manage.py runserver

-��������� � urls.py, ����������� include.
�� ��������� ����� path '' ������ ������ ( ��� ���� ��������� ��������)
� ����� include �����������, ��� �� ���������� �� 'weather.urls'  :

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls'))
]

-������ ��������� � /weather(���� ����������), ������� ����� ���� urls
���������, ���������:

from django.urls import path
# �� ������� ���������� �� ����������� views
from . import views
urlpatterns = [
    path('admin/', views.index),
]


- ������ ����� weather_project/WeatherApp/weather/templates
������ ������� ����� /weather � � ��� ������� /index.html
��������:

/WeatherApp/weather/templates/weather/index.html 

- ��������� weather/views � ���������:
(�� ��������� index ������� � ����� templates)

from django.shortcuts import render

def index(request):
    return render(request, 'weather/index.html')

-�������� ������ � ��������� ����������� �� html

-��������� �� ���� ���������/examples
�������� ����� �� ��������, �������� ��� � ��������� � index.html
������ ������ ���� ���� ��� ��������� ������ � body:

<div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-wgite border-bottom shadow-sm">
        <h5 class="h5 my-0 me-md-auto fw-normal">��, ������!</h5>
        <nav class="my-2 my-md-0 me-md-3">
            <a class="p-2 text-dark" href="#">�������</a>
            <a class="p-2 text-dark" href="#">����������</a>
        </nav>
        <a class="btn btn-outline-primary" href="#">Sign up</a>
    </div>
    <div class="container">
        <div class="row">
            <div class="col-4 offset-1">
                <h1>������ � ����� ������</h1>
                <form action="">
                    <label for="city">�����</label>
                    <input type="text" id="city" class="form-control" name="city" placeholder="������� �����">
                    <input type="submit" name="send" value="������" class="mt-2 btn btn-danger">
                </form>
            </div>
            <div class="col-4 offset-1">
              <h1>����������</h1>
              <div class="alert alert-danger">
                  ������ � ������
              </div>
            </div>
        </div>
    </div>

3. API()*****************************************************************************************

-��������� �� ���� weathermap, ��������������

- ��������� � API keys
������������, ������� � api, current weather date, �������� 

Examples of API calls:

api.openweathermap.org/data/2.5/weather?q={}&appid={API key}

{API key} - ��������� ������ ����� ��� ����
{} - ���� �� ����� ����������� �����

-��������� �� veiews:
import requests
from django.shortcuts import render

def index(request):
    appid = 'e0b416b5d62ff64362bf0c4238e0494e'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=' + appid

    city = 'London'
    res = requests.get(url.format(city)).json()
    print(res.text)
    return render(request, 'weather/index.html')

-����� ��������� ������ � �������� ����� � ������� json ����� ���������� ������ request()
 import requests

������ ������ � ���������� url, � ������� ������� format() ��������� ���������� city � {} ������ url 
 res = requests.get(url.format(city))

print(res.text) - ��������� ������ � � �������� ��������� ��� ������� ����� � ������� json

json() - ��������� ���������� ���������� res � �������

� weather map � ������� API ������� 

Fields in API response;
� ���� �������� main.temp Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.

��������� � url ����� {}:
&units=metric


������� �������:
��� 'temp' �� ���������� � ������� res, �� ����� "main" �� ����� "temp"
city_info = {
	'city': city, 
	'temp': res["main"]["temp"],
	'icon': res["weather"][0]["icon"]
}
(�������, ��� ������������! ���� � weather ������� ���� ������ � ������� ���� �������. ����� [0] 
��� �� ��������� ������ ������� � ������ )
-��� �� �������� ������ � html ������:

������� ������� 
context = {'info': city_info} � �������� ��� ������ �������� �  index.html

return render(request, 'weather/index.html', context)

- ������ � index.html:

<div class="col-4 offset-1">
              <h1>����������</h1>
              <div class="alert alert-danger">
                  <b>�����:</b> {{ info.city }}<br>
                  <b>�����������:</b> {{ city.temp}}<sup>o</sup></br>
                  <img src="http://openweathermap.org/img/w/{{ city.icon}}.png" alt="���� ������" class="img-thumbnail">
                  
              </div>

� {} �� ���������� � ������� context, ����� 'info' � �������� ������� ��� ����


4. ������()

������ ������� � models.py 
 � ������� ����� ������(�������)

 class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

__str__ ����� ��� �� ���������� �� ������, � ���� ��������(�������� ����������� ������)

-������� ��������:         
python manage.py makemigration

-��������� �������� � ���� ������

-��������� � admin ���� ������(��� ����������� � �������)
������� ����������� ������

from .models import City 

admin.site.register(City)

-������ ��� ���� �������� ���������� � ������� ������� �� ����

��������� �� views:

�����������:
from .models import City

� index() ������� ���������� city, ������ ����� �������:

cities = City.objects.all() (����� ��� �� ��� ������� �� ������� City)

-����� ���� for ��������� ��� ������ �� cities:
-���� ������ ����� �������� � ������! ������� �� ����� ���������� � ������(context = {'info': city_info})  
������� ������ ������ all_cities = []
� � ����� ������ ��� ����� ��������� ����� ������(all_cities.append(city_info))


def index(request):
    appid = 'e0b416b5d62ff64362bf0c4238e0494e'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    cities = City.objects.all()
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city)).json()
        city_info = {
            'city': city.name, (.name ����� ��� �� ���������� � �������� ������ City)
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]
        }
        all_cities.append(city_info)

    context = {'info': city_info}

    return render(request, 'weather/index.html', context)

����� �� ������ �������� ������*****************************************************************

1. �� �������� ��� ������ �� ������� (cities = City.objects.all())
2. ���������� ������ ������ for � ������ ��� ������� ������ ������ � ���������� ��� � ����������  city_info
city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]

3. ���������� ��� ������ � ������:
...
all_cities = []
...
all_cities.append(city_info)

�� �������� ���������� ���������� �� ������ ���� ������ �� ���������� � �������:

    try:
        for city in cities:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"]
            }
            all_cities.append(city_info)
    except KeyError:
        pass

    except EXCEPTION as e:
        pass

4. ������ all_cities �������� � �������
	
	context = {'all_info': all_cities} 

5. � contex �������� ��� �������� 'all_info' � ������ index.html  

6. ��������� � index.html

����� <div class="alert alert-info"> � � ����� ����� ����� �����������:

{% for info in all_info %}
.....
{% endfor %}


5. �����***********************************************************************

-� ������� index() ����� ��������� ���� �� ���� ������.()
� index.html ��������� method:"post"
...
<h1>������ � ����� ������</h1>
                <form action="" method="post">
...
����� �� ����� �������� �� ������ "������"
...
 <input type="submit" name="send" value="������" class="mt-2 btn btn-danger">
...
����� ����������� �������� ������ �� ������ post
� � ������� index() �� ����� ���������: ���� ����������� ����� ���� �� ����� �������� ��� ������, 
�������� ������ ��� ������������� ��������(submit ������ ��� �������������)
���������:

� index() �����:

if(request.method=='POST')
	������� ������ � �������� ���������� �������� ������� �� �������� �� ������������(�������� ������)
	form = CityForm(requests.POST)
	������ �������� ������ � ��������� ��� � ���� ������:
	form.save()

-������� ��� ���� ������ ��� �� �������� �����
��� �������� ��� ���� ��� �� ����� �� ������������ ��������, ���� ����� ����� ������ ����������.
���� ��� �� �������, ��������� ������ �������� ������ 
form = CityForm()



-������� ���� forms.py
���������, �����������:

from .models import City
from django.forms import ModelForm, TextInput

class CityForm(ModelForm):
	class Meta:
		model = City
		fields = ['name']

��������� �� views � �����������:
from .forms import CityForm



-��������� views

� context ��������� �������� form:

context = {'all_info': all_cities, 'form': form}

������ ���� ������� ��������. ��������� � index.html ��������: 
...
{% csrf_token %}
<label for="city">�����</label>
{{ form.name}}
<input type="text" id="city" class="form-control" name="city" placeholder="������� �����">
...

-������� � forms, ��������� CityForm() ������� 

widgets = {'name': TextInput(attrs={'class': 'form-control', 
									'name':'city', 
									'id':'city', 
									'placeholder': '������� �����'
									})}

������� ����:
...
<input type="text" id="city" class="form-control" name="city" placeholder="������� �����">
...

-������ ���� �� ������ ����� �� ����������� � ��, �������� ��������������� � ������ ����� ��������� ����� �����
�����***********************************************************************************************************