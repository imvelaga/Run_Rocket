import asyncio

# Define an event producer
async def produce(queue, item):
    await asyncio.sleep(100)  # Simulate some async operation
    await queue.put(item)
    print(f"Produced: {item}")

# Define an event consumer
async def consume(queue):
    while True:
        item = await queue.get()
        print(f"Consumed: {item}")
        queue.task_done()

async def main():
    # Create an asyncio queue
    queue = asyncio.Queue()

    # Create tasks for producer and consumer
    producer_task = asyncio.create_task(produce(queue, 'event1'))
    consumer_task = asyncio.create_task(consume(queue))

    # Wait for both tasks to finish
    await asyncio.gather(producer_task, consumer_task)

# Run the asyncio event loop
asyncio.run(main())