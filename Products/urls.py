from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('products',views.products,name='products'),
    path('contents/<str:pk>/', views.contents, name='contents'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.login, name='login'),
    
    # REST
    # path('api/',views.apiOverview,name='api'),
    # path('api/content-list/',views.contentlist,name='cl'),
    path('api/item-detail/<str:pk>',views.itemdetail,name='item-detail'),
    path('api/content-detail/<str:pk>',views.contentdetail,name='content-detail'),
    path('api/content-id/',views.contentid,name='content-id'),
    path('get_content/',views.get_content,name='get_content'),
    
    
]