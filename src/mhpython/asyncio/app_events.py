#  MIT License
#
#  Copyright (c) 2024 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import typing
import random
import asyncio


class AppEvent(asyncio.Event):
    def __init__(self, msg: str):
        super().__init__()
        self._msg = msg

    def __repr__(self):
        return f'AppEvent: {self._msg}'


async def event_logger(event_q: asyncio.Queue) -> None:
    """
    Consume all events from a queue and print them onto the console
    Args:
        event_q: The event queue holding events
    Returns:
        Nothing
    """
    try:
        print('Starting event logger task')
        while True:
            event = await event_q.get()
            print(repr(event))
            event_q.task_done()
    except asyncio.CancelledError:
        print('Shutting down event logger task')
    finally:
        print('Event logger task has shut down')


async def event_emitter(event_q: asyncio.Queue) -> None:
    """
        Emit an event at random times between 1 and 5 seconds
    Args:
        event_q: The event queue to place the event on

    Returns:
        Nothing
    """
    try:
        print('Starting event emitter task')
        while True:
            seconds_to_wait = random.randint(1, 5)
            await asyncio.sleep(seconds_to_wait)
            event_q.put_nowait(AppEvent(f'Event after {seconds_to_wait}s'))
    except asyncio.CancelledError:
        print('Shutting down event emitter task')
    finally:
        print('Event emitter task has shut down')


async def main() -> int:
    system_tasks: typing.List[asyncio.Task] = []

    #
    # Start the event system

    event_q: asyncio.Queue = asyncio.Queue()
    system_tasks.append(asyncio.create_task(event_logger(event_q)))
    system_tasks.append(asyncio.create_task(event_emitter(event_q)))

    #
    # Wait until all tasks complete

    try:
        await asyncio.gather(*system_tasks, return_exceptions=False)
    except asyncio.CancelledError:
        print('Shutting down')
    finally:
        print('Shut down')
    return 0


def run():
    """
    We must start the async run from a normal function when running with a script entry point
    Returns:
        System exit code
    """
    sys.exit(asyncio.run(main()))


if __name__ == '__main__':
    run()
