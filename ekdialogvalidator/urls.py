from django.contrib import admin
from django.urls import path
from ekdialogvalidator import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dialog/', views.index),
    path('home/', views.home, name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)