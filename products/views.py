from django.shortcuts import render

from .models import Product, ProductImage, Tag, Category, CategoryImage


def list_all(request):
    products = Product.objects.all()
    #images = ProductImage.objects.filter(product=product)
    template = "products/all.html"
    context = {
        "products": products,
        #'images': images,
    }
    return render(request, template, context)

def single_product(request, slug):
    template = "products/single.html"
    product = Product.objects.get(slug=slug)
    images = ProductImage.objects.filter(product=product)
    if request.user == product.user:
        cat = Category.objects.filter(product=product)
        context = {
            'product': product,
            'categories': cat,
            'images': images,
            'edit': True,
        }
    else:
        cat = Category.objects.filter(product=product)
        context = {
            'product': product,
        }

    return render(request, template, context)

def edit_product(request, slug):
    template = "products/edit.html"
    instance = Product.objects.get(slug=slug)
    images = ProductImage.objects.filter(product=instance)
    context = {
        'instance': instance,
        'images': images,
    }
    if request.user == instance.user:
        return render(request, template, context)
    else:
        raise Http404
