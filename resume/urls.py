from django.urls import path,include
from django.contrib import admin
from . import views
from .views import ResumeWizard

##User Authentications
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
	path('',views.home,name='home'),
	path('resume/create/',ResumeWizard.as_view(views.FORMS), name='create-resume'),
	path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	
	path('register/', views.register, name='register'),
	path('accounts/', include('allauth.urls')),
]
