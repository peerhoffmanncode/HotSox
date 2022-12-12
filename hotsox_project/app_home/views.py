from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1>Well done, you see the Hot Sox HomePage !</h1>")
