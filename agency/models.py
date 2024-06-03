from functools import total_ordering
from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# ������ ���������� ���������� � ������, � �������� �� ���������.
# ��� �������� ���� � ��������� ����� ������.
# ������ ���� ������ ������������ ���� ������� � ���� ������.
# ������ ������ ��� ����� �������������� �� django.db.models.Model.
# ������� ������ ������������ ���� � ���� ������.
# Django ������������� ������������� ��������� API ��� ������� � ������

# choices (������ ������). �������� (��������, ������ ��� ������) 2-� ���������� ��������,
# ������������ �������� �������� ��� ����.
# ��� �����������, ������ ����� ���������� select ������ ������������ ���������� ����
# � ��������� �������� ���� ���������� ����������.

# ����������� ��� ���� (�����, label). ������ ����, ����� ForeignKey, ManyToManyField � OneToOneField,
# ������ ���������� ��������� �������������� ����������� ��������.
# ���� ��� �� �������, Django �������������� ������� ���, ��������� �������� ����, ������� ������������� �� ������.
# null - ���� True, Django �������� ������ �������� ��� NULL � ���� ������. �� ��������� - False.
# blank - ���� True, ���� �� ����������� � ����� ���� ������. �� ��������� - False.
# ��� �� �� �� ��� � null. null ��������� � ���� ������, blank - � �������� ������.
# ���� ���� �������� blank=True, ����� �������� �������� ������ ��������.
# ��� blank=False - ���� �����������.

# ��������� ������ ������
class Category(models.Model):
    category_title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'category'
    def __str__(self):
        # ����� ��������� ��� SELECT 
        return "{}".format(self.category_title)

# ������ 
class Service(models.Model):
    category = models.ForeignKey(Category, related_name='service_category', on_delete=models.CASCADE)
    service_title = models.CharField(_('service_title'), max_length=256)
    details = models.TextField(_('service_details'))
    price = models.DecimalField(_('service_price'), max_digits=9, decimal_places=2)
    photo = models.ImageField(_('service_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'service'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['category', 'service_title']),
        ]
        # ���������� �� ���������
        ordering = ['service_title']
    def __str__(self):
        # ����� ������������� ������ 
        return "{}: {}".format(self.category, self.service_title)

# ������ �������
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    application_title = models.CharField(_('application_title'), max_length=256)
    application_details = models.TextField(_('application_details'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'application'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['user']),
        ]
        # ���������� �� ���������
        ordering = ['datea']
    def __str__(self):
        # ����� � ��� Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.user, self.application_title)

# ������������� �������������
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
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_application'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datea']),
        ]
        # ���������� �� ���������
        ordering = ['datea']
        # ������� �� ���� �� ��������� �� �������
        managed = False

# ������������ ������ �������
class Movement(models.Model):
    application = models.ForeignKey(Application, related_name='movement_application', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('datem'))
    status = models.CharField(_('movement_status'), max_length=128)
    details = models.TextField(_('movement_details'), blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'movement'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['datem']),
        ]
        # ���������� �� ���������
        ordering = ['datem']        
    def __str__(self):
        # ����� � ��� Select
        return "{} ({}): {}".format(self.datem.strftime('%d.%m.%Y'), self.application, self.status)

# ������� ����� �� ������ �������
class Sale(models.Model):
    application = models.ForeignKey(Application, related_name='sale_application', on_delete=models.CASCADE)
    dates = models.DateTimeField(_('dates'), auto_now_add=True)
    service = models.ForeignKey(Service, related_name='service_application', on_delete=models.CASCADE)
    payment = models.DecimalField(_('sale_payment'), max_digits=9, decimal_places=2)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'sale'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['dates']),
        ]
        # ���������� �� ���������
        ordering = ['dates']        
    def __str__(self):
        # ����� � ��� Select
        return "{} ({}): {}".format(self.dates.strftime('%d.%m.%Y'), self.application, self.service)

# ������� 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    news_title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'news'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['daten']),
        ]
        # ���������� �� ���������
        ordering = ['daten']
