from main_app.forms import FeedingForm
from main_app.models import Pup, Toy, Photo
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('pups_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'
  
  
def about(request):
  return render(request, 'about.html')

class PupCreate(LoginRequiredMixin,CreateView):
  model = Pup
  fields = ['name', 'breed', 'description', 'age']
  success_url = '/pups/'
  
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  
class PupUpdate(LoginRequiredMixin,UpdateView):
  model = Pup
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class PupDelete(LoginRequiredMixin,DeleteView):
  model = Pup
  success_url = '/pups/'
  
class ToyCreate(LoginRequiredMixin,CreateView):
  model = Toy
  fields = '__all__'
  
class ToyList(LoginRequiredMixin,ListView):
  model = Toy
  
  # def get_queryset(self):
  #     queryset=Toy.objects.filter(pk=1)
  #     return queryset

class ToyDetail(LoginRequiredMixin,DetailView):
  model = Toy
  
class ToyUpdate(LoginRequiredMixin,UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin,DeleteView):
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

@login_required
def pups_index(request):
  pups = Pup.objects.filter(user=request.user)
  return render(request, 'pups/index.html', { 'pups': pups })

@login_required
def pups_detail(request, pup_id):
  pup = Pup.objects.get(id=pup_id)
  toys_pup_doesnt_have = Toy.objects.exclude(id__in = pup.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'pups/detail.html', { 'pup': pup, 'feeding_form': feeding_form, 'toys': toys_pup_doesnt_have})

@login_required
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

@login_required
def assoc_toy(request, pup_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Pup.objects.get(id=pup_id).toys.add(toy_id)
  return redirect('pups_detail', pup_id=pup_id)

@login_required
def remove_toy(request, pup_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Pup.objects.get(id=pup_id).toys.remove(toy_id)
  return redirect('pups_detail', pup_id=pup_id)

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'my-pup-collector'

@login_required
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