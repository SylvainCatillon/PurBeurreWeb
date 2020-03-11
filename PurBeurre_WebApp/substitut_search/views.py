from django.shortcuts import render

from .models import Product

def search(request):
    query = request.GET.get("query")
    if not query:
        products = Product.objects.order_by('?')[:12]
    else:
        products = Product.objects.filter(name__icontains=query)[:12]
    return render(request, "substitut_search/search.html", {"products": products})
