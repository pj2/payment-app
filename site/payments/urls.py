from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AccountList.as_view(), name='account_list'),
    url(r'^transfers/new/$', views.TransferDialog.as_view(), name='transfer'),
    url(r'^accounts/new/$', views.CreateAccount.as_view(), name='create_account'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', views.AccountDetail.as_view(), name='account_detail'),
]
