import asyncio

asyncio.run(main())  # Python 3.7+

# ---------------------------

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
