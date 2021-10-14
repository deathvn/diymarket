from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='market-index'),
    path('order/get', views.get_orders, name='get-orders'),
    path('order/create/', views.OrderCreate.as_view(), name='order-create'),
    path('order/delete/<str:pk>', views.OrderDelete.as_view(), name='order-delete'),
    path('matching/<str:type>', views.MatchbyUser.as_view(), name='matching-list-view'),
    path('matching/create/', views.OrderMatchingCreate.as_view(), name='matching-create'),
    path('matching/delete/<str:type>/<str:pk>/<str:st>', views.OrderMatchingDelete.as_view(), name='matching-delete'),
]
