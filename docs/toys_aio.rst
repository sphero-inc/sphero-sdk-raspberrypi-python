================================
Asynchronous Toy Implementations
================================

Toys used here must use an asyncio event loop!

.. warning::

    All commands have a ``timeout`` parameter.  If set to ``None``, the commands will block until a response is received.  This means that they will block for-eve-r if no server can be reached.

:class:`AsyncSpheroRvr`
-----------------------

Use this Sphero RVR Implementation for Asynchronous Control

.. autoclass:: spheroboros.AsyncSpheroRvr
    :members:
