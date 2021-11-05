from django.shortcuts import render
from mainapp.models import ProductCategory, Product
import os, json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


MODULE_DIR = os.path.dirname(__file__)


def products(request, category_id=None, page_id=1):
    # products = Product.objects.all()
    # categories = ProductCategory.objects.all()

    products = Product.objects.filter(category_id=category_id).select_related(
        'category') if category_id != None else Product.objects.all()

    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        "title": "Каталог",
        "products": products_paginator,
        "categories": ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/products.html', context)
