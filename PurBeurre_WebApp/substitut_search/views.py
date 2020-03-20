from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden

from .models import Product

NB_DISPLAYED_PRODUCTS = 12

def search(request):
    """
    Takes a request GET with a query
    Displays products whose name contains the query
    Displays 12 random products if the query is empty

    Template: "substitut_search/search.html"
    Context: {"products": a list of products, "query": the initial query}
    """
    query = request.GET.get("query")
    if not query:
        query = "Produits aléatoires"
        products = Product.objects.order_by('?')[:NB_DISPLAYED_PRODUCTS]
    else:
        products = Product.objects.filter(
            name__icontains=query)[:NB_DISPLAYED_PRODUCTS]
    context = {"products": products, "query": query}
    return render(request, "substitut_search/search.html", context)

def find(request):
    """
    Takes a request GET with a product id
    Displays substituts to the initial product

    Template: "substitut_search/find.html"
    Context: {
        "initial_product": the product in the initial search,
        "products": a list of the products found as substituts}
    """
    product_id = request.GET.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    substituts = []
    max_sbts = NB_DISPLAYED_PRODUCTS
    #  search in categories, starting from the smaller
    #  until enough substituts are found
    for category in reversed(product.categories):
        #  find the products in the category with a better nutriscore
        cat_sbts = Product.objects \
                          .filter(categories__contains=[category]) \
                          .filter(nutriscore__lt=product.nutriscore) \
                          .order_by('nutriscore')
        #  add the products in the result list, without exceed the max
        substituts += cat_sbts[:max_sbts-len(substituts)]
        #  if the result list have enough products, end the search
        if len(substituts) >= max_sbts:
            break
    context = {
        "initial_product": product,
        "products": substituts
        }
    return render(request, "substitut_search/find.html", context)

def detail(request):
    """
    Takes a request GET with a product id
    Displays the informations of the product

    Template: "substitut_search/detail.html"
    Context: {"product": the searched product}
    """
    product_id = request.GET.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    return render(request, "substitut_search/detail.html", {"product": product})

def favories(request):
    """
    Takes a request GET or POST with a product id
    If the method is POST, save the product in the user favories
    Else, displays the saved products of the user

    Template: "substitut_search/favories.html"
    Context: {"products": a list of the products saved by the user}
    """
    user = request.user
    #  a user need to be authenticated to access this page
    if not user.is_authenticated:
        return HttpResponseForbidden()
    #  if the request method is POST, save the product in the user favories
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        user.profile.favories.add(product)
        #  return an HttpResponse which will be displayed by a jquerry script
        return HttpResponse("Produit sauvegardé")
    #  if the method isn't POST, display the saved products of the user
    products = user.profile.favories.all()
    return render(
        request, "substitut_search/favories.html", {'products': products})
