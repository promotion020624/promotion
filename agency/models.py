from functools import total_ordering
from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Категория товара услуги
class Category(models.Model):
    category_title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'category'
    def __str__(self):
        # Вывод названияв тег SELECT 
        return "{}".format(self.category_title)

# Услуги 
class Service(models.Model):
    category = models.ForeignKey(Category, related_name='service_category', on_delete=models.CASCADE)
    service_title = models.CharField(_('service_title'), max_length=256)
    details = models.TextField(_('service_details'))
    price = models.DecimalField(_('service_price'), max_digits=9, decimal_places=2)
    photo = models.ImageField(_('service_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'service'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['category', 'service_title']),
        ]
        # Сортировка по умолчанию
        ordering = ['service_title']
    def __str__(self):
        # Вывод удобочитаемой строки 
        return "{}: {}".format(self.category, self.service_title)

# Заявка клиента
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    application_title = models.CharField(_('application_title'), max_length=256)
    application_details = models.TextField(_('application_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['user']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.user, self.application_title)

# Представление Заявкиклиента
class ViewApplication(models.Model):
    datea = models.DateTimeField(_('datea'))
    user_id = models.IntegerField(_('user_id'))
    username = models.CharField(_('username'), max_length=30)    
    first_name = models.CharField(_('first_name'), max_length=30)    
    last_name = models.CharField(_('last_name'), max_length=30)   
    email = models.CharField(_('email'), max_length=75)   
    application_title = models.CharField(_('application_title'), max_length=254)
    application_details = models.TextField(_('application_details'))
    final = models.CharField(_('final'), max_length=254)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']
        # Таблицу не надо не добавлять не удалять
        managed = False

# Рассмотрение заявки клиента
class Movement(models.Model):
    application = models.ForeignKey(Application, related_name='movement_application', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('datem'))
    status = models.CharField(_('movement_status'), max_length=128)
    details = models.TextField(_('movement_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'movement'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['datem']),
        ]
        # Сортировка по умолчанию
        ordering = ['datem']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datem.strftime('%d.%m.%Y'), self.application, self.status)

# Продажа услуг по заявке клиента
class Sale(models.Model):
    application = models.ForeignKey(Application, related_name='sale_application', on_delete=models.CASCADE)
    dates = models.DateTimeField(_('dates'), auto_now_add=True)
    service = models.ForeignKey(Service, related_name='service_application', on_delete=models.CASCADE)
    payment = models.DecimalField(_('sale_payment'), max_digits=9, decimal_places=2)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'sale'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['dates']),
        ]
        # Сортировка по умолчанию
        ordering = ['dates']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.dates.strftime('%d.%m.%Y'), self.application, self.service)

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    news_title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
