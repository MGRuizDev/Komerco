from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import Product, ProductImage, Tag, Category, CategoryImage


class TagInline(admin.TabularInline):
    prepopulated_fields = {"slug":('tag',)}
    model = Tag

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "current_price", "categories")
    search_fields = ["title", "price", "category__title"]
    list_filter = ["title", "description", "price"]
    prepopulated_fields = {"slug":('title',)}
    inlines = [TagInline, ProductImageInline]
    readonly_fields = ['categories', 'timestamp', 'updated']
    class Meta:
        model = Product

    def current_price(self, obj):
        if obj.sale_price > 0:
            return obj.sale_price
        else:
            return obj.price

    def categories(self, obj):
        cat = []
        for i in obj.category_set.all():
            cat.append(i.title)
        return ", ".join(cat)

    categories.allow_tags=True

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":('title',)}
    inlines = [CategoryImageInline]
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)
