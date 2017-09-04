#!/usr/bin/env python3

from enum import Enum
from typing import Optional
import sys

import i3ipc
from i3ipc.i3ipc import Con


def window_contains(window: Con, x: int, y: int) -> bool:
    return (window.rect.x <= x < window.rect.x + window.rect.width
            and window.rect.y <= y < window.rect.y + window.rect.height)


def find_window_at(x: int, y: int, tree: Con) -> Optional[Con]:
    return next((leaf for leaf in tree.leaves() if window_contains(leaf, x, y)), None)


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def focus(i3: i3ipc.Connection, dir: Direction):
    tree = i3.get_tree()
    active_window = tree.find_focused()

    x, y = active_window.rect.x, active_window.rect.y
    width, height = active_window.rect.width, active_window.rect.height
    if dir == Direction.LEFT:
        correct_window = find_window_at(x - 1, y, tree)
    elif dir == Direction.RIGHT:
        correct_window = find_window_at(x + width + 1, y, tree)
    elif dir == Direction.UP:
        correct_window = find_window_at(x, y - 1, tree)
    elif dir == Direction.DOWN:
        correct_window = find_window_at(x, y + height + 1, tree)
    else:
        correct_window = None

    if correct_window is not None:
        correct_window.command('focus')


directions = {
    'left': Direction.LEFT,
    'right': Direction.RIGHT,
    'up': Direction.UP,
    'down': Direction.DOWN
}

if len(sys.argv) > 1 and sys.argv[1] in directions:
    i3 = i3ipc.Connection()
    focus(i3, directions[sys.argv[1]])
else:
    print("First argument must be left, right, up or down")
