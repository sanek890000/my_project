from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

def page1(request):
    return HttpResponse("Welcome to Page 1")

def page2(request):
    return HttpResponse("Welcome to Page 2")
