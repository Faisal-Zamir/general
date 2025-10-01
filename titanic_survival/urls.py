
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('', include('predictor.urls')),  # include predictor app's urls

]
