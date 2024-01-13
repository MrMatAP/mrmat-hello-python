#  MIT License
#
#  Copyright (c) 2022 Mathieu Imfeld
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

import typing

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, TaskID

from .workers import WorkerMessage

console = Console()


class InfoPanel:
    """
    An informational UI panel
    """

    def __init__(self, info: str):
        self._info = info

    def __rich__(self) -> Panel:
        return Panel(f'{self._info}', title='Info')


class ProgressPanel:
    """
    A progress UI panel
    """

    def __init__(self, worker_count: int, iterations: int):
        self._progress = Progress()
        self._worker_tasks: typing.Dict[int, TaskID] = {}
        self._worker_status: typing.Dict[int, str | None] = {}
        for i in range(0, worker_count):
            self._worker_tasks[i] = self._progress.add_task(f'Worker {i}', total=iterations - 1)
            self._worker_status[i] = 'OK'

    def update(self, msg: WorkerMessage):
        self._progress.update(self._worker_tasks[msg.worker_id], completed=msg.iteration)
        self._worker_status[msg.worker_id] = msg.message

    def __rich__(self) -> Panel:
        grid = Table.grid()
        grid.add_row(self._progress)
        for worker_id, status in self._worker_status.items():
            grid.add_row(f'Status {worker_id}: {status}')
        return Panel(grid, title='Progress')


class ResultsPanel:
    """
    A results UI panel
    """

    def __init__(self):
        self._results: typing.List[WorkerMessage] = []

    def update(self, msg: WorkerMessage):
        self._results.append(msg)

    @property
    def results(self):
        return self._results

    def __rich__(self) -> Panel:
        table = Table(show_edge=False)
        table.add_column('Worker ID')
        table.add_column('Result')
        for msg in self._results:
            table.add_row(str(msg.worker_id), str(msg.result))
        return Panel(table, title=f'Results: {len(self._results)}')
