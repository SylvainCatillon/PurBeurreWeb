import requests

from django.db import IntegrityError, DataError, transaction

from ..models import Product


def trad(word):
    initial_words = [
        'saturated-fat', 'fat', 'sugars', 'salt',
        'low', 'moderate', 'high']
    trad_words = [
        'Acides gras saturés', 'Matières grasses','Sucres', 'Sel',
        'faible', 'modérée', 'élevée']
    return trad_words[initial_words.index(word)]

def get_nutrients(product):
    result = []
    for nutrient in ['fat', 'saturated-fat', 'sugars', 'salt']:
        try:
            level = product['nutrient_levels'][nutrient]
            quantity = product['nutriments'][nutrient+'_100g']
        except KeyError:
            continue
        # gerer string vide
        string = f"{trad(nutrient)} en quantitée {trad(level)} ({quantity}g)"
        result.append(string)
    return result

class FillDB:
    """Use this class to download products from fr.openfoodfacts.org
    and fill the database"""
    NB_PRODUCTS = 2223

    def __init__(self, nb_products=1000):
        self.nb_products = nb_products

    def dl_page(self, nb, page):
        payload = {
            "sort_by": "unique_scans_n",
            "action": "process",
            "json": 1,
            "page_size": nb,
            "page": page}
        raw_result = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl",
            params=payload)
        return raw_result.json()["products"]

    def dl_products(self):
        # while nb_products > 1000: req 1000 nb-=1000 page+=1
        products_list = []
        nb_products = self.nb_products
        page = 1
        while nb_products > 1000:
            products_list += self.dl_page(1000, page)
            page += 1
            nb_products -= 1000
        products_list += self.dl_page(nb_products, page)
        return products_list

    def insert_products(self):
        products_list = self.dl_products()
        for product in products_list:
            try:
                nutriscore = product["nutrition_grade_fr"].lower()
                categories = product["categories_tags"] # filtrer les cat qui commencent pas par en:?
                # if categories == []: raise KeyError
                name = product["product_name"].title()
                """# If there is brands indicated for the product, the first of
                    # them will be used to complement the name of the product
                    brands = product.get("brands")
                    if brands:
                        name += " " + brands.split(",")[0]"""
                link = product["url"]
                image = product["image_front_small_url"]
            except KeyError as error:
                #print(error)
                #print("The product doesn't contain the needed informations")
                continue
            nutrient_levels = get_nutrients(product)
            try:
                with transaction.atomic():
                    Product.objects.create(
                        nutriscore=nutriscore,
                        categories=categories,
                        name=name, link=link, image=image,
                        nutrient_levels=nutrient_levels)
            except (IntegrityError, DataError) as error:
                #print(error)
                continue
        #print(str(Product.objects.count())+" products in the database")
