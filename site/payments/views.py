from django.views.generic import ListView, DetailView, FormView
from . import models


class AccountList(ListView):
    """Shows a list of all accounts."""
    model = models.Account


class AccountDetail(DetailView):
    """Shows a single account and its transfers."""
    model = models.Account


class TransferDialog(FormView):
    """Allows the user to send money from one account to another."""
    pass
