payment-app
===========
Simple payments website.

To install the app:

    cd payment-app # From the root directory
    virtualenv env
    . env/bin/activate
    pip install .
    python site/manage.py migrate

To run the app:

    python site/manage.py runserver

Once the site is running, you may visit it at `http://127.0.0.1:8000/`. To
send email, please ensure there is a SMTP server configured to listen
on localhost:8025. You may use the following command:

    python -m smtpd -d -n localhost:8025

You can see the SMTP output to verify that emails were sent.

To run the tests:

    . env/bin/activate
    py.test
