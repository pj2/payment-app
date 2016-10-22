from django.views.generic import ListView, DetailView, FormView


class AccountList(ListView):
    """Shows a list of all accounts."""
    pass


class AccountDetail(DetailView):
    """Shows a single account and its transfers."""
    pass


class TransferDialog(FormView):
    """Allows the user to send money from one account to another."""
    pass
