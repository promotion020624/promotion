from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput, CheckboxInput
from .models import Category, Service, Application, Movement, Sale, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.


# Категория товара
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_title',]
        widgets = {
            'category_title': TextInput(attrs={"size":"100"}),            
        }

# Услуги
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('category', 'service_title', 'details', 'photo', 'price')
        widgets = {
            'category': forms.Select(),
            'service_title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
        }
        labels = {
            'category': _('category_title'),            
        }

# Заявки
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('application_title', 'application_details', )
        widgets = {
            'application_title': TextInput(attrs={"size":"100"}),
            'application_details': Textarea(attrs={'cols': 100, 'rows': 10}),
        }        

# Движение заявки
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('datem', 'status', 'details')
        widgets = {
            'datem': DateInput(attrs={"type":"date", "readonly":"readonly"}),
            'status': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),
        }

# Продажа услуг по заявке клиента
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('service', 'payment')
        widgets = {
            'service': forms.Select(),
            'payment': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
        }
        labels = {
            'service': _('service_title'),            
        }

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'news_title', 'details', 'photo')
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'news_title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime.date) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
