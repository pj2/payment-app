from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/', views.AccountList.as_view()),
    url(r'^/account/(?P<pk>[0-9]+)/', views.AccountDetail.as_view()),
    url(r'^/transfer/', views.TransferDialog.as_view()),
]
