from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about,name='about'),
  path('pups/', views.pups_index, name='pups_index'),
  path('pups/<int:pk>',views.pups_detail,name='pups_detail')
]