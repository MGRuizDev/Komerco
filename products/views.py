from django.shortcuts import render, HttpResponseRedirect

from .models import Product, ProductImage, Tag, Category, CategoryImage
from .forms import ProductForm, ProductImageForm
from django.template.defaultfilters import slugify
from django.forms import modelformset_factory


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
    form = ProductForm(request.POST or None, instance = instance)
    context = {
        'instance': instance,
        'images': images,
        'form': form,
    }
    if request.user == instance.user:
        if form.is_valid():
            edited_form = form.save(commit = False)
            edited_form.save()
        return render(request, template, context)
    else:
        raise Http404

def add_product(request):
    template = "products/edit.html"
    form = ProductForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        product = form.save(commit = False)
        product.user = request.user
        product.slug = slugify(form.cleaned_data['title'])
        product.active = False
        product.save()
        return HttpResponseRedirect('/products/%s' %(product.slug))
    return render(request, template, context)

def manage_product_image(request, slug):
    template = "products/manage_images.html"
    try:
        product = Product.objects.get(slug=slug)
    except:
        product = False
    if request.user == product.user:
        queryset = ProductImage.objects.filter(product__slug = slug)
        ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, can_delete=True, extra=0)
        formset = ProductImageFormSet(request.POST or None, request.FILES or None, queryset = queryset)
        context = {
            'formset': formset,
            'product': product
        }
        if formset.is_valid():
            for form in formset:
                image = form.save(commit = False)
                image.save()
            if formset.deleted_forms:
                formset.save()
        return render(request, template, context)
    else:
        raise Http404
