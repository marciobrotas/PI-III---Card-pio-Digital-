from django.urls import path
from . import views

urlpatterns = [
    path('foods/', views.foods_viwer, name='foods_viwer'),
]
