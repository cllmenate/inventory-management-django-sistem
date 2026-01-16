from django.db.models import F, Sum
from django.utils import timezone
from django.utils.formats import number_format

from brands.models import Brand
from categories.models import Category
from outflows.models import Outflows
from products.models import Product


def get_product_metrics():
    products = Product.objects.all()

    total_products = sum(product.quantity for product in products)
    total_cost_price = sum(
        product.cost_price * product.quantity for product in products
    )
    total_sell_price = sum(
        product.sell_price * product.quantity for product in products
    )
    total_profit = total_sell_price - total_cost_price

    return dict(
        total_products=total_products,
        total_cost_price=number_format(
            total_cost_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        total_sell_price=number_format(
            total_sell_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        total_profit=number_format(
            total_profit,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
    )


def get_sales_metrics():
    total_sales = Outflows.objects.count()
    total_product_sold = (
        Outflows.objects.aggregate(total_product_sold=Sum("quantity"))[
            "total_product_sold"
        ]
        or 0
    )
    total_cost_price = sum(
        outflow.product.cost_price * outflow.quantity
        for outflow in Outflows.objects.all()
    )
    total_sell_price = sum(
        outflow.product.sell_price * outflow.quantity
        for outflow in Outflows.objects.all()
    )
    total_profit = total_sell_price - total_cost_price

    return dict(
        total_sales=total_sales,
        total_product_sold=total_product_sold,
        total_cost_price=number_format(
            total_cost_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        total_sell_price=number_format(
            total_sell_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        total_profit=number_format(
            total_profit,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
    )


def get_daily_sales_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(30, -1, -1)]
    values = list()

    for date in dates:
        sales_total = (
            Outflows.objects.filter(created_at__date=date).aggregate(
                total_sales=Sum(F("product__sell_price") * F("quantity"))
            )["total_sales"]
            or 0
        )
        values.append(float(sales_total))

    return dict(
        dates=dates,
        values=values,
    )


def get_daily_sales_quantity_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(30, -1, -1)]
    quantities = list()

    for date in dates:
        sales_quantity = Outflows.objects.filter(created_at__date=date).count()
        quantities.append(sales_quantity)

    return dict(
        dates=dates,
        values=quantities,
    )


def get_products_by_category():
    categories = Category.objects.all()
    return {
        category.name: Product.objects.filter(category=category).count()
        for category in categories
    }

    # return {
    #     category.name: Product.objects.filter(category=category).count()
    #     for category in categories
    # }


def get_products_by_brand():
    brands = Brand.objects.all()

    return {
        brand.name: Product.objects.filter(product_model__brand=brand).count()
        for brand in brands
    }
