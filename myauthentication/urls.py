from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.handleSignUp , name='handleSignUp'),
    path('login/',views.handeLogin , name='handleLogin'),
    path('logout/',views.handelLogout , name='handelLogout'),

    
]
