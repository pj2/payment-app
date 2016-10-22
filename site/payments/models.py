import decimal
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.core import mail
from django.db import models, transaction, IntegrityError
from django.db.models import F
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    """A bank account."""
    name = models.CharField(max_length=200)
    balance = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        default=200,
        editable=False,
    )
    email = models.EmailField(unique=True)

    def transfers(self):
        """Return a queryset which contains all transfers made
        by this account."""
        return self.sent_transfers.all() | self.received_transfers.all()

    def __str__(self):
        """Return the model's human-readable representation."""
        return self.name


class Transfer(models.Model):
    """A movement of funds from one account to another."""
    class Meta(object):
        ordering = ('-sent_at',)

    source = models.ForeignKey(
        Account,
        related_name='sent_transfers',
        verbose_name=_('From'),
    )
    dest = models.ForeignKey(
        Account,
        related_name='received_transfers',
        verbose_name=_('To'),
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        validators=[MinValueValidator(decimal.Decimal('0.01'))],
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate the model as a whole."""
        try:
            if self.source == self.dest:
                raise ValidationError(
                    _('The source account cannot be the destination.'))

            # Disclaimer: should be checked at database level
            if self.source.balance - self.amount < 0:
                raise ValidationError(
                    _('There are not enough funds available to transfer.'))
        except ObjectDoesNotExist:
            pass # These checks only apply if there are two valid related objects
                 # Pass to allow clean_fields to invalidate the form

        super(Transfer, self).clean()

    def save(self, *args, **kwargs):
        """Commit the model to the database. Transfers may only be saved once.

        The save causes an atomic transaction which transfers the funds and
        commits the transfer record.

        Raises IntegrityError iff one of the accounts no longer exists."""
        # Disclaimer: this check is a race-condition
        if self.pk is not None:
            raise ValueError('Transfer can be saved once only')

        with transaction.atomic():
            # Commit the new account balances and transfer object
            i = 0
            i += Account.objects.filter(pk=self.source_id).update(
                balance=F('balance') - self.amount)
            i += Account.objects.filter(pk=self.dest_id).update(
                balance=F('balance') + self.amount)

            if i != 2:
                raise IntegrityError()

            super(Transfer, self).save(*args, **kwargs)

        self.source.refresh_from_db(fields=['balance'])
        self.dest.refresh_from_db(fields=['balance'])

    def notify_account_holders(self):
        """Send an email to the holders of both accounts summarizing the
        transfer."""
        sender = 'noreply@example.com'
        message_1 = 'You sent {0} to {1}'.format(self.amount, self.dest)
        message_2 = '{0} sent you {1}'.format(self.source, self.amount)

        mail.send_mail(message_1, message_1, sender, [self.source.email])
        mail.send_mail(message_2, message_2, sender, [self.dest.email])
