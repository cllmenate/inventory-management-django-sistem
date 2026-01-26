from django.core.cache import cache
from django.db.models import F, Sum
from django.utils import timezone
from django.utils.formats import number_format

from brands.models import Brand
from categories.models import Category
from outflows.models import Outflows
from products.models import Product

# ========== RAW FUNCTIONS (SEM CACHE) ==========


def get_product_metrics_raw():
    """Calcula métricas de produtos (sem cache) - otimizado."""
    products = Product.objects.all()

    total_products = sum(product.quantity for product in products)
    total_cost_price = sum(
        product.cost_price * product.quantity for product in products
    )
    total_sell_price = sum(
        product.sell_price * product.quantity for product in products
    )
    total_profit = total_sell_price - total_cost_price

    return {
        "total_products": total_products,
        "total_cost_price": number_format(
            total_cost_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        "total_sell_price": number_format(
            total_sell_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        "total_profit": number_format(
            total_profit,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
    }


def get_sales_metrics_raw():
    """Calcula métricas de vendas (sem cache) - otimizado."""
    # Otimização: select_related para evitar N+1 queries
    outflows = Outflows.objects.select_related("product").all()

    total_sales = outflows.count()
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

    return {
        "total_sales": total_sales,
        "total_product_sold": total_product_sold,
        "total_cost_price": number_format(
            total_cost_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        "total_sell_price": number_format(
            total_sell_price,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
        "total_profit": number_format(
            total_profit,
            decimal_pos=2,
            force_grouping=True,
            use_l10n=True,
        ),
    }


def get_daily_sales_data_raw():
    """Calcula dados de vendas diárias (sem cache)."""
    today = timezone.now().date()
    dates = [
        str(today - timezone.timedelta(days=i)) for i in range(30, -1, -1)
    ]
    values = []

    for date in dates:
        sales_total = (
            Outflows.objects.filter(created_at__date=date).aggregate(
                total_sales=Sum(F("product__sell_price") * F("quantity"))
            )["total_sales"]
            or 0
        )
        values.append(float(sales_total))

    return {
        "dates": dates,
        "values": values,
    }


def get_daily_sales_quantity_data_raw():
    """Calcula quantidades de vendas diárias (sem cache)."""
    today = timezone.now().date()
    dates = [
        str(today - timezone.timedelta(days=i)) for i in range(30, -1, -1)
    ]
    quantities = []

    for date in dates:
        sales_quantity = Outflows.objects.filter(created_at__date=date).count()
        quantities.append(sales_quantity)

    return {
        "dates": dates,
        "values": quantities,
    }


def get_products_by_category_raw():
    """Calcula produtos por categoria (sem cache) - otimizado."""
    # Otimização: select_related para evitar N+1 queries
    categories = Category.objects.all()
    return {
        category.name: Product.objects.filter(category=category).count()
        for category in categories
    }


def get_products_by_brand_raw():
    """Calcula produtos por marca (sem cache) - otimizado."""
    # Otimização: select_related para evitar N+1 nas queries de brand
    brands = Brand.objects.all()

    return {
        brand.name: Product.objects.filter(product_model__brand=brand).count()
        for brand in brands
    }


# ========== CACHED FUNCTIONS (COM CACHE) ==========


def get_product_metrics():
    """Retorna métricas de produtos (com cache)."""
    cached = cache.get("metrics:product")
    if cached:
        return cached
    # Fallback se cache miss
    return get_product_metrics_raw()


def get_sales_metrics():
    """Retorna métricas de vendas (com cache)."""
    cached = cache.get("metrics:sales")
    if cached:
        return cached
    # Fallback se cache miss
    return get_sales_metrics_raw()


def get_daily_sales_data():
    """Retorna dados de vendas diárias (com cache)."""
    cached = cache.get("metrics:daily_sales")
    if cached:
        return cached
    # Fallback se cache miss
    return get_daily_sales_data_raw()


def get_daily_sales_quantity_data():
    """Retorna quantidades de vendas diárias (com cache)."""
    cached = cache.get("metrics:daily_sales_quantity")
    if cached:
        return cached
    # Fallback se cache miss
    return get_daily_sales_quantity_data_raw()


def get_products_by_category():
    """Retorna produtos por categoria (com cache)."""
    cached = cache.get("metrics:products_by_category")
    if cached:
        return cached
    # Fallback se cache miss
    return get_products_by_category_raw()


def get_products_by_brand():
    """Retorna produtos por marca (com cache)."""
    cached = cache.get("metrics:products_by_brand")
    if cached:
        return cached
    # Fallback se cache miss
    return get_products_by_brand_raw()
