Getting Started
===============

To use this library to interface with the Reporter API, you first need to
instantiate a client. You will need to specify the URL to your Reporter
instance (e.g. ``https://reporter.example.com``) and your API token.

.. code:: python

   from reporter import Reporter
   rc = Reporter(url="https://reporter.example.com", api_token="secret")

You can now perform operations on the Reporter API, depending on the
permissions of your API token.

.. code:: python

   # Retrieve a user
   user = rc.users.list(filter_={"email": "researcher@example.com"})[0]

   # Retrieve a list of clients.
   clients = rc.clients.list()

   # Create an assessment under the first client.
   assessment = clients[0].assessments.create({
      "title": "My Awesome Assessment",
      "assessment_type_id": "owasp_top10_2021",
   })

   # Retrieve a list of assessment phases.
   phases = rc.assessments.get(assessment.id, include=["phases"])

   # Update an assessment phase.
   rc.assessment_phases.update(phases[0].id, {"researchers": [user.id]})

Requesting API Endpoints
------------------------

The capabilities of this library should correspond closely with those of the Reporter API itself. The capabilities of objects in
this library correspond directly to API endpoints. For example the endpoint :code:`GET api/v1/findings/{id}` allows you to retrieve a finding.
Requesting this endpoint using :code:`python-reporter` can be done as follows:

.. code:: python

   from reporter import Reporter
   rc = Reporter(url="https://reporter.example.com", api_token="secret")
   rc.findings.get(finding_id)

Some endpoints have query parameters, such as :code:`sort` and :code:`include`. You can pass these to the method calls
as arguments.

.. code:: python

   from reporter import Reporter
   rc = Reporter(url="https://reporter.example.com", api_token="secret")
   rc.findings.list(include=["targets", "user.documents"])



