python-reporter
===============

A Python wrapper around the `Reporter <https://securityreporter.app>`_ API.

Getting Started
---------------

To use this library to interface with the Reporter API, you first need to
instantiate a client. You will need to specify the URL to your Reporter
instance (e.g. ``https://reporter.dongit.nl``) and your API token.

.. code:: python

   from reporter import Reporter
   rc = Reporter(url="https://reporter.dongit.nl", api_token="secret")

You can now perform operations on the Reporter API, depending on the
permissions of your API token.

.. code:: python

   # Retrieve a user
   user = rc.users.list(filter={"email": "researcher@example.com"})[0]

   # Retrieve a list of clients.
   clients = rc.clients.list()

   # Create an assessment under the first client.
   assessment = clients[0].assessments.create({
      "title": "My Awesome Assessment",
      "assessment_type_id": "owasp_top10_2021",
   })

   # Retrieve a list of assessment phases.
   phases = rc.assessments.get(assessmend.id, include=["phases"])

   # Update an assessment phase.
   rc.assessment_phases.update(phases[0].id, {"researchers": [user.id]})

See the API reference in the sidebar for more information. The capabilities of
this library should correspond closely with those of the Reporter API itself.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api-reference
   objects-list
