from django.contrib import admin

from .models import  Category, Service, Application, Movement, Sale, News

# ���������� ������ �� ������� �������� ���������� ��������������
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Application)
admin.site.register(Movement)
admin.site.register(Sale)
admin.site.register(News)
