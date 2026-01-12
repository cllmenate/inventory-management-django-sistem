import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app import metrics


@login_required(login_url='login')
def home(request):
    product_metrics = metrics.get_product_metrics()
    sales_metrics = metrics.get_sales_metrics()
    daily_sales_data = metrics.get_daily_sales_data()
    daily_sales_quantity_data = metrics.get_daily_sales_quantity_data()
    products_by_category = metrics.get_products_by_category()
    products_by_brand = metrics.get_products_by_brand()

    context = {
        'product_metrics': product_metrics,
        'sales_metrics': sales_metrics,
        'daily_sales_data': json.dumps(daily_sales_data),
        'daily_sales_quantity_data': json.dumps(daily_sales_quantity_data),
        'products_by_category': json.dumps(products_by_category),
        'products_by_brand': json.dumps(products_by_brand),
    }

    return render(request, 'home.html', context)
