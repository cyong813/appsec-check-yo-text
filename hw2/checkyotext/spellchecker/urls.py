from django.urls import include, path
from spellchecker import views

urlpatterns = [
    path('', views.HomePageView.as_view())
]
