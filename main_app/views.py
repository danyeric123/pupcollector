from main_app.models import Pup
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

class PupCreate(CreateView):
  model = Pup
  fields = ['name', 'breed', 'description', 'age']
  success_url = '/pups/'
  
class PupUpdate(UpdateView):
  model = Pup
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class PupDelete(DeleteView):
  model = Pup
  success_url = '/pups/'

# class Pup:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age

# pups = [
#   Pup('Lolo', 'tabby', 'Kinda rude.', 3),
#   Pup('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#   Pup('Fancy', 'bombay', 'Happy fluff ball.', 4),
# ]

def pups_index(request):
  pups = Pup.objects.all()
  return render(request, 'pups/index.html', { 'pups': pups })

def pups_detail(request, pk):
  pup = Pup.objects.get(id=pk)
  return render(request, 'pups/detail.html', { 'pup': pup })