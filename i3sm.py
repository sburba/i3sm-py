#!/usr/bin/env python3

import sys
from enum import Enum
from typing import Optional

import i3ipc
from i3ipc.i3ipc import Con


def contains(window: Con, x: int, y: int) -> bool:
    return (window.rect.x <= x < window.rect.x + window.rect.width
            and window.rect.y <= y < window.rect.y + window.rect.height)


def is_eligible_node(node: Con):
    return (node.type == 'con' or node.type == 'workspace') and not node.nodes


def find_eligible_node_at(x: int, y: int, tree: Con) -> Optional[Con]:
    return next((node for node in tree.descendents() if is_eligible_node(node) and contains(node, x, y)), None)


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
        x = x - 1
    elif dir == Direction.RIGHT:
        x = x + width + 1
    elif dir == Direction.UP:
        y = y - 1
    elif dir == Direction.DOWN:
        y = y + height + 1
    else:
        raise ValueError('{} is not a valid direction', dir)

    correct_window = find_eligible_node_at(x, y, tree)

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
