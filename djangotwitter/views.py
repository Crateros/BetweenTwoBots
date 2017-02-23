from django.shortcuts import render, redirect
import subprocess
import sys
import djangotwitter.singleton



# Create your views here.
def index(request):
    return render(request, 'djangotwitter/index.html')

def startbot(reqest):
    djangotwitter.singleton.proc = subprocess.Popen([sys.executable, '/home/donne/WDI/Week 12/djangotwittersite/twitterBot.py'])
    # print(djangotwitter.singleton.proc)
    return redirect('index')

def stopbot(request):
    djangotwitter.singleton.proc.kill()
    return redirect('index')

def about(request):
    return render(request, 'djangotwitter/about.html')
