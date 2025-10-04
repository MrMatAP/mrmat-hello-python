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
import concurrent.futures

from rich.layout import Layout
from rich.live import Live

from .workers import WorkerMessage, cpu_intensive_work
from .ui import ProgressPanel, ResultsPanel, InfoPanel


def ui_update(
    msg: WorkerMessage,
    progress_panel: ProgressPanel,
    results_panel: ResultsPanel,
):
    progress_panel.update(msg)
    results_panel.update(msg)


def main() -> int:
    worker_count = 4
    iterations = 100
    progress_panel = ProgressPanel(
        worker_count=worker_count, iterations=iterations
    )
    results_panel = ResultsPanel()
    layout = Layout()
    layout.split_column(
        Layout(name="upper"), Layout(results_panel, name="lower")
    )
    layout["upper"].split_row(
        Layout(
            InfoPanel(info="Using concurrent.futures with ProcessPoolExecutor"),
            name="info",
        ),
        Layout(progress_panel, name="progress"),
    )
    with (
        Live(layout, refresh_per_second=4, screen=False),
        concurrent.futures.ProcessPoolExecutor() as executor,
    ):
        workers = []
        for worker_id in range(0, worker_count):
            workers.append(
                executor.submit(cpu_intensive_work, worker_id, iterations)
            )
        try:
            for worker in concurrent.futures.as_completed(workers):
                ui_update(worker.result(), progress_panel, results_panel)
        except KeyboardInterrupt:
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
