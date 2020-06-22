from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name="product_list"),
    path("filter/", views.FilterProductView.as_view(), name="filter"),
    path("search/", views.Search.as_view(), name="search"),

    url(r"favourites/$", views.post_favourite_list, name='post_favourite_list'),
    url(r"(?P<id>\d+)/favourite_post/$", views.favourite_post, name='favourite_post'),

    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    url(r"product(?P<pk>[0-9]+)/delete/$", views.ProdDelView.as_view(), name='prod_delete'),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("manufacturers/<str:slug>/", views.ManufView.as_view(), name="manufacturers_detail"),
    path("cpus/<str:slug>/", views.CpuView.as_view(), name="cpus_detail"),
]
