from __future__ import annotations

from typing import Generic, TypeVar

from widget_state import FloatState, IntState, DictState, State

NT = TypeVar("NT", IntState, FloatState)


class PointState(DictState, Generic[NT]):
    """
    Point state that represents 2D pixel coordinates.

    It is often used for drawing.
    """

    def __init__(
        self,
        x: int | IntState | float | FloatState,
        y: int | IntState | float | FloatState,
    ):
        super().__init__()

        self.x = x if isinstance(x, State) else x
        self.y = y if isinstance(y, State) else y

    def __add__(self, other: PointState[NT]) -> PointState[NT]:
        return PointState(self.x.value + other.x.value, self.y.value + other.y.value)

    def __sub__(self, other: PointState[NT]):
        return PointState(self.x.value - other.x.value, self.y.value - other.y.value)


if __name__ == "__main__":
    pt1 = PointState(5.0, 3.141)
    pt2 = PointState(2.0, 2.7)
    print(pt1 + pt2)
    print(pt1 - pt2)
