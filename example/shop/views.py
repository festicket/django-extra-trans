from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import translation

from shop.models import Order, hashids


def tickets(request):
    return render(request, 'shop/ticket_list.html', context={
        'orders': Order.objects.all()
    })


def ticket_details(request, order_public_id):
    order_pk = hashids.decode(order_public_id)
    if not order_pk:
        raise Http404
    order = get_object_or_404(Order, pk=order_pk[0])
    with translation.override(order.language):
        return render(request, 'shop/ticket_details.html', context={
            'order': order,
        })