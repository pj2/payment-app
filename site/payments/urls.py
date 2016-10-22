from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transfer/', views.TransferDialog.as_view(), name='transfer'),
    url(r'^account/(?P<pk>[0-9]+)/', views.AccountDetail.as_view(), name='account_detail'),
    url(r'', views.AccountList.as_view(), name='account_list'),
]
