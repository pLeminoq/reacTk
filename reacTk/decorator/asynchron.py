from dataclasses import dataclass
import functools
import threading
from typing import Callable, Generic, Optional, ParamSpec
from warnings import warn


P = ParamSpec("P")


def is_instance_method(func: Callable) -> bool:
    params = list(inspect.signature(func).parameters.values())
    return len(params) > 0 and params[0].name == "self"


@dataclass
class AsyncData(Generic[P]):
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.current_call: Optional[threading.Thread] = None
        self.pending_call: Optional[threading.Thread] = None

        self.last_args: Optional[P.args] = None
        self.last_kwargs: Optional[P.kwargs] = None


def asynchron(func: Callable[P, None]) -> Callable[P, None]:
    warn("`asynchron` decorator is deprecated. Use `async_once` instead")
    async_data = AsyncData()

    def trigger_pending() -> None:
        async_data.current_call.join()

        with async_data.lock:
            async_data.pending_call = None

            async_data.current_call = threading.Thread(
                target=func, args=async_data.last_args, kwargs=async_data.last_kwargs
            )
            async_data.current_call.start()

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        with async_data.lock:
            if async_data.current_call is None:
                async_data.current_call = threading.Thread(
                    target=func, args=args, kwargs=kwargs
                )
                async_data.current_call.start()
                return

            async_data.last_args = args
            async_data.last_kwargs = kwargs
            if (
                async_data.pending_call is None
                or async_data.pending_call.is_alive() is False
            ):
                async_data.pending_call = threading.Thread(target=trigger_pending)
                async_data.pending_call.start()

    return wrapper

def async_once(func: Callable[P, None]) -> Callable[P, None]:
    # async_data = AsyncData()
    async_data_map_lock = threading.Lock()
    async_data_map = {}

    # def wait():
    #     print(f"Wait for func ...{func.__name__=}")
    #     for i, async_data in enumerate(async_data_map.values()):
    #         print(f" - Lock {i=}")
    #         with async_data.lock:
    #             pass
    #
    # func.__wait = wait

    func.__async_data_map = async_data_map

    def trigger_pending(async_data) -> None:
        async_data.current_call.join()

        with async_data.lock:
            async_data.pending_call = None

            async_data.current_call = threading.Thread(
                target=func, args=async_data.last_args, kwargs=async_data.last_kwargs
            )
            async_data.current_call.start()

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        print(f"Call to func {func.__name__=}")
        with async_data_map_lock:
            _self = args[0]
            if _self not in async_data_map:
                async_data_map[_self] = AsyncData()
            async_data = async_data_map[_self]

        with async_data.lock:
            if async_data.current_call is None:
                async_data.current_call = threading.Thread(
                    target=func, args=args, kwargs=kwargs
                )
                print(f"Start current call")
                async_data.current_call.start()
                return

            async_data.last_args = args
            async_data.last_kwargs = kwargs
            if (
                async_data.pending_call is None
                or async_data.pending_call.is_alive() is False
            ):
                async_data.pending_call = threading.Thread(target=trigger_pending, args=[async_data])
                async_data.pending_call.start()


    return wrapper
