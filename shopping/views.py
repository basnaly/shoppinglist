from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "shopping/index.html",{})