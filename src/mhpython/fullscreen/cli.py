#!python3
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

import sys
import time
import typing
import queue
import concurrent.futures
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live


class ValuePanel:
    """
    A base class for holding a counter, a queue for concurrent data exchange and a UI panel for display
    """

    def __init__(self, title: str, q: queue.Queue, period: typing.Optional[int] = 1):
        self._title = title
        self._current = 0
        self._q = q
        self._period = period

    def __rich__(self) -> Panel:
        panel = Panel(f'Value: [red]{self._current}', title=self._title, expand=True, height=3)
        return panel


class ProducerPanel(ValuePanel):
    """
    A producer panel that emits its update via a concurrent queue
    """

    def work(self):
        while self._current < 10:
            time.sleep(self._period)
            self._current += 1
            self._q.put(self._current, block=True)


class ConsumerPanel(ValuePanel):
    """
    A consumer panel that pulls information from the concurrent queue and displays it
    """

    def work(self):
        while self._current < 10:
            try:
                time.sleep(self._period)
                self._current = self._q.get(block=True)
            except queue.Empty:
                pass


def main() -> int:
    q = queue.Queue()
    layout = Layout()
    producer_panel = ProducerPanel('Producer', q)
    consumer_panel = ConsumerPanel('Consumer', q)
    layout.split_row(
        Layout(producer_panel, name='producer'),
        Layout(consumer_panel, name='consumer')
    )
    with (Live(layout, refresh_per_second=4, screen=False),
          concurrent.futures.ThreadPoolExecutor() as executor):
        executor.submit(producer_panel.work)
        c_job = executor.submit(consumer_panel.work)
        try:
            # We do not require another while/sleep here
            c_job.result()
        except KeyboardInterrupt:
            return 0


if __name__ == '__main__':
    sys.exit(main())
