from django.shortcuts import render, get_object_or_404

from .models import Product

def search(request):
    query = request.GET.get("query")
    if not query:
        products = Product.objects.order_by('?')[:12]
    else:
        products = Product.objects.filter(name__icontains=query)[:12]
    return render(request, "substitut_search/search.html", {"products": products})

def find(request):
    product_id = request.GET.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    substituts = []
    max_sbts = 12 # fichier de config?
    for category in reversed(product.categories):
        cat_sbts = Product.objects.filter(
            categories__contains=[category]).filter(
            nutriscore__lt=product.nutriscore).order_by('nutriscore')
        substituts += cat_sbts[:max_sbts-len(substituts)]
        if len(substituts) >= max_sbts:
            break

    # unorded_substitutes = []
    # for i in range(3):
    #     category = reversed(product.categories)
    #     point = abs(i-3)
    #     cat_sbts = Product.objects.filter(
    #         categories__contains=[category]).filter(
    #         nutriscore__lt=product.nutriscore)
    #     for e in cat_sbts:
    #         e_point = point + abs(ord(e.nutriscore)-(97+5))
    #         unorded_substitutes.append((e_point, e))
    # substituts = sorted(unorded_substitutes, reverse=True)[:max_sbts]
    context = {
    "initial_product": product,
    "products": substituts
    }
    return render(request, "substitut_search/find.html", context)

def detail(request):
    product_id = request.GET.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    return render(request, "substitut_search/detail.html", {"product": product})
