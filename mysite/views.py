from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from sem.models import User  
from django.http import HttpResponse

def login_view(request):
    return HttpResponse("This is the login page.")


def home(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def login_view(request):
    return HttpResponse("This is the login page.")

# Register API
@api_view(['POST'])
def register(request):
    mobile = request.data.get('mobile')
    password = request.data.get('password')

    if not mobile or not password:
        return Response({'error': 'Mobile number and password are required'}, status=400)

    if User.objects.filter(mobile=mobile).exists():


        return Response({'error': 'Mobile number already exists'}, status=400)

    user = User.objects.create_user(mobile=mobile, password=password)
    return Response({'message': 'User registered successfully'}, status=201)


@api_view(['POST'])
def api_login(request):  
    mobile = request.data.get('mobile')
    password = request.data.get('password')

    user = authenticate(request, mobile=mobile, password=password)
    if user:
        tokens = get_tokens_for_user(user)
        return Response(tokens)
    else:
        return Response({'error': 'Invalid Credentials'}, status=400)

# Protected API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view"})
@api_view(["POST"])
def register(request):
    return Response({"message": "User registered successfully"})


from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Hello from the sem app!")

from django.shortcuts import render

def register_view(request):
    return render(request, 'register.html')

def home(request):
    return render(request, 'index.html')  # Your main homepage

def create_account(request):
    return render(request, 'createaccount.html')  # File must exist

def forget_password(request):
    return render(request, 'forget.html')  # File must exist