from django.urls import path
from .views  import *
urlpatterns = [
    path('',index,name="index"),
    path('login/',login,name='login'),
    path('home/<username>',home,name='home'),
    path('generate/<username>',generate,name='generate'),
    path('meet/<str:username>/<str:link>',meet,name='meet'),
    path('user_register/',user_register,name='user_register'),
    path('user_info/<username>',userInfo,name='user_info')
]
