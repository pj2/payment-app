from django import forms
from .models import Transfer, Account


class TransferForm(forms.ModelForm):
    """Allows the creation of a transfer."""

    class Meta(object):
        model = Transfer
        fields = ['source', 'dest', 'amount']


class AccountForm(forms.ModelForm):
    """Allows the creation of a new account."""

    class Meta(object):
        model = Account
        fields = ['name', 'email']
