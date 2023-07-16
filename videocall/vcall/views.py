from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import users

# Create your views here.


def index(request):
    return render(request, 'vcall/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = users.objects.get(username=username)
        if user is not None:
            if user.password == password:
                return redirect('home', username)
            else :
                return HttpResponse("password is wrong")
        #     # return render(request, 'vcall/meet.html', {'username': username})
        else:
            return redirect('login')
    else:
        return render(request, 'vcall/contact.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            users.objects.create(username=username, first_name=first_name,
                                 last_name=last_name, email=email, password=password1)
            return redirect('login')
        else:
            return render(request, 'vcall/register.html')
    else:
        return render(request, 'vcall/register.html')


def home(request, username):
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('link')
        temp = users.objects.filter(isactive=room_name)
        if len(temp)!=0:
            return render(request, 'vcall/meet.html', {'username': username, 'roomId': room_name})
        else:
            return render(request, 'vcall/home.html', {'username': username})
    else:
        exit=users.objects.get(username=username)
        exit.isactive=''
        exit.save()
        return render(request, 'vcall/home.html', {'username': username})


def generate(request, username):
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('link')
        temp = users.objects.filter(isactive=room_name)
        if len(temp)==0:
            r=users.objects.get(username=username)
            r.isactive=room_name
            r.save()
            return render(request, 'vcall/meet.html', {'username': username, 'roomId': room_name})
        else:
            return render(request, 'vcall/generate.html', {'username': username})
    else:
        exit=users.objects.get(username=username)
        exit.isactive=''
        exit.save()
        return render(request, 'vcall/generate.html', {'username': username})


def meet(request, username, roomId):
    return render(request, 'vcall/meet.html', {'username': username, 'roomId': roomId})
