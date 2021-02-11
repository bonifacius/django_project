Инструкция к созданию джанго приложения weather:

1. Подготовка*********************************************************************************

-Установка:

python -m pip install django

-Создаем requirements.txt:

pip freeze > requirements.txt

-создаем файл .gitignore

-Создаем проект:
django-admin startproject WeatherApp

-Создаем приложение:
python manage.py startapp weather


2. Настройка**********************************************************************************

-Регистририруем приложение в WeatherApp /settings.py -> INSTALLED_APPS
 прописываем в конце название своего приложения
-python manage.py migrate

-Создаем нового superuser: 

python manage.py createsuperuser

-Проверяем работу сайта:

python manage.py runserver

-переходим в urls.py, импортируем include.
Мы добавляем после path '' пустую строку ( это наша стартовая страница)
а посде include прописываем, что мы подключаем из 'weather.urls'  :

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls'))
]

-теперь переходим в /weather(наше приложение), создаем новый файл urls
переходим, добавляем:

from django.urls import path
# из текущей дериктории мы импортируем views
from . import views
urlpatterns = [
    path('admin/', views.index),
]


- создем папку weather_project/WeatherApp/weather/templates
внутри создаем папку /weather и в ней создаем /index.html
Получаем:

/WeatherApp/weather/templates/weather/index.html 

- открываем weather/views и добавляем:
(по умолчанию index ищеться в папке templates)

from django.shortcuts import render

def index(request):
    return render(request, 'weather/index.html')

-заускаем сервер и проверяем запустилися ли html

-Переходим на сайт бутстрапа/examples
выбираем шапку из шаблонов, копируем код и вставляем в index.html
меняем дизайн если надо или вставляем шаблон в body:

<div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-wgite border-bottom shadow-sm">
        <h5 class="h5 my-0 me-md-auto fw-normal">Ну, Погода!</h5>
        <nav class="my-2 my-md-0 me-md-3">
            <a class="p-2 text-dark" href="#">Главное</a>
            <a class="p-2 text-dark" href="#">Информация</a>
        </nav>
        <a class="btn btn-outline-primary" href="#">Sign up</a>
    </div>
    <div class="container">
        <div class="row">
            <div class="col-4 offset-1">
                <h1>Погода в вашем городе</h1>
                <form action="">
                    <label for="city">Город</label>
                    <input type="text" id="city" class="form-control" name="city" placeholder="Введите город">
                    <input type="submit" name="send" value="Узнать" class="mt-2 btn btn-danger">
                </form>
            </div>
            <div class="col-4 offset-1">
              <h1>Информация</h1>
              <div class="alert alert-danger">
                  Погода в Москве
              </div>
            </div>
        </div>
    </div>

3. API()*****************************************************************************************

-Переходим на сайт weather map, регистрируемся

- переходим в API keys
авторизуемся, заходим в api, current weather date, копируем 

Examples of API calls:

api.openweathermap.org/data/2.5/weather?q={}&appid={API key}

{API key} - вставляем вместо этого наш ключ
{} - сюда мы будем подставлять город

-добавляем во veiews:
import requests
from django.shortcuts import render

def index(request):
    appid = 'e0b416b5d62ff64362bf0c4238e0494e'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=' + appid

    city = 'London'
    res = requests.get(url.format(city)).json()
    print(res.text)
    return render(request, 'weather/index.html')

-Чтобы отправить запрос и получить ответ в формате json нужно установить модуль request()
 import requests

Делаем запрос к переменной url, с помощью функции format() вставляем переменную city в {} нашего url 
 res = requests.get(url.format(city))

print(res.text) - запускаем сервер и в термнале проверяем что получен текст в формате json

json() - позволяет превратить переменную res в словарь

В weather map в разделе API находим 

Fields in API response;
и ищем параметр main.temp Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.

добавляем в url после {}:
&units=metric


создаем словарь:
для 'temp' мы обращаемся к словарю res, по ключю "main" по ключю "temp"
city_info = {
	'city': city, 
	'temp': res["main"]["temp"],
	'icon': res["weather"][0]["icon"]
}
(смтрите, что запрашиваете! Если у weather сначала идет список в котором есть словарь. пишем [0] 
что бы запросить первый элемент в списке )
-Что бы передать данные в html шаблон:

