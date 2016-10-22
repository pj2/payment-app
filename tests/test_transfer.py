import mock
import pytest
from django.core import mail
from django.db import IntegrityError
from payments.models import Account, Transfer
from payments.forms import TransferForm


@pytest.fixture
def accounts():
    models = (
        Account(name='a', email='a@example.com', balance=200),
        Account(name='b', email='b@example.com', balance=200),
    )

    models[0].save()
    models[1].save()
    yield models
    models[0].delete()
    models[1].delete()


@pytest.mark.django_db
@pytest.mark.parametrize('amount', [100, 200, 0.01])
def test_allow_transfer(accounts, amount):
    """Allow valid transfer"""
    form = TransferForm({
        'source': accounts[0].pk,
        'dest': accounts[1].pk,
        'amount': amount,
    })

    assert form.is_valid()


@pytest.mark.django_db
def test_reject_transfer_to_self(accounts):
    """Reject transfer to my own account"""
    form = TransferForm({
        'source': accounts[0].pk,
        'dest': accounts[0].pk,
        'amount': 100,
    })

    assert not form.is_valid()


@pytest.mark.django_db
def test_reject_insufficient_funds(accounts):
    """Reject transfer if insufficient funds"""
    form = TransferForm({
        'source': accounts[0].pk,
        'dest': accounts[1].pk,
        'amount': 201,
    })

    assert not form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize('amount', [-100, 0])
def test_reject_invalid_amount(accounts, amount):
    """Reject transfer if the amount is invalid"""
    form = TransferForm({
        'source': accounts[0].pk,
        'dest': accounts[1].pk,
        'amount': amount,
    })

    assert not form.is_valid()


@pytest.mark.django_db
def test_reject_no_source(accounts):
    """Reject transfer if the source account is non-existent"""
    form = TransferForm({
        'source': 10000,
        'dest': accounts[1].pk,
        'amount': 100,
    })

    assert not form.is_valid()


@pytest.mark.django_db
def test_reject_no_dest(accounts):
    """Reject transfer if the destination account is non-existent"""
    form = TransferForm({
        'source': accounts[0].pk,
        'dest': 10000,
        'amount': 100,
    })

    assert not form.is_valid()


@pytest.mark.django_db
def test_applies_transfer(accounts):
    """Apply a transfer when the Transfer object is saved"""
    form = TransferForm({
        'source': accounts[0].pk,
        'dest': accounts[1].pk,
        'amount': 100,
    })
    transfer = form.save()

    assert transfer.source.balance == 100
    assert transfer.dest.balance == 300


@pytest.mark.django_db
def test_rollback(accounts):
    """Rollback if the transaction fails halfway"""
    try:
        transfer = Transfer(
            source=accounts[0],
            dest=accounts[1],
            amount=100,
        )

        # Cause an IntegrityError when updating dest...
        accounts[1].delete()
        accounts[1].pk = 10000
        transfer.save()
    except IntegrityError:
        transfer.source.refresh_from_db()
        assert transfer.source.balance == 200
    else:
        assert False, 'IntegrityError was not raised'


@pytest.mark.django_db
def test_send_email_to_source_and_dest(accounts, monkeypatch):
    """Send an email to the source and dest"""
    mock_send_mail = mock.Mock(return_value=ValueError)
    monkeypatch.setattr(mail, 'send_mail', mock_send_mail)

    transfer = Transfer(
        source=accounts[0],
        dest=accounts[1],
        amount=100,
    )
    transfer.save()
    transfer.notify_account_holders()

    assert mock.call_count == 2
