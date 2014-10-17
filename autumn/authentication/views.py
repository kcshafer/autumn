from django.shortcuts import render
from django.http import HttpResponse

def handle_callback(request):
    print request
    return HttpResponse('success')