создаем словарь 
context = {'info': city_info} и передаем как третий параметр в  index.html

return render(request, 'weather/index.html', context)

- Меняем в index.html:

<div class="col-4 offset-1">
              <h1>Информация</h1>
              <div class="alert alert-danger">
                  <b>Город:</b> {{ info.city }}<br>
                  <b>Температура:</b> {{ city.temp}}<sup>o</sup></br>
                  <img src="http://openweathermap.org/img/w/{{ city.icon}}.png" alt="Фото погоды" class="img-thumbnail">
                  
              </div>

В {} мы обращаемся к словарю context, ключу 'info' и значению которое нам надо


4. Модели()

Теперь заходим в models.py 
 и создаем новую модель(таблицу)

 class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

__str__ нужен что бы возвращать не объект, а само значение(название конкретного города)

-создаем миграции:         
python manage.py makemigration

-сохраняем миграции в базе данных

-добавляем в admin нашу модель(для отображения в админке)
сначала импортируем модель

from .models import City 

admin.site.register(City)

-Теперь нам надо выводить информацию о городах которые мы ищем

переходим во views:

импортируем:
from .models import City

в index() удаляем переменную city, вместо этого создаем:

cities = City.objects.all() (берем как бы все объекты из таблицы City)

-через цикл for прогоняем все данные из cities:
-Этот объект нужно добалять в список! Который мы будем передавать в шаблон(context = {'info': city_info})  
Создаем пустой список all_cities = []
и в цикле каждый раз нужно добавлять новый объект(all_cities.append(city_info))


def index(request):
    appid = 'e0b416b5d62ff64362bf0c4238e0494e'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    cities = City.objects.all()
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city)).json()
        city_info = {
            'city': city.name, (.name нужен что бы обращаться к атрибуту модели City)
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]
        }
        all_cities.append(city_info)

    context = {'info': city_info}

    return render(request, 'weather/index.html', context)

ВЫВОД по выводу объектов модели*****************************************************************

1. Мы выбираем все данные из таблицы (cities = City.objects.all())
2. Перебираем города циклом for и узнаем для каждого города погоду и перемещаем это в переменную  city_info
city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]

3. Записываем эти данные в массив:
...
all_cities = []
...
all_cities.append(city_info)

4. Массив all_cities передаем в словарь
	
	context = {'all_info': all_cities} 

5. А contex передаем как параметр 'all_info' в шаблон index.html  

6. переходим в index.html

перед <div class="alert alert-info"> и в конце этого блока прописываем:

{% for info in all_info %}
.....
{% endfor %}


5. Формы***********************************************************************

-В функции index() нужно проверить если ли пост запрос.()
в index.html добавляем method:"post"
...
<h1>Погода в вашем городе</h1>
                <form action="" method="post">
...
Когда мы будем нажимать на кнопку "Узнать"
...
 <input type="submit" name="send" value="Узнать" class="mt-2 btn btn-danger">
...
Будет происходить отправка данных по методу post
и в функции index() мы можем проверять: Если применяется метод пост мы можем получать эти данные, 
записать данные или перезагрузить страницу(submit делает это автоматически)
проверяем:

в index() пишем:

if(request.method=='POST')
	создаем объект в атрибуте передаются значения которые мы получаем от пользователя(название города)
	form = CityForm(requests.POST)
	теперь вызываем объект и сохраняем его в базу данных:
	form.save()

-Создаем еще один объект что бы очистить форму
Это делается для того что бы когда мы перезагрузим страницу, наша форма ввода города очистилась.
Если это не сделать, останутся старые введеные данные 
form = CityForm()



-создаем файл forms.py
открываем, прописываем:

from .models import City
from django.forms import ModelForm, TextInput

class CityForm(ModelForm):
	class Meta:
		model = City
		fields = ['name']


Переходим во views и импортируем:
from .forms import CityForm



