Quick Start
===========

There are two ways to interact with Sphero Toys, Blocking and Asynchronous:

Blocking
--------

.. code::

    from spheroboros import BlockingSpheroRvr

    rvr = BlockingSpheroRvr()

    # Get the FW Version of the Nordic Processor
    major, minor, revision = rvr.get_main_application_version(target=1)
    print("{}.{}.{}".format(major, minor, revision))


Asynchronous
____________

.. code::

    import asyncio
    from spheroboros import AsyncSpheroRvr

    loop = asyncio.get_event_loop()

    rvr = AsyncSpheroRvr()

    async def do_stuff_with_rvr():
        major, minor, revision = await rvr.get_main_application_version(target=1)

    async def do_other_stuff_with_rvr():
        # Set all LEDs to red
        await rvr.set_all_leds_with_32_bit_mask(
            0x3FFFFFFF,
            [255, 0, 255]
        )            

    loop.run_until_complete(
        asyncio.gather(
            do_stuff_with_rvr(),
            do_other_stuff_with_rvr()
        )
    )
