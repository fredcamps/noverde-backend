==========================
NoVerde Back-end Challenge
==========================

Requirements
------------
 * Docker_
 * docker-compose_

.. _Docker: http://docs.docker.com/
.. _docker-compose: http://docs.docker.com/compose

How to run at first time
------------------------

.. code-block:: bash

   $ echo "EXTERNAL_API_TOKEN='<token-sent-by-email-here>'" >> vars.env
   $ docker-compose up --build
   $ poetry run python manage.py migrate
   $ poetry run python manage.py loaddata interest.json

How to access endpoints
-----------------------
