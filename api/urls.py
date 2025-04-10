from home.views import *
from django.urls import path,include


urlpatterns = [
path('animals/',AnimalView.as_view()),
path('animal/<pk>/',AnimalDetailView.as_view()),
path('register/',RegisterAPI.as_view()),
path('login/',LoginAPI.as_view()),
path('animalcreate/',AnimalCreateAPI.as_view()),
path('animalupdate/',AnimalCreateAPI.as_view())

]