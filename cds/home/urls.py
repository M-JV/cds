from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('cancer/', views.cancer, name='cancer'),
    path('prediction/', views.prediction, name='prediction'),
]
