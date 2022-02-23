from django.http import HttpResponse, JsonResponse
from escpos.printer import Network, Serial, Usb
from apps.menu.models import Order
import json
from django.utils import timezone
import pdfkit
from django.shortcuts import render


def print_check(request, pk):
    company = 'APART HOTEL COSMOS'
    # company = 'CITYNET'
    try:
        order = Order.objects.get(id=pk)
    except Exception as e:
        return JsonResponse({'error': f'{e.args}'})
    else:
        items = order.order_items.all()
        context = {
            'company': company,
            'order_id': order.id,
            'order': order,

        }
        foods = []
        for i in items:
            foods.append({
                'meal': i.meal.title,
                'count': i.quantity,
                'price': i.price,
                'total_price': i.get_total,
            })
        context['foods'] = foods
        context['date'] = timezone.now()
        context['total'] = order.get_cart_total

        # f = open(f'media/check/order-{order_id}-{timezone.now()}', 'x')
        # f = write(
        #     f"""
        #     \n\t\t{company}\n
        #     {order} - {timezone.now().date()}\n

        #     """
        # )
        # pdfkit.from_url(f'http://bot.amspage.uz/print_check/{pk}/', f'media/check/out-{order.id}-{timezone.now()}.pdf')
        return render(request, 'menu/check.html', context)
        # return JsonResponse(context, safe=False, json_dumps_params={'ensure_ascii': False})

