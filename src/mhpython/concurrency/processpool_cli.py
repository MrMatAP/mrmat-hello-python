import time
import sys
import concurrent.futures
import itertools

from rich.layout import Layout
from rich.live import Live

from mhpython.concurrency.workers import WorkerMessage, cpu_intensive_work
from mhpython.concurrency.ui import ProgressPanel, ResultsPanel, InfoPanel, console


def ui_update(msg: WorkerMessage,
              progress_panel: ProgressPanel,
              results_panel: ResultsPanel):
    progress_panel.update(msg)
    results_panel.update(msg)


def main() -> int:
    worker_count = 4
    iterations = 100
    progress_panel = ProgressPanel(worker_count=worker_count,
                                   iterations=iterations)
    results_panel = ResultsPanel()
    layout = Layout()
    layout.split_column(
        Layout(name='upper'),
        Layout(results_panel, name='lower')
    )
    layout['upper'].split_row(
        Layout(InfoPanel(info='Using concurrent.futures with ProcessPoolExecutor'), name='info'),
        Layout(progress_panel, name='progress')
    )
    with (Live(layout, refresh_per_second=4, screen=False),
          concurrent.futures.ProcessPoolExecutor() as executor):
        workers = []
        for worker_id in range(0, worker_count):
            workers.append(executor.submit(cpu_intensive_work, worker_id, iterations))
        try:
            for worker in concurrent.futures.as_completed(workers):
                ui_update(worker.result(), progress_panel, results_panel)
        except Exception as e:
            console.print_exception()
        except concurrent.futures.CancelledError | concurrent.futures.TimeoutError as er:
            console.print('CancelledError or TimeoutError')
        except KeyboardInterrupt:
            return 0


if __name__ == '__main__':
    sys.exit(main())
