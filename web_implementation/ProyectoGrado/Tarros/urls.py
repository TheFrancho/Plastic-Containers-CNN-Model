from django.urls import path, include

from .views import TestImage

urlpatterns = [
    path('test', TestImage.as_view()),
]
