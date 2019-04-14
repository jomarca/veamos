
from . import views
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('create',views.create, name='create'),
    path('home1',views.home, name='home1'),
    path('<int:product_id>',views.detail,name='detail'),
    path('<int:product_id>/upvote',views.upvote,name='upvote'),
    path('search',views.search,name='search'),
    path('ordenardate',views.ordenardate,name='ordenardate'),
    path('ordenarname',views.ordenarname,name='ordenarname'),
    path('votes_total',views.votes_total,name='votes_total'),
    path('<int:pk>/update', views.UpdateProduct.as_view(), name='update_product'),
    path('<int:pk>/delete', views.DeleteProduct.as_view(), name='delete_product'),
    # path('<int:comment_id>/deletecomment', views.DeleteComment.as_view(), name='delete_comment'),
    #path('graph',views.testpandas,name='testpandas'),
    #path('<int:comment_id>',views.search,name='comment'),
    # path('<int:product_id>/<str:username_id>/upvote',views.upvote,name='upvote'),
]
