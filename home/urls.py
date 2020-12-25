from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    path('referances/', views.referances, name='referances'),
    path('fag/', views.faq, name='fag'),
]