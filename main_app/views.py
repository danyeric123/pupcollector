from main_app.forms import FeedingForm
from main_app.models import Pup, Toy
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

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
  
class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'
  
class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy
  
class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

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

def pups_detail(request, pup_id):
  pup = Pup.objects.get(id=pup_id)
  feeding_form = FeedingForm()
  return render(request, 'pups/detail.html', { 'pup': pup, 'feeding_form': feeding_form })

def add_feeding(request, pup_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the pup_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.pup_id = pup_id
    new_feeding.save()
  return redirect('pups_detail', pup_id=pup_id)