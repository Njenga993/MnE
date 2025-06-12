from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def html_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard-home')  # Make sure this route exists in your urls.py

    error = None

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard-home')  # Make sure this matches your dashboard URL name
        else:
            error = "Invalid username or password."

    return render(request, "Login.html", {"error": error})

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        # registration logic
        return JsonResponse({"message": "User registered"})
    elif request.method == "GET":
        return JsonResponse({"message": "Please POST user data to register"})
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/api/v1/dashboard/')  # Change if needed
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def get_profile(request):
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username, 'email': request.user.email})
    return JsonResponse({'error': 'User not authenticated'}, status=403)
