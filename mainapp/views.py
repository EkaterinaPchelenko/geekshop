from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from mainapp.models import ProductCategory, Product
import os, json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache


# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')

def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()

MODULE_DIR = os.path.dirname(__file__)

def get_link_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.all().select_related('category')
            cache.set(key, link_product)
        return link_product
    return Product.objects.all().select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    return get_object_or_404(Product, pk=pk)


def products(request, category_id=None, page_id=1):
    # products = Product.objects.all()
    # categories = ProductCategory.objects.all()

    # products = Product.objects.filter(category_id=category_id).select_related(
    #     'category') if category_id != None else Product.objects.all()

    products =get_link_product()

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
        "categories": get_link_category,
    }
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()

        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.all()
        return context