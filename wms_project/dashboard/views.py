from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.db.models import Sum, Count, F  # <-- shu yerga F qo‘shildi


from authentication import models
from inventory.models import StockMovement
from orders.models import Order
from products.models import Product
from suppliers.models import Restock



@login_required
def dashboard(request):
    # Get low stock products
    low_stock_products = Product.objects.filter(quantity__lte=F('low_stock_threshold'))

    # Get recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]

    # Get recent stock movements
    recent_movements = StockMovement.objects.order_by('-created_at')[:5]

    # Get pending restocks
    pending_restocks = Restock.objects.filter(status='PENDING')

    # Get sales data for chart (last 7 days)
    today = datetime.now().date()
    last_week = today - timedelta(days=6)

    sales_data = []
    for i in range(7):
        day = last_week + timedelta(days=i)
        day_orders = Order.objects.filter(created_at__date=day)
        day_total = day_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        sales_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'day': day.strftime('%a'),
            'total': float(day_total),
            'count': day_orders.count(),
        })

    # Get product category distribution for chart
    category_data = Product.objects.values('category__name').annotate(
        count=Count('id'),
        total_stock=Sum('quantity')
    ).order_by('-total_stock')

    context = {
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'recent_movements': recent_movements,
        'pending_restocks': pending_restocks,
        'sales_data': sales_data,
        'category_data': category_data,
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_stock_value': Product.objects.aggregate(
    total=Sum(F('price') * F('quantity'))  # to‘g‘ri
)['total'] or 0,

    }

    return render(request, 'index.html', context)