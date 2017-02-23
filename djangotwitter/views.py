from django.shortcuts import render, redirect
import subprocess
import sys
import djangotwitter.singleton



# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'djangotwitter/index.html')

def startbot(reqest):
    djangotwitter.singleton.proc = subprocess.Popen([sys.executable, '/home/donne/WDI/Week 12/djangotwittersite/twitterBot.py'])
    # print(djangotwitter.singleton.proc)
    return redirect('index')

def stopbot(request):
    djangotwitter.singleton.proc.kill()
    return redirect('index')
#
#     print("This is proc kill: ", _local.proc)
#     print(_local)
#     _local.proc.kill()
#     return redirect('index')

# def submit(request):
#     startBot=request.POST['info']
#     # do something with info
