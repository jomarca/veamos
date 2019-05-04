
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('prices/', views.prices, name="prices"),
    path('newsrepository/', views.newsrepository, name="newsrepository"),
    path('showdate',views.showdate,name='showdate'),
    path('searchcrypto',views.searchcrypto,name='searchcrypto'),
    path('searchanddate',views.searchanddate,name='searchanddate'),
    path('arbs/',views.cryptoarbs,name='cryptoarbs'),
    path('arbsdelete/',views.deletearbsfromdatabase,name='deletearbs'),
    
]
