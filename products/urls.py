from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from products.views import list_all, single_product, edit_product

urlpatterns = [
    path('', list_all, name="list_all_products"),
    path('<slug:slug>/edit/', edit_product, name="edit_product"),
    path('<slug:slug>/', single_product, name="single_product"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
