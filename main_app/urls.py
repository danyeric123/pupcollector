from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about,name='about'),
  path('pups/', views.pups_index, name='pups_index'),
  path('pups/<int:pup_id>',views.pups_detail,name='pups_detail'),
  path('pups/create/', views.PupCreate.as_view(), name='pups_create'),
  path('pups/<int:pk>/update/', views.PupUpdate.as_view(), name='pups_update'),
  path('pups/<int:pk>/delete/', views.PupDelete.as_view(), name='pups_delete'),
  path('pup/<int:pup_id>/add_feeding/', views.add_feeding, name='add_feeding'),
]