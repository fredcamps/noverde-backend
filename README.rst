==========================
NoVerde Back-end Challenge
==========================

Requirements
------------
 * Docker
 * docker-compose

How to run at first time
------------------------

.. code-block:: bash

   $ docker-compose up --build
   $ poetry run migrate
   $ poetry run python manage.py loaddata interest.json

.. _Docker: http://docs.docker.com/
.. _docker-compose: http://docs.docker.com/compose

How to access endpoints
-----------------------
