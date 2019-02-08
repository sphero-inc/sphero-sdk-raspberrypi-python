===========
Quick Start
===========

---------------------------------
Sending Commands to Sphero Robots
---------------------------------
There are two ways to send commands to Sphero Robots:

^^^^^^^^^^^
1. Blocking
^^^^^^^^^^^

.. code-block:: python

   from spheroboros import BlockingSpheroRvr

   rvr = BlockingSpheroRvr()

   # Get the FW Version of the Nordic Processor
   major, minor, revision = rvr.get_main_application_version(target=1)
   print("{}.{}.{}".format(major, minor, revision))

^^^^^^^^^^^^^^^
2. Asynchronous
^^^^^^^^^^^^^^^
.. code-block:: python

   import asyncio
   from spheroboros import AsyncSpheroRvr

   loop = asyncio.get_event_loop()

   rvr = AsyncSpheroRvr()

   async def do_stuff_with_rvr():
       major, minor, revision = await rvr.get_main_application_version(target=1)
       print("{}.{}.{}".format(major, minor, revision))

   async def do_other_stuff_with_rvr():
       # Set all LEDs to red
       await rvr.set_all_leds_with_32_bit_mask(
           0x3FFFFFFF,
           [255, 0, 0]
       )            

   loop.run_until_complete(
       asyncio.gather(
           do_stuff_with_rvr(),
           do_other_stuff_with_rvr()
       )
   )

-------------------------------------
Receiving Commands From Sphero Robots
-------------------------------------
Sometimes, a Sphero Robot will want to say things without you asking first. Generally, we use handlers (a.k.a. callbacks) to `handle` messages coming from the bot.  To register handlers, toys have methods that begin with ``on_``.  For example, ``on_sensor_streaming_data_notify`` takes a handler with prototype ``handler(sensor_data)``.

Similar to commands to the Robot, there are two ways to register handlers from the Robot:

^^^^^^^^^^^
1. Blocking
^^^^^^^^^^^
.. warning::

    The handler passed is called from a different thread. Use a ``queue.Queue`` to transfer information from one thread to another.

.. code-block:: python

    from spheroboros import BlockingSpheroRvr
    from queue import Queue

    rvr = BlockingSpheroRvr()

    # Using a Queue because sensor_data_handler runs in a different thread than the ``while True``!
    sensor_data_queue = Queue()

    def sensor_data_handler(sensor_data):
        sensor_data_queue.put(sensor_data)

    # Set the Streaming Mask (what actually starts the Robot sending commands)
    rvr.set_sensor_streaming_mask(
        interval=100,  # stream using 100ms intervals
        packet_count=0, # stream forever
        data_mask=0x00070000  # Pitch, Roll, Yaw
    )

    # Register the above defined handler
    rvr.on_sensor_streaming_data_notify(sensor_data_handler)

    while True:
        sensor_data = sensor_data_queue.get():
        print("Pitch: {}".format(sensor_data[0]))
        print("Roll: {}".format(sensor_data[1]))
        print("Yaw: {}".format(sensor_data[2]))
        
^^^^^^^^^^^^^^^
2. Asynchronous
^^^^^^^^^^^^^^^
.. warning::

    The provided handler must be a coroutine, i.e., it must be defined using ``async``.  It will be called using ``await``.

.. code-block:: python

    import asyncio
    from spheroboros import AsyncSpheroRvr
    
    loop = asyncio.get_event_loop()
    
    rvr = AsyncSpheroRvr()

    async def sensor_data_handler(sensor_data):
        print("Pitch: {}".format(sensor_data[0]))
        print("Roll: {}".format(sensor_data[1]))
        print("Yaw: {}".format(sensor_data[2]))
    
    async def start_streaming_data():
        # Set the Streaming Mask (what actually starts the Robot sending commands)
        await rvr.set_sensor_streaming_mask(
            interval=100,  # stream using 100ms intervals
            packet_count=0,  # stream forever
            data_mask=0x00070000  #Pitch, Roll, Yaw 
        )

        # Register the above defined handler
        await rvr.on_sensor_streaming_data_notify(sensor_data_handler)
    
    loop.ensure_future(start_streaming_data())
    loop.run_forever()


.. note::
    
    For both Blocking and Asynchronous, to unregister a handler, simply pass ``None`` to the ``on_`` based method
