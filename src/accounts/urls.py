from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('create/', views.Create.as_view(), name='create'),
    path('delete/', views.Delete.as_view(), name='delete'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('settings/', views.Settings.as_view(), name='settings'),
]