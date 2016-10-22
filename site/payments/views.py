import logging
from smtplib import SMTPException
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from . import models, forms

logger = logging.getLogger(__name__)


class AccountList(ListView):
    """Shows a list of all accounts."""
    model = models.Account


class AccountDetail(DetailView):
    """Shows a single account and its transfers."""
    model = models.Account


class TransferDialog(CreateView):
    """Allows the user to send money from one account to another."""
    template_name = 'payments/create.html'
    form_class = forms.TransferForm
    success_url = reverse_lazy('payments:account_list')

    def form_valid(self, form):
        try:
            form.instance.notify_account_holders()
        except (IOError, SMTPException), e:
            logger.error('Failed to send transfer notification email', exc_info=e)

        data = form.cleaned_data
        messages.success(self.request,
            'Successfully transferred {0} to {1}.'.format(data['amount'], data['dest']))

        return super(TransferDialog, self).form_valid(form)


class CreateAccount(CreateView):
    """Allows the user to create an account."""
    template_name = 'payments/create.html'
    form_class = forms.AccountForm
    success_url = reverse_lazy('payments:account_list')
