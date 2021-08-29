from main_app.forms import FeedingForm
from main_app.models import Pup, Toy, Photo
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3

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
  toys_pup_doesnt_have = Toy.objects.exclude(id__in = pup.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'pups/detail.html', { 'pup': pup, 'feeding_form': feeding_form, 'toys': toys_pup_doesnt_have})

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

def assoc_toy(request, pup_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Pup.objects.get(id=pup_id).toys.add(toy_id)
  return redirect('pups_detail', pup_id=pup_id)

def remove_toy(request, pup_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Pup.objects.get(id=pup_id).toys.remove(toy_id)
  return redirect('pups_detail', pup_id=pup_id)

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'my-pup-collector'


def add_photo(request, pup_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      photo = Photo(url=url, pup_id=pup_id)
      # Remove old photo if it exists
      pup_photo = Photo.objects.filter(pup_id=pup_id)
      if pup_photo.first():
        pup_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('pups_detail', pup_id=pup_id)