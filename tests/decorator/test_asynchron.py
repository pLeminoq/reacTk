import time
import threading

from reacTk.decorator.asynchron import asynchron, asynchron_self

print(f"Create class ...")
class AsyncClass:

    def __init__(self, value, name):
        self.lock = threading.Lock()
        self.value = value
        self.name = name

        self.exec_lock = threading.Lock()
        self.exec_lock.acquire()

    @asynchron
    def increment(self):
        # self.value = self.value + 1
        self.value = self.value + 1
        print(f"{self.name=} release exec lock to mark execution start ...")
        self.exec_lock.release()

        print(f"{self.name} rncrement to {self.value=}. Acquire lock on {self.name}")
        with self.lock:
            pass

def test_async_on_instance_method():
    instance_a = AsyncClass(0, name="a")
    instance_b = AsyncClass(10, name="b")

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
