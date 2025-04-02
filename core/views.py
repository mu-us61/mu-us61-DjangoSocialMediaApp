from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    # return HttpResponse(" <h1> Hello WORLD </h1>")
    return render(request, "index.html")
