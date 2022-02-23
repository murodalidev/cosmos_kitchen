import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.menu.models import Order
from django.db.models import Q
from datetime import datetime


def order_list(request):
    today = datetime.now().date()
    orders = Order.objects.filter(Q(status=1) & Q(updated_at__date=today))
    status = request.GET.get('status')
    context = {}
    if status:
        try:
            status = int(status)
        except:
            return redirect('/?status=1')
        else:
            if status == 0:
                orders = Order.objects.filter(updated_at__date=today).order_by('-updated_at')
                context['orders'] = orders
            if status == 1:
                orders = Order.objects.filter(updated_at__date=today).order_by('updated_at')
                context['orders'] = orders
            if status == 2:
                orders = Order.objects.filter(updated_at__date=today).order_by('-updated_at')
            if status >= 3:
                orders = Order.objects.filter(updated_at__date=today).order_by('-updated_at')
                context['orders'] = orders
            else:
                orders = Order.objects.filter(Q(status=status) & Q(updated_at__date=today))
                context['orders'] = orders

    context = {'orders': orders.order_by('updated_at')}
    return render(request, 'menu/index.html', context)


def payment_type(request):
    
    pk = request.GET.get('id')
    payment_type = request.GET.get('payment_type')
    order = Order.objects.get(id=pk)
    order.payed = payment_type
    order.save()
    messages.success(request, 'success')
    return redirect('/?status=0')
    


def complete_order(request):
    pk = request.GET.get('pk')

    try:
        order = Order.objects.get(id=pk)
    except Exception as e:
        messages.error(request, f'Error: {e.args}')
        return redirect('/?status=0')
    else:
        order.status = 0
        order_items = order.order_items.all()
        for item in order_items:
            item.is_completed = True
            item.save()
        order.save()
    return redirect('/?status=1')


def pending_order(request):
    pk = request.GET.get('pk')

    try:
        order = Order.objects.get(id=pk)
    except Exception as e:
        messages.error(request, f'Error: {e.args}')
        return redirect('/?status=1')
    else:
        order_items = order.order_items.all()
        for item in order_items:
            item.is_completed = False
            item.save()
        order.status = 1
        order.save()
    return redirect('/?status=1')


def cancel_order(request):
    pk = request.GET.get('pk')

    try:
        order = Order.objects.get(id=pk)
    except Exception as e:
        messages.error(request, f'Error: {e.args}')
        return redirect('/?status=2')
    else:
        order_items = order.order_items.all()
        for item in order_items:
            item.is_completed = False
            item.save()
        order.status = 2
        order.save()
    return redirect('/?status=1')
