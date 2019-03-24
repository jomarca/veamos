
from . import views
from django.urls import path, include


urlpatterns = [
    path('create',views.create, name='create'),
    path('home1',views.home, name='home1'),
    path('<int:product_id>',views.detail,name='detail'),
    path('<int:product_id>/upvote',views.upvote,name='upvote'),
    path('search',views.search,name='search'),
    # path('<int:product_id>/<str:username_id>/upvote',views.upvote,name='upvote'),
]
