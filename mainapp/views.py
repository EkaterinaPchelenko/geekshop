from django.shortcuts import render
from mainapp.models import ProductCategory, Product
import os, json
# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


MODULE_DIR = os.path.dirname(__file__)


def products(request):
    context = {
        "title": "geekshop",
        "products": Product.objects.all(),
        "categories": ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/products.html', context)
