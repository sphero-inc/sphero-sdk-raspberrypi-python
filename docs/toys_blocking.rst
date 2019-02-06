============================
Blocking Toy Implementations
============================

Toys used here can be called directly, but will block.

:class:`BlockingSpheroRvr`
--------------------------

Use this Sphero RVR Implementation for Blocking Control

.. warning::

    All commands have a ``timeout`` parameter.  If set to ``None``, the commands will block until a response is received.  This means that they will block for-eve-r if no server can be reached.

.. autoclass:: spheroboros.BlockingSpheroRvr
    :members:
