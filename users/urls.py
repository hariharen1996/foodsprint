from django.urls import path,include
from .views import LoginView,CreateUserView

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('register/',CreateUserView.as_view(),name='register'),
]
