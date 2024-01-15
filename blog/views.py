from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import BlogForm
from .models import Blog
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('blog')    
            except IntegrityError:
                 return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Useer already exists'
        })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })
@login_required
def blog(request):
    blog = Blog.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'blog.html', {'blog' : blog})

@login_required
def blog_completed(request):
    blog = Blog.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ('-datecompleted')
    return render(request,'blog.html', {'blog' : blog})

@login_required
def create_blog(request):
    if request.method == 'GET':
        return render(request, 'create_blog.html',{
            'form': BlogForm
        })
    else:
        try:
            form = BlogForm(request.POST)
            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.save()
            return redirect('blog')
        except ValueError: 
            return render(request, 'create_blog.html', {
                'form': BlogForm,
                'error': 'Please provide valide data'
        })

@login_required
def blog_detail(request, blog_id):
    if request.method == 'GET':
        blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
        form = BlogForm(instance=blog)
        return render(request, 'blog_detail.html', {'blog': blog, 'form': form })
    else:
       try:
            blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
            form= BlogForm(request.POST, instance=blog)
            form.save()
            return redirect('blog')
       except ValueError:
           return render(request, 'blog_detail.html', {'blog': blog, 'form': form, 
            'error': "Error updating blog"})

@login_required
def complete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        blog.datecompleted = timezone.now()
        blog.save()
        return redirect('blog')

@login_required    
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog')

@login_required
def sigout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
    })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('blog')

