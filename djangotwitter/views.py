from django.shortcuts import render, redirect
import subprocess
import sys

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'djangotwitter/index.html')

def startbot(reqest):
    proc = subprocess.Popen([sys.executable, '/home/donne/WDI/Week 12/djangotwittersite/twitterBot.py'])
    return redirect('index')

def stopbot(request):
    proc.kill()
    return redirect('index')

# def submit(request):
#     startBot=request.POST['info']
#     # do something with info
