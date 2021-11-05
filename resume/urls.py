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
	#Dashboard and Landing Page Routes
	path('',views.base,name='base'),
	path('dashboard',views.home,name='home'),

	# Resume Routes
	path('resumes/', views.my_resumes, name='my-resumes'),
	path('templates/', views.templates, name='templates'),
	path('resume/create/',ResumeWizard.as_view(views.FORMS), name='create-resume'),
	path('edit/resume/<int:pk>/', views.ResumeWizard.as_view(views.FORMS), name='edit-resume'),
	path('delete/<int:pk>/', views.delete_resume, name='delete-resume'),
	path('resume/<int:pk>/choose/', views.choose, name='choose'),
	path('resume/<int:pk>/view-resume/', views.choose, name='view-resume'),

	# Login and Authentication Routes
	path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	path('edit-profile/', views.edit_profile, name='edit-profile'),
	path('register/', views.register, name='register'),
	path('accounts/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)