from django.urls import path
from . import views

urlpatterns = [
    path('', views.catch_all_view, name='catch_all'),
]
