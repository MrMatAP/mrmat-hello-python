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

import abc
import typing
import dataclasses
import queue
import concurrent.futures
from cryptography.hazmat.primitives.asymmetric import rsa


@dataclasses.dataclass
class WorkerMessage:
    worker_id: int
    iteration: int
    result: typing.Optional[str] = None
    message: typing.Optional[str] = 'OK'


class Work(abc.ABC):

    def __init__(self, worker_id: int, q: queue.Queue, iterations: typing.Optional[int] = 100):
        self._worker_id = worker_id
        self._q = q
        self._iterations = iterations

    @property
    def worker_id(self) -> int:
        return self._worker_id

    @abc.abstractmethod
    def work(self):
        pass


class CPUIntensiveWorkThreaded(Work):

    def work(self):
        for iteration in range(0, self._iterations):
            try:
                key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
                self._q.put(WorkerMessage(worker_id=self._worker_id,
                                          iteration=iteration,
                                          result=str(key)),
                            block=True)
            except Exception as e:
                self._q.put(WorkerMessage(worker_id=self._worker_id,
                                          iteration=iteration,
                                          message=f'Exception: {e}'),
                            block=True)


def cpu_intensive_work(worker_id: int, iterations: int) -> WorkerMessage:
    keys = list()
    for iteration in range(0, iterations):
        try:
            keys.append(rsa.generate_private_key(public_exponent=65537, key_size=1024))
        except Exception as e:
            pass
    return WorkerMessage(worker_id, iterations, f'Number of keys {len(keys)}', 'OK')


class Execution(abc.ABC):

    def __init__(self,
                 worker_class: typing.Type[Work],
                 worker_count: typing.Optional[int] = 4,
                 iterations: typing.Optional[int] = 100):
        self._q = queue.Queue()
        self._worker_class = worker_class
        self._worker_count = worker_count
        self._iterations = iterations
        self._jobs = []
        self._done = False

    @abc.abstractmethod
    def start(self):
        pass

    @property
    def queue(self) -> queue.Queue:
        return self._q

    @property
    def done(self) -> bool:
        return self._done


class ConcurrentFuturesThreadExecution(Execution):

    def start(self):
        with concurrent.futures.ThreadPoolExecutor(thread_name_prefix='worker') as executor:
            for i in range(0, self._worker_count):
                worker = self._worker_class(worker_id=i,
                                            q=self._q,
                                            iterations=self._iterations)
                self._jobs.append(executor.submit(worker.work))
            status = concurrent.futures.wait(self._jobs, return_when=concurrent.futures.ALL_COMPLETED)
            self._done = True


class ConcurrentFuturesProcessExecution(Execution):

    def start(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map()
            for i in range(0, self._worker_count):
                self._jobs.append(executor.submit(cpu_intensive_work(worker_id=i,
                                                                     iterations=self._iterations,
                                                                     q=self._q)))
            status = concurrent.futures.wait(self._jobs, return_when=concurrent.futures.ALL_COMPLETED)
            self._done = True


