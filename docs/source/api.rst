.. yellowdog-sdk-api:

====================
yellowdog-sdk API
====================

.. testsetup:: *

    import yellowdog_client

.. contents::

:mod:`yellowdog_client` -- Platform Client
==========================================

:class:`yellowdog_client.PlatformClient` is the main class, which is used to access various YellowDog services. When created with a provided configuration, the user can utilize:

- Compute service
- Account service
- Scheduler service
- Object store service

.. autoclass:: yellowdog_client.PlatformClient
    :members:
    :undoc-members:


YellowDog services
---------------------------------------------------
.. toctree::

   compute
   scheduler
   account
   images
   object_store
   usage
   model
