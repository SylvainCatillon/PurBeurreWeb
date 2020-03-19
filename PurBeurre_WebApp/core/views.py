from django.shortcuts import render

def index(request):
    """
    Display the home page

    Template: "core/index.html"
    """
    return render(request, "core/index.html")
