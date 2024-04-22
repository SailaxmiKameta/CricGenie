from django.shortcuts import render, redirect
import requests

def home(request):
    return  render(request, 'home.html', {})
