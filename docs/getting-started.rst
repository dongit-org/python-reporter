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
   finding = rc.findings.get(finding_id, include=["targets", "user.documents"], sort="title")
   print([t.name for t in finding.targets])
   # ["Acceptance Environment", "Production Environment"]

.. note::
   The query parameter :code:`filter` is called :code:`filter_` in python-reporter to avoid clashes with the
   :code:`filter` keyword, as prescribed in https://peps.python.org/pep-0008/#descriptive-naming-styles

The following demonstrates how to update a finding:

.. code:: python

   from reporter import Reporter
   rc = Reporter(url="https://reporter.example.com", api_token="secret")
   finding = rc.findings.list(filter_={"title": "Incoming Meteor"})[0]
   rc.findings.update(finding.id, {
       "risk": "This is a massive risk to the entire planet.",
       "targets": [target_id],
   }

Some endpoints, especially create ones, require the ID of a different type of object. For example
:code:`POST api/v1/clients/{client_id}/assessments` creates an assessment, but requires the ID of a client.
These endpoints must be called from the parent object.

.. code:: python

   from reporter import Reporter
   rc = Reporter(url="https://reporter.example.com", api_token="secret")
   client = rc.clients.get(client_id)
   client.assessments.create({
       "assessment_type_id": "owasp_top10_2021",
       "assessment_type_name": "OWASP Top 10 - version 2021",
       "title": "SuperApp periodic",
       "description": "White-box test",
   })

Some endpoints require you to upload files:

.. code:: python

   from reporter import Reporter
   rc = Reporter(url="https://reporter.example.com", api_token="secret")

   f = open(path, "rb")
   document = rc.documents.create(
       {
           "documentable_type": "User",
           "documentable_id": user.id,
           "section": "avatar",
       },
       file=f,
   )
