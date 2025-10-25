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

import asyncio
import enum
import typing
import uuid


class TaskState(enum.Enum):
    INITIALISED = (0,)
    CREATED = (1,)
    RUNNING = (2,)
    DONE = 3
    FAILED = 4


class Task:
    def __init__(self, coro: typing.Any, msg: str = 'Task Created'):
        self._uid = uuid.uuid4()
        self._percent_complete: int = 0
        self._state = TaskState.INITIALISED
        self._msg = msg
        self._task: asyncio.Task | None = None
        self._coro = coro

    @property
    def percent_complete(self) -> int:
        return self._percent_complete

    @property
    def state(self) -> TaskState:
        return self._state

    @property
    def msg(self) -> str:
        return self._msg

    async def run(self):
        self._task = asyncio.create_task(
            self._coro(self.progress, self.done, self.failed)
        )
        self._state = TaskState.CREATED
        await self._task

    def progress(self, percent_complete: int, msg: str = 'Task executing') -> None:
        self._state = TaskState.RUNNING
        self._percent_complete = percent_complete
        self._msg = msg

    def done(self, msg: str = 'Task completed') -> None:
        self._state = TaskState.DONE
        self._percent_complete = 100
        self._msg = msg

    def failed(self, msg: str = 'Task failed') -> None:
        self._state = TaskState.FAILED
        self._msg = msg


class TaskService:
    def __init__(self) -> None:
        self._tasks: typing.Set[Task] = set()

    async def create(self, coro: typing.Any) -> Task:
        t = Task(coro)
        await t.run()
        self._tasks.add(t)
        return t
