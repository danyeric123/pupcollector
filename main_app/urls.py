from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about,name='about'),
  path('pups/', views.pups_index, name='pups_index'),
  path('pups/<int:pup_id>',views.pups_detail,name='pups_detail'),
  path('pups/create/', views.PupCreate.as_view(), name='pups_create'),
  path('pups/<int:pk>/update/', views.PupUpdate.as_view(), name='pups_update'),
  path('pups/<int:pk>/delete/', views.PupDelete.as_view(), name='pups_delete'),
  path('pup/<int:pup_id>/add_feeding/', views.add_feeding, name='add_feeding'),
  path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
  path('toys/', views.ToyList.as_view(), name='toys_index'),
  path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
  path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
  path('pups/<int:pup_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
  path('pups/<int:pup_id>/remove_toy/<int:toy_id>/', views.remove_toy, name='remove_toy'),
  path('pups/<int:pup_id>/add_photo/', views.add_photo, name='add_photo'),
  path('accounts/signup/', views.signup, name='signup'),
]