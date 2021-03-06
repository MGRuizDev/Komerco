from django.forms import ModelForm
from .models import Product, ProductImage

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'sale_price')

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('title', 'image', 'featured_image')
