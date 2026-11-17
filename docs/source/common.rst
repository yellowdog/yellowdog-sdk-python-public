:mod:`yellowdog_client.common` -- Common
----------------------------------------
:mod:`yellowdog_client.common` contains the classes that the :mod:`yellowdog_client` services share, such as the
:class:`yellowdog_client.common.SearchClient` that each search returns.

.. module:: yellowdog_client.common

.. autoclass:: yellowdog_client.common.SearchClient
    :members:

.. autoclass:: yellowdog_client.common.SliceIterator
    :members:

.. autoclass:: yellowdog_client.common.server_sent_events.SubscriptionEventListener
    :members:

.. py:class:: Proxy
    :canonical: yellowdog_client.common.proxy.Proxy

    The base class of the service proxies, which send the services' requests to the YellowDog Platform.

.. autoclass:: yellowdog_client.common.server_sent_events.sse4python.EventSource()
