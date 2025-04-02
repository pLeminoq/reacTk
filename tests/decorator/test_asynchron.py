"""
Tests for the asynchron decorators.
Note that these tests become complicated quickly because it must be ensured
that the asynchron methods have started/finished.
This is usually achieved by acquiring/releasing locks.
"""

import time
import threading

from reacTk.decorator import async_once


wait_lock = threading.Lock()
exec_lock = threading.Lock()
exec_lock.acquire()
n_executions = []


@async_once
def async_once_method():
    n_executions.append(1)
    if exec_lock.locked():
        exec_lock.release()

    with wait_lock:
        pass


def test_async_once():
    with wait_lock:
        async_once_method()
        async_once_method()
        async_once_method()
        async_once_method()
        with exec_lock:
            pass
    assert len(n_executions) == 1


class BlockingInstanceMethod:
    """ """

    def __init__(self, value):
        self.lock = threading.Lock()
        self.value = value

        self.exec_lock = threading.Lock()
        self.exec_lock.acquire()

    @async_once
    def increment(self):
        self.value = self.value + 1
        self.exec_lock.release()

        with self.lock:
            pass


def test_async_on_instance_method():
    instance_a = BlockingInstanceMethod(0)
    instance_b = BlockingInstanceMethod(10)

    with instance_a.lock:
        instance_a.increment()
        instance_b.increment()

        with instance_a.exec_lock:
            pass

        # curent_call: threading.Thread = instance_a.increment.__async_data_map[instance_a].current_call
        # print(f"Current_call {curent_call.is_alive()=}")

        assert instance_a.value == 1
        assert instance_b.value == 11


if __name__ == "__main__":
    test_async_on_instance_method()
