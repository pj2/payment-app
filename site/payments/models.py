from django.db import models


class Account(models.Model):
    """A bank account."""

    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=200)
    email = models.EmailField()


class Transfer(models.Model):
    """A movement of funds from one account to another."""

    source = models.ForeignKey(Account, related_name='sent_transfers')
    dest = models.ForeignKey(Account, related_name='received_transfers')
    amount = models.DecimalField(max_digits=30, decimal_places=2)
