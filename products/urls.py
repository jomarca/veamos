
from . import views
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('create',views.create, name='create'),
    path('home1',views.home, name='home1'),
    path('<int:product_id>',views.detail,name='detail'),
    path('<int:product_id>/upvote',views.upvote,name='upvote'),
    path('search',views.search,name='search'),
    path('<int:pk>/update', views.UpdateProduct.as_view(), name='update_product'),
     path('<int:pk>/delete', views.DeleteProduct.as_view(), name='delete_product'),
    # path('<int:product_id>/<str:username_id>/upvote',views.upvote,name='upvote'),
]
