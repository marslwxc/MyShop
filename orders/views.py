from django.shortcuts import render, redirect
from django.urls import reverse

from cart.models import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, \
                                        product=item['product'], \
                                        price=item['price'], \
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    
    context = {}
    context['cart'] = cart
    context['form'] = form
    return render(request, 'orders/order/create.html', context)