from django.db import models


class Account(models.Model):
    """A bank account."""

    name = models.StringField()
    balance = models.DecimalField(max_digits=30, decimal_places=2)
    email = models.EmailField()


class Transfer(models.Model):
    """A movement of funds from one account to another."""

    source = models.ForeignKey(Account)
    dest = models.ForeignKey(Account)
    amount = models.DecimalField(max_digits=30, decimal_places=2)
