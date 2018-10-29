from django.shortcuts import render
from django.http import HttpResponse

def index(req):
    return HttpResponse("<h1>Check your text</h1>")