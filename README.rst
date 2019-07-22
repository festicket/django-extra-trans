Install
-------

To install the demo project:

.. code:: shell

   make install python=python3.7

The command will create a virtual environment and install all the dependencies.

To run the demo project:

.. code:: shell

   . venv/bin/activate
   cd example
   python manage.py runserver


What inside
===========

The example project is a fake kind of ticketing application to illustrate usage of ``{% with_default_language %}``` template tag. It provides simplest `Order` model to hold various information about the purchase made by a user which then will be used to render tickets.

It also used to run tests which can be run via:

.. code:: shell

   make test-all


To get a list of all tickets, run the project and visit: http://127.0.0.1:8000/tickets/

You should see a list with at least two pre-generated tickets. Each ticket has its own language set. If you open non-English ticket you shall see that it has content in two languages rendered. This is the exact purpose of ``{% with_default_language %}`` tag.
