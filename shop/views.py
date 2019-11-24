from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from .models import Category, Product

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

        context = {}
        context['category'] = category
        context['categories'] = categories
        context['products'] = products
        return render(request, 'product/list.html', context)
        
    context = {}
    context['categories'] = categories
    context['products'] = products
    return render(request, 'product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    context = {}
    context['product'] = product
    context['cart_product_form'] = cart_product_form
    return render(request, 'product/detail.html', context)