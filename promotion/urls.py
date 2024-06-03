"""
URL configuration for promotion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from agency import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('report/index/', views.report_index, name='report_index'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('category/index/', views.category_index, name='category_index'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/read/<int:id>/', views.category_read, name='category_read'),
    
    path('service/index/', views.service_index, name='service_index'),
    path('service/create/', views.service_create, name='service_create'),
    path('service/edit/<int:id>/', views.service_edit, name='service_edit'),
    path('service/delete/<int:id>/', views.service_delete, name='service_delete'),
    path('service/read/<int:id>/', views.service_read, name='service_read'),

    path('application/index/', views.application_index, name='application_index'),
    path('application/list/', views.application_list, name='application_list'),
    path('application/create/', views.application_create, name='application_create'),
    path('application/edit/<int:id>/', views.application_edit, name='application_edit'),
    path('application/delete/<int:id>/', views.application_delete, name='application_delete'),
    path('application/read/<int:id>/', views.application_read, name='application_read'),

    path('movement/index/<int:application_id>/', views.movement_index, name='movement_index'),
    path('movement/create/<int:application_id>/', views.movement_create, name='movement_create'),
    path('movement/edit/<int:id>/<int:application_id>/', views.movement_edit, name='movement_edit'),
    path('movement/delete/<int:id>/<int:application_id>/', views.movement_delete, name='movement_delete'),
    path('movement/read/<int:id>/<int:application_id>/', views.movement_read, name='movement_read'),

    path('sale/index/<int:application_id>/', views.sale_index, name='sale_index'),
    path('sale/create/<int:application_id>/', views.sale_create, name='sale_create'),
    path('sale/edit/<int:id>/<int:application_id>/', views.sale_edit, name='sale_edit'),
    path('sale/delete/<int:id>/<int:application_id>/', views.sale_delete, name='sale_delete'),
    path('sale/read/<int:id>/<int:application_id>/', views.sale_read, name='sale_read'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

