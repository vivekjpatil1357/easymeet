from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import users, history
import pytz  # timezone india
from datetime import datetime, time, timedelta
# Create your views here.


def index(request):
    return render(request, 'vcall/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = users.objects.get(username=username)
        except:
            return render(request, 'vcall/login.html', {'error': 'Incorrect username or password. Please try again.'})
        if user is not None:
            if user.password == password:
                return redirect('home', user.username)
            else:
                return render(request, 'vcall/login.html')
        #     # return render(request, 'vcall/meet.html', {'username': username})
        else:
            return redirect('login')
    else:
        return render(request, 'vcall/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user = users.objects.create(username=username, first_name=first_name,
                                        last_name=last_name, email=email, password=password1)
            except:
                return render(request,'vcall/pricing.html',{'error':'Username already exist'})

            return redirect('login')
        else:
            
            return render(request,'vcall/pricing.html',{'error':'passwords not matching '})
    else:
        return render(request, 'vcall/pricing.html')


def userInfo(request, username):
    user = users.objects.get(username=username)
    if user is not None:
        h = history.objects.filter(user=user)

        return render(request, 'vcall/user_info.html', {'user': user, 'list': h})
    else:
        return render(request, 'vcall/user_info.html', {'error': 'error'})


def home(request, username):
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('link')
        temp = users.objects.filter(isactive=room_name)
        if len(temp) != 0:
            return render(request, 'vcall/meet.html', {'username': username, 'roomId': room_name})
        else:
            return render(request, 'vcall/services.html', {'username': username, 'error': 'Meeting is not yet started!! generate one to join'})
    else:
        exit = users.objects.get(username=username)
        exit.isactive = ''
        exit.save()
        return render(request, 'vcall/services.html', {'username': username, 'welcome': 'Welcome ,{}!'.format(username)})


def generate(request, username):
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('link')
        temp = users.objects.filter(isactive=room_name)
        if len(temp) == 0:
            r = users.objects.get(username=username)
            r.isactive = room_name
            r.save()
            india_timezone = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(india_timezone).time()
            join_time = current_time.strftime("%H:%M:%S")
            history.objects.create(
                user=r, join_time=join_time, meet_name=room_name)
            return render(request, 'vcall/meet.html', {'username': username, 'roomId': room_name})
        else:
            return render(request, 'vcall/generate.html', {'username': username, 'error': 'Name not available!!!'})
    else:
        exit = users.objects.get(username=username)
        if exit.isactive != '':
            exit.isactive = ''
            exit.save()
            h = history.objects.last()
            india_timezone = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(india_timezone).time()
            h.leave_time = str(current_time.strftime("%H:%M:%S"))
            v = str(h.join_time)
            time1 = datetime.strptime(v, "%H:%M:%S").time()
            time2 = datetime.strptime(h.leave_time, "%H:%M:%S").time()
            current_date = datetime.today().date()
            datetime1 = datetime.combine(current_date, time1)
            datetime2 = datetime.combine(current_date, time2)
            time_diff = datetime2 - datetime1
            min = format((time_diff.total_seconds()//60), '.0f')
            sec = format((time_diff.total_seconds() % 60), '.0f')
            final = min+" min"+sec+" sec"
            h.total_time = str(final)

            h.save()

        return render(request, 'vcall/generate.html', {'username': username})


def meet(request, username, roomId):
    h = history.objects.last()
    h.meet_name = roomId
    h.save()
    return render(request, 'vcall/meet.html', {'username': username, 'roomId': roomId})
