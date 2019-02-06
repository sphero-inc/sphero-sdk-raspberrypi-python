====
Toys
====

In most instances, toys will have both an Asynchronous and a Blocking Implementation.

Toys with an Asynchronous implemenation require the use of an asyncio event loop, and all commands are called using ``await``

Toys with a Blocking implemenation can be called like regular functions, but block execution.

There are certain instances where information is common amongst implementations, and even amongst different toys. For example, the targets for a toy will be constant, regardless of implementation.  Similarly, certain enums are constant, regardless of toy.  See Common for that sort of information

.. toctree::
   _Common <toys_common>
   Asynchronous <toys_aio>
   Blocking <toys_blocking>
