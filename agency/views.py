from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Category, Service, Application, ViewApplication, Movement, Sale, News
# Подключение форм
from .forms import CategoryForm, ServiceForm, ApplicationForm, MovementForm, SaleForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        return render(request, "index.html")            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Отчеты
@login_required
@group_required("Managers")
def report_index(request):
    try:
        start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
        finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0).strftime('%Y-%m-%d')         
        application = ViewApplication.objects.all().order_by('datea')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по дате
                start_date = request.POST.get("start_date")
                #print(start_date)
                finish_date = request.POST.get("finish_date")
                finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
                application = ViewApplication.objects.filter(datea__range=[start_date, finish_date]).order_by('datea')                
                finish_date = request.POST.get("finish_date")
        return render(request, "report/index.html", {"application": application, "start_date": start_date, "finish_date": finish_date,  })    
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    try:
        category = Category.objects.all().order_by('category_title')
        return render(request, "category/index.html", {"category": category,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.category_title = request.POST.get("category_title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.category_title = request.POST.get("category_title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'category_title': category.category_title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def service_index(request):
    try:
        service = Service.objects.all().order_by('service_title')
        return render(request, "service/index.html", {"service": service,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def service_create(request):
    try:
        if request.method == "POST":
            service = Service()
            service.category = Category.objects.filter(id=request.POST.get("category")).first()
            service.service_title = request.POST.get("service_title")
            service.details = request.POST.get("details")
            service.price = request.POST.get("price")
            if "photo" in request.FILES:                
                service.photo = request.FILES["photo"]
            serviceform = ServiceForm(request.POST)
            if serviceform.is_valid():
                service.save()
                return HttpResponseRedirect(reverse('service_index'))
            else:
                return render(request, "service/create.html", {"form": serviceform})
        else:        
            serviceform = ServiceForm()
            return render(request, "service/create.html", {"form": serviceform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def service_edit(request, id):
    try:
        service = Service.objects.get(id=id)
        if request.method == "POST":
            service.category = Category.objects.filter(id=request.POST.get("category")).first()
            service.service_title = request.POST.get("service_title")
            service.details = request.POST.get("details")
            service.price = request.POST.get("price")
            if "photo" in request.FILES:                
                service.photo = request.FILES["photo"]
            serviceform = ServiceForm(request.POST)
            if serviceform.is_valid():
                service.save()
                return HttpResponseRedirect(reverse('service_index'))
            else:
                return render(request, "service/edit.html", {"form": serviceform})
        else:
            # Загрузка начальных данных
            serviceform = ServiceForm(initial={'category': service.category, 'service_title': service.service_title, 'details': service.details, 'price': service.price, 'photo': service.photo, })
            return render(request, "service/edit.html", {"form": serviceform})
    except Service.DoesNotExist:
        return HttpResponseNotFound("<h2>Service not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def service_delete(request, id):
    try:
        service = Service.objects.get(id=id)
        service.delete()
        return HttpResponseRedirect(reverse('service_index'))
    except Service.DoesNotExist:
        return HttpResponseNotFound("<h2>Service not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def service_read(request, id):
    try:
        service = Service.objects.get(id=id) 
        return render(request, "service/read.html", {"service": service})
    except Service.DoesNotExist:
        return HttpResponseNotFound("<h2>Service not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def application_index(request):
    try:
        application = ViewApplication.objects.all().order_by('datea')
        return render(request, "application/index.html", {"application": application})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список 
@login_required
def application_list(request):
    try:
        #print(request.user.id)
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        application = ViewApplication.objects.filter(user_id=request.user.id).order_by('-datea')
        return render(request, "application/list.html", {"application": application, 'first_name': first_name, 'last_name': last_name, 'email': email})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
#@group_required("Managers")
def application_create(request):
    try:
        if request.method == "POST":
            application = Application()
            application.user_id = request.user.id
            application.datea = datetime.now()
            application.application_title = request.POST.get("application_title")
            application.application_details = request.POST.get("application_details")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_list'))
            else:
                return render(request, "application/create.html", {"form": applicationform})
        else:        
            applicationform = ApplicationForm(initial={'dates': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "application/create.html", {"form": applicationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def application_edit(request, id):
    try:
        application = Application.objects.get(id=id) 
        if request.method == "POST":
            application.application_title = request.POST.get("application_title")
            application.application_details = request.POST.get("application_details")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/edit.html", {"form": applicationform})
        else:
            # Загрузка начальных данных
            applicationform = ApplicationForm(initial={'dates': application.dates.strftime('%Y-%m-%d'), 'application_title': application.application_title, 'application_details': application.application_details, })
            return render(request, "application/edit.html", {"form": applicationform})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def application_delete(request, id):
    try:
        application = Application.objects.get(id=id)
        application.delete()
        return HttpResponseRedirect(reverse('application_index'))
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def application_read(request, id):
    try:
        application = ViewApplication.objects.get(id=id)
        movement = Movement.objects.filter(application_id=id).order_by('-datem')
        sale = Sale.objects.filter(application_id=id).order_by('-dates')
        return render(request, "application/read.html", {"application": application, "movement": movement, "sale": sale})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def movement_index(request, application_id):
    try:
        movement = Movement.objects.filter(application_id=application_id).order_by('-datem')
        app = ViewApplication.objects.get(id=application_id)
        #movement = Movement.objects.all().order_by('-orders', '-datem')
        return render(request, "movement/index.html", {"movement": movement, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def movement_create(request, application_id):
    try:
        app = ViewApplication.objects.get(id=application_id)
        if request.method == "POST":
            movement = Movement()
            movement.application_id = application_id
            movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/create.html", {"form": movementform})
        else:
            movementform = MovementForm(initial={ 'datem': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "movement/create.html", {"form": movementform, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def movement_edit(request, id, application_id):
    app = ViewApplication.objects.get(id=application_id)
    try:
        movement = Movement.objects.get(id=id) 
        if request.method == "POST":
            #movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/edit.html", {"form": movementform})
        else:
            # Загрузка начальных данных
            movementform = MovementForm(initial={'application': movement.application, 'datem': movement.datem.strftime('%Y-%m-%d'), 'status': movement.status, 'details': movement.details,  })
            return render(request, "movement/edit.html", {"form": movementform, "application_id": application_id, "app": app})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def movement_delete(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id)
        movement.delete()
        return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def movement_read(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id) 
        return render(request, "movement/read.html", {"movement": movement, "application_id": application_id})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def sale_index(request, application_id):
    try:
        sale = Sale.objects.filter(application_id=application_id).order_by('-dates')
        app = ViewApplication.objects.get(id=application_id)
        #sale = Sale.objects.all().order_by('-orders', '-datem')
        return render(request, "sale/index.html", {"sale": sale, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def sale_create(request, application_id):
    try:
        app = ViewApplication.objects.get(id=application_id)
        if request.method == "POST":
            sale = Sale()
            sale.application_id = application_id
            sale.dates = datetime.now()
            sale.service = Service.objects.filter(id=request.POST.get("service")).first()
            sale.payment = request.POST.get("payment")
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index', args=(application_id,)))
            else:
                return render(request, "application/create.html", {"form": saleform})
        else:
            saleform = SaleForm(initial={ 'dates': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "sale/create.html", {"form": saleform, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def sale_edit(request, id, application_id):
    app = ViewApplication.objects.get(id=application_id)
    try:
        sale = Sale.objects.get(id=id) 
        if request.method == "POST":
            #sale.datem = datetime.now()
            sale.service = Service.objects.filter(id=request.POST.get("service")).first()
            sale.payment = request.POST.get("payment")
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index', args=(application_id,)))
            else:
                return render(request, "application/edit.html", {"form": saleform})
        else:
            # Загрузка начальных данных
            saleform = SaleForm(initial={'application': sale.application, 'datem': sale.datem.strftime('%Y-%m-%d'), 'service': sale.service, 'payment': sale.payment,  })
            return render(request, "sale/edit.html", {"form": saleform, "application_id": application_id, "app": app})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def sale_delete(request, id, application_id):
    try:
        sale = Sale.objects.get(id=id)
        sale.delete()
        return HttpResponseRedirect(reverse('sale_index', args=(application_id,)))
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def sale_read(request, id, application_id):
    try:
        sale = Sale.objects.get(id=id) 
        return render(request, "sale/read.html", {"sale": sale, "application_id": application_id})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по названию 
                news_search = request.POST.get("news_search")
                #print(news_search)                
                if news_search != '':
                    news = news.filter(Q(title__contains = news_search) | Q(details__contains = news_search)).all()                
                return render(request, "news/list.html", {"news": news, "news_search": news_search, })    
            else:          
                return render(request, "news/list.html", {"news": news})                 
        else:
            return render(request, "news/list.html", {"news": news}) 
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.news_title = request.POST.get("news_title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']   
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/create.html", {"form": newsform})
        else:        
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.news_title = request.POST.get("news_title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/edit.html", {"form": newsform})
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M:%S'), 'news_title': news.news_title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")


