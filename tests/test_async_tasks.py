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
import typing

import pytest

from mhpython.async_tasks.base import TaskService, TaskState


async def churn(progress: typing.Callable[[int, str], None],
                done: typing.Callable[[str], None],
                failed: typing.Callable[[str], None]):
    i = 0
    while i < 5:
        progress(i / 5 * 100, f'Iteration {i}')
        i += 1
        await asyncio.sleep(1)
    done('Task finished')


async def fail(progress: typing.Callable[[int, str], None],
               done: typing.Callable[[str], None],
               failed: typing.Callable[[str], None]):
    progress(20, 'failed')
    await asyncio.sleep(3)
    failed('We deliberately failed')


@pytest.mark.asyncio
async def test_async_task():
    svc = TaskService()
    churn_task = await svc.create(churn)
    fail_task = await svc.create(fail)
    assert churn_task is not None
    assert churn_task.percent_complete == 100
    assert churn_task.state == TaskState.DONE

    assert fail_task is not None
    assert fail_task.percent_complete > 0
    assert fail_task.state == TaskState.FAILED
