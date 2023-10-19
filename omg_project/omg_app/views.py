from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')

def chat(request):
    return render(request, 'chat.html')

def write(request):
    return render(request, 'write.html')

def loading(request):
    return render(request, 'loading.html')

def intro(request):
    return render(request, 'intro.html')

def login(request):
    return render(request, 'login.html')

def center_write(request):
    return render(request, 'center-write.html')

def center(request):
    return render(request, 'center.html')

def payment(request):
    return render(request, 'payment.html')