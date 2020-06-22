from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.base import View
from .models import Product, Manufacturer, CPU, Category
from .forms import ReviewForm, RatingForm


# Create your views here.
class CategoryYear:
    def get_category(self):
        return Category.objects.all()

    def get_years(self):
        return Product.objects.filter(draft=False).values("year")


class ProdDelView(DeleteView):
    model = Product
    success_url = reverse_lazy("product_list")


class ProductView(CategoryYear, ListView):
    model = Product
    queryset = Product.objects.filter(draft=False)
    '''template_name = "products/product_list.html"'''


class ProductDetailView(CategoryYear, DetailView):
    model = Product
    slug_field = "url"
    template_name = "products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class AddReview(CategoryYear, View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


class ManufView(CategoryYear, DetailView):
    model = Manufacturer
    template_name = 'products/manufacturers.html'
    slug_field = "name"


class CpuView(CategoryYear, DetailView):
    model = CPU
    template_name = 'products/cpus.html'
    slug_field = "name"


class Search(CategoryYear, ListView):

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context


def favourite_post(request, id):
    prod = get_object_or_404(Product, id=id)
    if prod.favourite.filter(id=request.user.id).exists():
        prod.favourite.remove(request.user)
    else:
        prod.favourite.add(request.user)
    return HttpResponseRedirect(prod.get_absolute_url())


def post_favourite_list(request):
    user = request.user
    favourite_prod = user.favourite.all()
    context = {
        'favourite_prod': favourite_prod,
    }
    return render(request, 'products/prod_favourite_list.html', context)


class FilterProductView(CategoryYear, ListView):
    def get_queryset(self):
        try:
            return Product.objects.filter(year__in=self.request.GET.getlist("year"))
        except ValueError:
            return Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = self.request.GET.get("year")
        return context
