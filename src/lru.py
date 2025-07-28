#!/usr/bin/env python3
from tkinter import NO
from typing import Any, Optional

class LRUCache:
    """
    A Least Recently Used (LRU) cache keeps items in the cache until it reaches its size
    and/or item limit (only item in our case). In which case, it removes an item that was accessed
    least recently.
    An item is considered accessed whenever `has`, `get`, or `set` is called with its key.

    Implement the LRU cache here and use the unit tests to check your implementation.
    """

    def __init__(self, item_limit: int):
        self.item_limit=item_limit
        self.cache={}
        self.dll = DoublyLinkedList()


    def has(self, key: str) -> bool:
        if key in self.cache:
            # move that node with same key to head
            self.dll.move_to_head(self.cache[key])
            return True
        return False


    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            # move that node with same key to head
            self.dll.move_to_head(self.cache[key])
            return self.cache[key].value
        return None

    def set(self, key: str, value: Any):
        if key in self.cache:
            # move that node with same key to head
            self.dll.move_to_head(self.cache[key])
            return
        node = Node(key, value)
        self.dll.add_to_head(node)
        self.cache[key] = node
        if len(self.cache)>self.item_limit:
            node = self.dll.remove_tail()
            del self.cache[node.key]
            


class Node:
    def __init__(self, key:str, value:str):
        self.key=key
        self.value=value
        self.prev=None
        self.next=None
    
class DoublyLinkedList:
    def __init__(self):
        self.head=Node('head', None)
        self.tail=Node('tail', None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_head(self, node: Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_to_head(self, node: Node):
        self.remove_node(node)
        self.add_to_head(node)

    def remove_tail(self):
        node = self.tail.prev
        if node == self.head:
            return
        # this is also correct version
        # self.tail.prev = self.tail.prev.prev
        # self.tail.prev.next = self.tail
        self.remove_node(node)
        return node
    





     
