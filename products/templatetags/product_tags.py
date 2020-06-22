from django import template
from products.models import Category, Product

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('products/tags/last_products.html')
def get_last_products():
    products = Product.objects.order_by("id")[:5]
    return {"last_products": products}
