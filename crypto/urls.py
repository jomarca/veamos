
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
    path('arbsbycoindown/',views.arborderbycoindown,name='arbsbycoindown'),
    path('arbsbycoinup/',views.arborderbycoinup,name='arborderbycoinup'),
    path('percentageup/',views.percentageup,name='percentageup'),
    path('arbsgreaterthan0/',views.arbsgreaterthan0,name='arbsgreaterthan0'),
    path('arbsgreaterthan1/',views.arbsgreaterthan1,name='arbsgreaterthan1'),
    path('arbsgreaterthan2/',views.arbsgreaterthan2,name='arbsgreaterthan2'),
    path('arbsgreaterthan5/',views.arbsgreaterthan5,name='arbsgreaterthan5'),
    path('manualreset/',views.manualreset,name='manualreset'),
    path('posttweet/',views.posttweet,name='posttweet'),
    
]
